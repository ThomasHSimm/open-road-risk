"""
Adjusted expected-KSI severity-reporting consistency diagnostic.

This is a Part A rerun only. It uses DfT collision-level adjusted severity
probabilities to check force/year consistency and does not fit KSI models, run
EB shrinkage, or change production risk artefacts.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Any

import pandas as pd

from road_risk.config import _ROOT, FORCE_CODES
from road_risk.model.collision import RLA_PATH

logger = logging.getLogger(__name__)

SNAPPED_PATH = _ROOT / "data/processed/stats19/snapped_weighted.parquet"
ORIGINAL_REPORT_PATH = _ROOT / "reports/ksi_reporting_consistency.md"
REPORT_PATH = _ROOT / "reports/ksi_reporting_consistency_adjusted.md"
FIGURE_DIR = _ROOT / "reports/figures"

FATAL_VALUE = 1
SERIOUS_VALUE = 2
YOY_FLAG_THRESHOLD = 20.0
PRACTICAL_KSI_COUNT_CHANGE_THRESHOLD = 25.0
SENSITIVITY_WINDOWS = [
    (2015, 2024),
    (2017, 2024),
    (2017, 2023),
    (2019, 2023),
]

REQUIRED_COLUMNS = {
    "collision_index",
    "collision_severity",
    "collision_adjusted_severity_serious",
    "police_force",
    "link_id",
    "snap_method",
}


@dataclass(frozen=True)
class DiagnosticResult:
    adjusted_counts: pd.DataFrame
    recorded_counts: pd.DataFrame
    adjusted_flags: pd.DataFrame
    recorded_flags: pd.DataFrame
    verdict: str
    operational_decision: str
    missing_fields: list[str]
    input_rows: int
    retained_rows: int
    figure_paths: dict[str, str]


def _force_lookup() -> dict[int, str]:
    return {int(code): name.replace("_", " ").title() for name, code in FORCE_CODES.items()}


def _markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(lines)


def _relative(path: str) -> str:
    return str(path).replace(str(_ROOT) + "/", "")


def _load_snapped() -> pd.DataFrame:
    if not SNAPPED_PATH.exists():
        raise FileNotFoundError(f"Required snapped collision file not found: {SNAPPED_PATH}")
    return pd.read_parquet(SNAPPED_PATH)


def _prepare_collision_frame(collisions: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    missing = sorted(REQUIRED_COLUMNS - set(collisions.columns))
    if "collision_year" not in collisions.columns and "date" not in collisions.columns:
        missing.append("collision_year_or_date")
    if missing:
        return pd.DataFrame(), missing

    df = collisions.copy()
    if "collision_year" in df.columns:
        df["year"] = df["collision_year"].astype("Int64")
    else:
        df["year"] = pd.to_datetime(df["date"], errors="coerce").dt.year.astype("Int64")

    df = df[df["snap_method"].isin(["attribute", "spatial", "weighted"])].copy()
    if "snap_score" in df.columns:
        df = df[df["snap_score"] >= 0.6].copy()

    df = df[df["year"].notna()].copy()
    df["year"] = df["year"].astype(int)
    df["police_force"] = df["police_force"].astype(int)
    df["recorded_ksi"] = df["collision_severity"].isin({FATAL_VALUE, SERIOUS_VALUE}).astype(float)
    df["fatal_indicator"] = (df["collision_severity"] == FATAL_VALUE).astype(float)
    df["adjusted_expected_ksi"] = df["fatal_indicator"] + df[
        "collision_adjusted_severity_serious"
    ].astype(float)

    bad_adjusted = df["adjusted_expected_ksi"].isna()
    if bad_adjusted.any():
        missing_count = int(bad_adjusted.sum())
        raise ValueError(f"{missing_count:,} retained rows have missing adjusted expected KSI")

    return df, []


def _summarise_force_year(df: pd.DataFrame, target_col: str, target_name: str) -> pd.DataFrame:
    force_names = _force_lookup()
    counts = (
        df.groupby(["police_force", "year"], observed=True)
        .agg(
            all_injury_count=("collision_index", "count"),
            target=(target_col, "sum"),
        )
        .reset_index()
        .sort_values(["police_force", "year"])
    )
    counts["force_name"] = counts["police_force"].map(force_names).fillna("Unknown")
    counts[target_name] = counts.pop("target")
    counts[f"{target_name}_to_all_injury_ratio"] = counts[target_name] / counts["all_injury_count"]
    counts[f"prior_{target_name}"] = counts.groupby("police_force")[target_name].shift(1)
    counts[f"{target_name}_change"] = counts[target_name] - counts[f"prior_{target_name}"]
    counts["ratio_yoy_pct_change"] = (
        counts.groupby("police_force")[f"{target_name}_to_all_injury_ratio"].pct_change() * 100
    )
    counts["flag_yoy_gt_20pct"] = counts["ratio_yoy_pct_change"].abs() > YOY_FLAG_THRESHOLD
    counts["flag_yoy_gt_20pct_and_abs_ksi_change_ge25"] = counts["flag_yoy_gt_20pct"] & (
        counts[f"{target_name}_change"].abs() >= PRACTICAL_KSI_COUNT_CHANGE_THRESHOLD
    )
    return counts[
        [
            "police_force",
            "force_name",
            "year",
            "all_injury_count",
            target_name,
            f"{target_name}_to_all_injury_ratio",
            f"{target_name}_change",
            "ratio_yoy_pct_change",
            "flag_yoy_gt_20pct",
            "flag_yoy_gt_20pct_and_abs_ksi_change_ge25",
        ]
    ]


def _force_list(values: pd.Series) -> str:
    codes = sorted(int(value) for value in values.dropna().unique())
    return ", ".join(str(code) for code in codes) if codes else "none"


def _window_sensitivity(counts: pd.DataFrame, target_name: str) -> pd.DataFrame:
    rows = []
    for start_year, end_year in SENSITIVITY_WINDOWS:
        sub = counts[counts["year"].between(start_year, end_year)]
        flags = sub[sub["flag_yoy_gt_20pct"]]
        practical_flags = sub[sub["flag_yoy_gt_20pct_and_abs_ksi_change_ge25"]]
        all_injury = int(sub["all_injury_count"].sum())
        target_total = float(sub[target_name].sum())
        rows.append(
            {
                "window": f"{start_year}-{end_year}",
                "number_of_forces": int(sub["police_force"].nunique()),
                "number_of_force_year_rows": int(len(sub)),
                "all_injury_count": all_injury,
                target_name: target_total,
                "overall_ratio": target_total / all_injury if all_injury else float("nan"),
                "flagged_force_year_rows": int(len(flags)),
                "forces_with_any_flagged_years": _force_list(flags["police_force"]),
                "practical_flagged_force_year_rows": int(len(practical_flags)),
                "forces_with_any_practical_flagged_years": _force_list(
                    practical_flags["police_force"]
                ),
            }
        )
    return pd.DataFrame(rows)


def _determine_verdict(counts: pd.DataFrame, flags: pd.DataFrame) -> tuple[str, str]:
    if counts.empty:
        return (
            "diagnostic incomplete",
            "keep KSI parked because adjusted Part A could not be completed.",
        )
    if flags.empty:
        return (
            "pass / proceed to Part B",
            (
                "adjusted Part A passes the pre-registered force/year consistency gate, "
                "but this diagnostic alone does not unpark KSI modelling."
            ),
        )

    n_forces = counts["police_force"].nunique()
    flags_2024 = flags.loc[flags["year"] == 2024, "police_force"].nunique()
    if n_forces > 0 and flags_2024 / n_forces > 0.5:
        return (
            "restrict years",
            "restrict to 2015-2023 before any Part B rerun; do not use 2024 intact.",
        )

    flag_years = set(flags["year"])
    if flag_years <= {2016, 2017}:
        return (
            "restrict years",
            "restrict to post-2016 years before any Part B rerun.",
        )

    flagged_forces = flags["police_force"].nunique()
    if flagged_forces == 1:
        force = int(flags["police_force"].iloc[0])
        return (
            "restrict forces",
            f"exclude or separately handle force {force} before any Part B rerun.",
        )

    return (
        "keep KSI parked",
        (
            "adjusted Part A still shows heterogeneous force/year breaks, so Part B "
            "should not be run as a defensible national-scope KSI modelling stage."
        ),
    )


def _plot_panel(
    counts: pd.DataFrame,
    y_col: str,
    ylabel: str,
    title: str,
    out_path: str,
    *,
    percent_axis: bool = False,
) -> None:
    os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")
    import matplotlib.pyplot as plt

    forces = counts[["police_force", "force_name"]].drop_duplicates().sort_values("police_force")
    n_forces = len(forces)
    ncols = 4
    nrows = max((n_forces + ncols - 1) // ncols, 1)

    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(14, 2.4 * nrows), sharex=True)
    axes_list = axes.flatten() if hasattr(axes, "flatten") else [axes]

    for ax, (_, force) in zip(axes_list, forces.iterrows(), strict=False):
        sub = counts[counts["police_force"] == force["police_force"]].sort_values("year")
        ax.plot(sub["year"], sub[y_col], marker="o", linewidth=1.7)
        flagged = sub[sub["flag_yoy_gt_20pct"]]
        if not flagged.empty:
            ax.scatter(flagged["year"], flagged[y_col], color="#c41e3a", s=35, zorder=3)
        ax.set_title(f"{force['police_force']} {force['force_name']}", fontsize=10)
        ax.grid(True, alpha=0.25)
        if percent_axis:
            ax.yaxis.set_major_formatter(lambda value, _pos: f"{value:.0%}")

    for ax in axes_list[n_forces:]:
        ax.axis("off")

    fig.suptitle(title, fontsize=14)
    fig.supxlabel("Collision year")
    fig.supylabel(ylabel)
    fig.tight_layout()
    fig.savefig(out_path, dpi=110, bbox_inches="tight")
    plt.close(fig)


def _write_plots(counts: pd.DataFrame) -> dict[str, str]:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    count_path = FIGURE_DIR / "ksi_reporting_consistency_adjusted_expected_count.png"
    ratio_path = FIGURE_DIR / "ksi_reporting_consistency_adjusted_ratio.png"
    _plot_panel(
        counts,
        "adjusted_expected_ksi",
        "Adjusted expected KSI",
        "Adjusted expected KSI by force and year",
        str(count_path),
    )
    _plot_panel(
        counts,
        "adjusted_expected_ksi_to_all_injury_ratio",
        "Adjusted expected KSI / all-injury ratio",
        "Adjusted expected KSI-to-all-injury ratio by force and year",
        str(ratio_path),
        percent_axis=True,
    )
    return {"count": _relative(str(count_path)), "ratio": _relative(str(ratio_path))}


def _format_float(value: float, digits: int = 1) -> str:
    if pd.isna(value):
        return ""
    return f"{value:,.{digits}f}"


def _format_int(value: float) -> str:
    if pd.isna(value):
        return ""
    return f"{int(value):,}"


def _format_pct(value: float, digits: int = 1) -> str:
    if pd.isna(value):
        return ""
    return f"{value:.{digits}f}%"


def _format_ratio(value: float) -> str:
    if pd.isna(value):
        return ""
    return f"{value:.4f}"


def _format_change(value: float) -> str:
    if pd.isna(value):
        return ""
    return f"{value:+,.1f}"


def _format_bool(value: bool) -> str:
    return "yes" if bool(value) else "no"


def _summary_rows(counts: pd.DataFrame, target_name: str) -> list[list[Any]]:
    summary = (
        counts.groupby("year")
        .agg(
            all_injury_count=("all_injury_count", "sum"),
            target=(target_name, "sum"),
            flagged_force_years=("flag_yoy_gt_20pct", "sum"),
            practical_flagged_force_years=(
                "flag_yoy_gt_20pct_and_abs_ksi_change_ge25",
                "sum",
            ),
        )
        .reset_index()
    )
    summary["ratio"] = summary["target"] / summary["all_injury_count"]
    return [
        [
            int(row.year),
            _format_int(row.all_injury_count),
            _format_float(row.target),
            _format_ratio(row.ratio),
            int(row.flagged_force_years),
            int(row.practical_flagged_force_years),
        ]
        for row in summary.itertuples(index=False)
    ]


def _flag_rows(flags: pd.DataFrame) -> list[list[Any]]:
    return [
        [
            int(row.police_force),
            row.force_name,
            int(row.year),
            _format_int(row.all_injury_count),
            _format_float(row.adjusted_expected_ksi),
            _format_ratio(row.adjusted_expected_ksi_to_all_injury_ratio),
            _format_change(row.adjusted_expected_ksi_change),
            _format_pct(row.ratio_yoy_pct_change),
            _format_bool(row.flag_yoy_gt_20pct_and_abs_ksi_change_ge25),
        ]
        for row in flags.sort_values(["year", "police_force"]).itertuples(index=False)
    ]


def _force_year_rows(counts: pd.DataFrame) -> list[list[Any]]:
    return [
        [
            int(row.police_force),
            row.force_name,
            int(row.year),
            _format_int(row.all_injury_count),
            _format_float(row.adjusted_expected_ksi),
            _format_ratio(row.adjusted_expected_ksi_to_all_injury_ratio),
            _format_pct(row.ratio_yoy_pct_change),
            _format_bool(row.flag_yoy_gt_20pct),
        ]
        for row in counts.sort_values(["police_force", "year"]).itertuples(index=False)
    ]


def _comparison_rows(result: DiagnosticResult) -> list[list[Any]]:
    adjusted = result.adjusted_counts
    recorded = result.recorded_counts
    adjusted_sensitivity = _window_sensitivity(adjusted, "adjusted_expected_ksi")
    recorded_sensitivity = _window_sensitivity(recorded, "recorded_ksi")
    return [
        [
            "unadjusted recorded KSI",
            _format_float(recorded["recorded_ksi"].sum()),
            _format_ratio(recorded["recorded_ksi"].sum() / recorded["all_injury_count"].sum()),
            len(result.recorded_flags),
            int(recorded["flag_yoy_gt_20pct_and_abs_ksi_change_ge25"].sum()),
            recorded_sensitivity.loc[
                recorded_sensitivity["practical_flagged_force_year_rows"].idxmin(), "window"
            ],
        ],
        [
            "adjusted expected KSI",
            _format_float(adjusted["adjusted_expected_ksi"].sum()),
            _format_ratio(
                adjusted["adjusted_expected_ksi"].sum() / adjusted["all_injury_count"].sum()
            ),
            len(result.adjusted_flags),
            int(adjusted["flag_yoy_gt_20pct_and_abs_ksi_change_ge25"].sum()),
            adjusted_sensitivity.loc[
                adjusted_sensitivity["practical_flagged_force_year_rows"].idxmin(), "window"
            ],
        ],
    ]


def _write_report(result: DiagnosticResult) -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Adjusted Expected KSI Reporting Consistency Diagnostic",
        "",
        (
            "**Status:** Part A diagnostic rerun only. No KSI modelling, EB shrinkage, "
            "decision-register edit, or production model change."
        ),
        "",
        "## Purpose",
        "",
        (
            "This report reruns the KSI Part A force/year reporting consistency check "
            "using DfT collision-level adjusted severity probabilities. It tests whether "
            "the adjusted expected KSI target clears the same pre-registered +/-20% "
            "year-on-year KSI-to-all-injury ratio threshold used in the original Part A "
            "diagnostic."
        ),
        "",
        "## Input Files",
        "",
        f"- Stage 2 collision count table: `{_relative(str(RLA_PATH))}`",
        f"- Snapped collision source: `{_relative(str(SNAPPED_PATH))}`",
        f"- Original unadjusted Part A report: `{_relative(str(ORIGINAL_REPORT_PATH))}`",
        f"- Input collision rows: {result.input_rows:,}",
        f"- Retained rows after Stage 2 snap-method and snap-score filters: {result.retained_rows:,}",
        "",
        "## Target Definition",
        "",
        "For each retained collision:",
        "",
        "```text",
        "fatal_indicator = 1 if collision_severity == 1 else 0",
        "adjusted_expected_ksi = fatal_indicator + collision_adjusted_severity_serious",
        "```",
        "",
        (
            "`enhanced_severity_collision` is not used directly as the KSI target. "
            "The adjusted target is an expected-count target, not an observed integer "
            "collision count."
        ),
        "",
    ]

    if result.missing_fields:
        lines.extend(
            [
                "## Missing Fields",
                "",
                _markdown_table(["missing field"], [[field] for field in result.missing_fields]),
                "",
                "## Verdict",
                "",
                "**Headline adjusted Part A verdict:** diagnostic incomplete.",
                "",
                "**Parking status:** KSI remains parked.",
            ]
        )
        REPORT_PATH.write_text("\n".join(lines) + "\n")
        return

    adjusted = result.adjusted_counts
    adjusted_total = float(adjusted["adjusted_expected_ksi"].sum())
    all_injury_total = int(adjusted["all_injury_count"].sum())
    practical_adjusted_flags = int(adjusted["flag_yoy_gt_20pct_and_abs_ksi_change_ge25"].sum())
    sensitivity = _window_sensitivity(adjusted, "adjusted_expected_ksi")
    sensitivity_rows = [
        [
            row.window,
            int(row.number_of_forces),
            int(row.number_of_force_year_rows),
            _format_int(row.all_injury_count),
            _format_float(row.adjusted_expected_ksi),
            _format_ratio(row.overall_ratio),
            int(row.flagged_force_year_rows),
            row.forces_with_any_flagged_years,
            int(row.practical_flagged_force_year_rows),
            row.forces_with_any_practical_flagged_years,
        ]
        for row in sensitivity.itertuples(index=False)
    ]

    lines.extend(
        [
            "## Summary",
            "",
            _markdown_table(
                ["metric", "value"],
                [
                    ["force/year rows", len(adjusted)],
                    ["forces", adjusted["police_force"].nunique()],
                    ["years", f"{adjusted['year'].min()}-{adjusted['year'].max()}"],
                    ["all-injury collisions", _format_int(all_injury_total)],
                    ["adjusted expected KSI", _format_float(adjusted_total)],
                    [
                        "overall adjusted expected KSI/all-injury ratio",
                        _format_ratio(adjusted_total / all_injury_total),
                    ],
                    ["pre-registered flagged force/year rows", len(result.adjusted_flags)],
                    ["practical-sensitivity flagged force/year rows", practical_adjusted_flags],
                ],
            ),
            "",
            "## By Year",
            "",
            _markdown_table(
                [
                    "year",
                    "all_injury_count",
                    "adjusted_expected_ksi",
                    "adjusted_expected_ksi_to_all_injury_ratio",
                    "pre_registered_flagged_force_years",
                    "practical_sensitivity_flagged_force_years",
                ],
                _summary_rows(adjusted, "adjusted_expected_ksi"),
            ),
            "",
            "## Force-Year Ratios",
            "",
            _markdown_table(
                [
                    "police_force",
                    "force_name",
                    "year",
                    "all_injury_count",
                    "adjusted_expected_ksi",
                    "adjusted_expected_ksi_to_all_injury_ratio",
                    "ratio_yoy_pct_change",
                    "pre_registered_flag",
                ],
                _force_year_rows(adjusted),
            ),
            "",
            "## Plots",
            "",
            f"![Adjusted expected KSI by force and year]({result.figure_paths['count']})",
            "",
            (
                "![Adjusted expected KSI-to-all-injury ratio by force and year]"
                f"({result.figure_paths['ratio']})"
            ),
            "",
            "## Flagged Force/Year Breaks",
            "",
        ]
    )

    if result.adjusted_flags.empty:
        lines.append("No force/year rows exceeded the +/-20% year-on-year ratio-change flag.")
    else:
        lines.append(
            _markdown_table(
                [
                    "police_force",
                    "force_name",
                    "year",
                    "all_injury_count",
                    "adjusted_expected_ksi",
                    "adjusted_expected_ksi_to_all_injury_ratio",
                    "adjusted_expected_ksi_change",
                    "ratio_yoy_pct_change",
                    "practical_sensitivity_flag",
                ],
                _flag_rows(result.adjusted_flags),
            )
        )

    lines.extend(
        [
            "",
            "## Window Sensitivity",
            "",
            (
                "The pre-registered flag is the +/-20% year-on-year ratio-change rule. "
                "The practical-sensitivity flag mirrors the original extra check using "
                "an absolute adjusted expected-KSI change of at least 25."
            ),
            "",
            _markdown_table(
                [
                    "window",
                    "number_of_forces",
                    "number_of_force_year_rows",
                    "all_injury_count",
                    "adjusted_expected_ksi",
                    "overall_adjusted_ratio",
                    "pre_registered_flagged_force_year_rows",
                    "forces_with_any_pre_registered_flagged_years",
                    "practical_sensitivity_flagged_force_year_rows",
                    "forces_with_any_practical_sensitivity_flagged_years",
                ],
                sensitivity_rows,
            ),
            "",
            "## Comparison With Original Part A",
            "",
            _markdown_table(
                [
                    "target",
                    "total_ksi_metric",
                    "overall_ratio",
                    "pre_registered_flagged_force_year_rows",
                    "practical_sensitivity_flagged_force_year_rows",
                    "least_disrupted_tested_window",
                ],
                _comparison_rows(result),
            ),
            "",
            (
                "The adjusted target materially reduces the original recorded-KSI flag "
                "count, but it does not clear the pre-registered Part A consistency gate. "
                "The decision still follows the pre-registered Part A logic, not an "
                "after-the-fact threshold."
            ),
            "",
            "## Methodological Caveats",
            "",
            ("- Adjusted expected KSI is an expected-count target, not an observed integer count."),
            (
                "- The adjusted severity columns are suitable for aggregate force/year "
                "checks; they are not deterministic record-level labels."
            ),
            (
                "- Passing adjusted Part A would not automatically justify full KSI "
                "modelling. It would only clear the reporting-consistency gate for a "
                "future Part B."
            ),
            (
                "- EB shrinkage is not a drop-in target swap, because the current EB "
                "layer assumes observed integer counts."
            ),
            (
                "- If Part B proceeds later, it must specify whether EB is re-derived "
                "for expected-count targets or deferred."
            ),
            "",
            "## Verdict",
            "",
            f"**Headline adjusted Part A verdict:** {result.verdict}.",
            "",
            f"**Operational decision:** {result.operational_decision}",
            "",
            (
                "**Parking status:** this diagnostic does not unpark the KSI atlas or "
                "modify the decision register."
            ),
        ]
    )

    REPORT_PATH.write_text("\n".join(lines) + "\n")


def run() -> DiagnosticResult:
    collisions = _load_snapped()
    prepared, missing = _prepare_collision_frame(collisions)

    if missing:
        result = DiagnosticResult(
            adjusted_counts=pd.DataFrame(),
            recorded_counts=pd.DataFrame(),
            adjusted_flags=pd.DataFrame(),
            recorded_flags=pd.DataFrame(),
            verdict="diagnostic incomplete",
            operational_decision="keep KSI parked because adjusted Part A could not be completed.",
            missing_fields=missing,
            input_rows=len(collisions),
            retained_rows=0,
            figure_paths={},
        )
        _write_report(result)
        return result

    adjusted_counts = _summarise_force_year(
        prepared,
        "adjusted_expected_ksi",
        "adjusted_expected_ksi",
    )
    recorded_counts = _summarise_force_year(prepared, "recorded_ksi", "recorded_ksi")
    adjusted_flags = adjusted_counts[adjusted_counts["flag_yoy_gt_20pct"]].copy()
    recorded_flags = recorded_counts[recorded_counts["flag_yoy_gt_20pct"]].copy()
    verdict, operational_decision = _determine_verdict(adjusted_counts, adjusted_flags)
    figure_paths = _write_plots(adjusted_counts)

    result = DiagnosticResult(
        adjusted_counts=adjusted_counts,
        recorded_counts=recorded_counts,
        adjusted_flags=adjusted_flags,
        recorded_flags=recorded_flags,
        verdict=verdict,
        operational_decision=operational_decision,
        missing_fields=[],
        input_rows=len(collisions),
        retained_rows=len(prepared),
        figure_paths=figure_paths,
    )
    _write_report(result)
    return result


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    result = run()
    logger.info("Wrote %s", REPORT_PATH)
    logger.info("Headline adjusted Part A verdict: %s", result.verdict)


if __name__ == "__main__":
    main()
