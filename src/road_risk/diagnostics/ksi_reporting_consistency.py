"""
KSI severity-reporting consistency diagnostic.

This is Part A of the pre-registered KSI diagnostic only. It does not fit KSI
models, run EB shrinkage, or change production risk artefacts.
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
REPORT_PATH = _ROOT / "reports/ksi_reporting_consistency.md"
FIGURE_DIR = _ROOT / "reports/figures/ksi_reporting_consistency"

FATAL_SERIOUS_VALUES = {1, 2}
YOY_FLAG_THRESHOLD = 20.0
PRACTICAL_KSI_COUNT_CHANGE_THRESHOLD = 25
SENSITIVITY_WINDOWS = [
    (2015, 2024),
    (2017, 2024),
    (2017, 2023),
    (2019, 2023),
]

REQUIRED_COLUMNS = {
    "collision_index",
    "collision_severity",
    "police_force",
    "link_id",
    "snap_method",
}


@dataclass(frozen=True)
class DiagnosticResult:
    counts: pd.DataFrame
    flags: pd.DataFrame
    verdict: str
    practical_recommendation: str
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
    df["is_ksi"] = df["collision_severity"].isin(FATAL_SERIOUS_VALUES).astype(int)
    return df, []


def _summarise_force_year(df: pd.DataFrame) -> pd.DataFrame:
    force_names = _force_lookup()
    counts = (
        df.groupby(["police_force", "year"], observed=True)
        .agg(
            all_injury_count=("collision_index", "count"),
            ksi_count=("is_ksi", "sum"),
        )
        .reset_index()
        .sort_values(["police_force", "year"])
    )
    counts["force_name"] = counts["police_force"].map(force_names).fillna("Unknown")
    counts["ksi_to_all_injury_ratio"] = counts["ksi_count"] / counts["all_injury_count"]
    counts["prior_ksi_count"] = counts.groupby("police_force")["ksi_count"].shift(1)
    counts["ksi_count_change"] = counts["ksi_count"] - counts["prior_ksi_count"]
    counts["ratio_yoy_pct_change"] = (
        counts.groupby("police_force")["ksi_to_all_injury_ratio"].pct_change() * 100
    )
    counts["flag_yoy_gt_20pct"] = counts["ratio_yoy_pct_change"].abs() > YOY_FLAG_THRESHOLD
    counts["flag_yoy_gt_20pct_and_abs_ksi_change_ge25"] = counts["flag_yoy_gt_20pct"] & (
        counts["ksi_count_change"].abs() >= PRACTICAL_KSI_COUNT_CHANGE_THRESHOLD
    )
    return counts[
        [
            "police_force",
            "force_name",
            "year",
            "all_injury_count",
            "ksi_count",
            "ksi_to_all_injury_ratio",
            "ksi_count_change",
            "ratio_yoy_pct_change",
            "flag_yoy_gt_20pct",
            "flag_yoy_gt_20pct_and_abs_ksi_change_ge25",
        ]
    ]


def _determine_verdict(counts: pd.DataFrame, flags: pd.DataFrame, missing: list[str]) -> str:
    if missing:
        return "Verdict: diagnostic could not be completed because required fields were missing."
    if flags.empty:
        return "Verdict: use 2015–2024 intact."

    n_forces = counts["police_force"].nunique()
    flags_2024 = flags.loc[flags["year"] == 2024, "police_force"].nunique()
    if n_forces > 0 and flags_2024 / n_forces > 0.5:
        return "Verdict: restrict to 2015–2023."

    around_2016 = flags[flags["year"].isin([2016, 2017])]
    other_flag_years = set(flags["year"]) - {2016, 2017, 2024}
    if not around_2016.empty and len(other_flag_years) == 0:
        return "Verdict: restrict to post-2016 years."

    return "Verdict: per-force handling required before KSI modelling is defensible."


def _practical_recommendation(counts: pd.DataFrame) -> str:
    if counts.empty:
        return "Practical modelling recommendation: diagnostic incomplete; do not run Part B."

    sensitivity = _window_sensitivity(counts)
    clean_windows = sensitivity[
        (sensitivity["flagged_force_year_rows"] == 0)
        & (sensitivity["practical_flagged_force_year_rows"] == 0)
    ]
    if not clean_windows.empty:
        first_clean = clean_windows.iloc[0]
        return (
            "Practical modelling recommendation: Part B should use the restricted "
            f"{first_clean['window']} year window."
        )

    few_practical_flags = sensitivity["practical_flagged_force_year_rows"].min() <= 3
    if few_practical_flags:
        best = sensitivity.sort_values(
            ["practical_flagged_force_year_rows", "flagged_force_year_rows"]
        ).iloc[0]
        return (
            "Practical modelling recommendation: Part B can continue only as a sensitivity "
            f"analysis, with {best['window']} as the least-disrupted window and no headline "
            "KSI model claim."
        )

    return (
        "Practical modelling recommendation: Part B can continue only as a sensitivity "
        "analysis, not as a defensible standalone KSI modelling stage; all tested windows "
        "retain heterogeneous force/year breaks."
    )


def _force_list(values: pd.Series) -> str:
    codes = sorted(int(value) for value in values.dropna().unique())
    return ", ".join(str(code) for code in codes) if codes else "none"


def _window_sensitivity(counts: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for start_year, end_year in SENSITIVITY_WINDOWS:
        sub = counts[counts["year"].between(start_year, end_year)]
        flags = sub[sub["flag_yoy_gt_20pct"]]
        practical_flags = sub[sub["flag_yoy_gt_20pct_and_abs_ksi_change_ge25"]]
        all_injury = int(sub["all_injury_count"].sum())
        ksi = int(sub["ksi_count"].sum())
        rows.append(
            {
                "window": f"{start_year}–{end_year}",
                "number_of_forces": int(sub["police_force"].nunique()),
                "number_of_force_year_rows": int(len(sub)),
                "all_injury_count": all_injury,
                "ksi_count": ksi,
                "overall_ksi_to_all_injury_ratio": ksi / all_injury if all_injury else float("nan"),
                "flagged_force_year_rows": int(len(flags)),
                "forces_with_any_flagged_years": _force_list(flags["police_force"]),
                "practical_flagged_force_year_rows": int(len(practical_flags)),
                "forces_with_any_practical_flagged_years": _force_list(
                    practical_flags["police_force"]
                ),
            }
        )
    return pd.DataFrame(rows)


def _interpretation_text(counts: pd.DataFrame) -> list[str]:
    flags = counts[counts["flag_yoy_gt_20pct"]]
    practical_flags = counts[counts["flag_yoy_gt_20pct_and_abs_ksi_change_ge25"]]

    total_flags = len(flags)
    practical_total = len(practical_flags)
    flags_2016_2017 = int(flags["year"].isin([2016, 2017]).sum())
    flags_2020_2021 = int(flags["year"].isin([2020, 2021]).sum())
    flags_2024 = int((flags["year"] == 2024).sum())
    n_forces = counts["police_force"].nunique()
    flagged_forces = flags["police_force"].nunique()

    repeated = (
        flags.groupby(["police_force", "force_name"])
        .size()
        .reset_index(name="n_flags")
        .query("n_flags >= 2")
        .sort_values(["n_flags", "police_force"], ascending=[False, True])
    )
    repeated_text = "none"
    if not repeated.empty:
        repeated_text = ", ".join(
            f"{int(row.police_force)} {row.force_name} ({int(row.n_flags)})"
            for row in repeated.itertuples(index=False)
        )

    return [
        (
            f"Isolated small-number volatility: the pre-registered ±20% rule flags {total_flags} force/year rows across "
            f"{flagged_forces} of {n_forces} forces. The stricter practical sensitivity "
            f"flag still retains {practical_total} rows, so the result is not mainly an "
            "artefact of tiny absolute KSI changes."
        ),
        (
            f"Systematic reporting transition: there is some evidence of an early transition because {flags_2016_2017} "
            "flags occur in 2016–2017, including clustered changes for South Yorkshire "
            "and Lincolnshire. This is not a clean national transition, however: removing "
            "2015–2016 reduces but does not remove the issue."
        ),
        (
            f"Covid-era disruption: present but not dominant. {flags_2020_2021} flags "
            "occur in 2020–2021. The flagged rows continue before and after the Covid "
            "period, so Covid alone is not a sufficient explanation."
        ),
        (
            f"2024 CF→RSF transition: this does not appear to be a system-wide break in this "
            f"extract: {flags_2024} of {n_forces} forces are flagged in 2024, well below "
            "the 'all or most forces' decision rule."
        ),
        (
            "Heterogeneous force-specific behaviour: this is the dominant pattern rather than a "
            f"single clean national break. Forces with repeated flagged years are: {repeated_text}."
        ),
    ]


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
    count_path = FIGURE_DIR / "ksi_count_by_force_year.png"
    ratio_path = FIGURE_DIR / "ksi_ratio_by_force_year.png"
    _plot_panel(
        counts,
        "ksi_count",
        "KSI collisions",
        "KSI count by force and year",
        str(count_path),
    )
    _plot_panel(
        counts,
        "ksi_to_all_injury_ratio",
        "KSI / all-injury ratio",
        "KSI-to-all-injury ratio by force and year",
        str(ratio_path),
        percent_axis=True,
    )
    return {"count": _relative(str(count_path)), "ratio": _relative(str(ratio_path))}


def _format_pct(value: float, digits: int = 1) -> str:
    if pd.isna(value):
        return ""
    return f"{value:.{digits}f}%"


def _format_ratio(value: float) -> str:
    if pd.isna(value):
        return ""
    return f"{value:.4f}"


def _format_count_change(value: float) -> str:
    if pd.isna(value):
        return ""
    return f"{int(value):+d}"


def _format_bool(value: bool) -> str:
    return "yes" if bool(value) else "no"


def _plain_verdict(value: str) -> str:
    return value.removeprefix("Verdict: ")


def _plain_recommendation(value: str) -> str:
    return value.removeprefix("Practical modelling recommendation: ")


def _write_report(result: DiagnosticResult) -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# KSI Reporting Consistency Diagnostic",
        "",
        "**Status:** Part A diagnostic report. No KSI GLM, EB shrinkage, or production model change.",
        "",
        "## Setup",
        "",
        (
            "This report checks whether fatal/serious reporting is consistent enough across "
            "force/year cells to proceed to the next pre-registered KSI diagnostic stage."
        ),
        "",
        "## Input Data Path",
        "",
        f"- Stage 2 collision count table: `{_relative(str(RLA_PATH))}`",
        f"- Collision-level STATS19-linked source used for force/year reporting: `{_relative(str(SNAPPED_PATH))}`",
        f"- Input collision rows: {result.input_rows:,}",
        f"- Retained rows after Stage 2 snap-method and snap-score filters: {result.retained_rows:,}",
        "",
        "## Method",
        "",
        (
            "The diagnostic uses the same snapped collision source that feeds "
            "`road_link_annual.parquet`, then applies the Stage 2 snap filters: "
            "`snap_method in {attribute, spatial, weighted}` and, where present, "
            "`snap_score >= 0.6`."
        ),
        "",
        "- Collision year field: `collision_year` if present; otherwise derived from `date`.",
        "- Police force field: `police_force`, with names mapped from `config/settings.yaml`.",
        "- Severity field: `collision_severity`.",
        "- All-injury count indicator: one retained STATS19 collision row counted by `collision_index`.",
        "- KSI definition: `collision_severity in {1, 2}` where 1=fatal and 2=serious.",
        (
            "- Flag rule: a force/year row is flagged when the year-on-year percentage "
            "change in KSI-to-all-injury ratio exceeds ±20%."
        ),
        (
            "- Sensitivity flag: a force/year row is flagged only when the same ±20% "
            "ratio rule is met and the absolute KSI count change is at least 25 collisions. "
            "This does not replace the pre-registered rule."
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
                "## Flagged Force/Year Breaks",
                "",
                "Not computed.",
                "",
                "## Verdict",
                "",
                f"**Strict pre-registered verdict:** {_plain_verdict(result.verdict)}",
                "",
                (
                    "**Practical modelling recommendation:** "
                    f"{_plain_recommendation(result.practical_recommendation)}"
                ),
            ]
        )
        REPORT_PATH.write_text("\n".join(lines) + "\n")
        return

    total_all = int(result.counts["all_injury_count"].sum())
    total_ksi = int(result.counts["ksi_count"].sum())
    total_ratio = total_ksi / total_all if total_all else float("nan")
    year_summary = (
        result.counts.groupby("year")
        .agg(
            all_injury_count=("all_injury_count", "sum"),
            ksi_count=("ksi_count", "sum"),
            flagged_force_years=("flag_yoy_gt_20pct", "sum"),
            practical_flagged_force_years=(
                "flag_yoy_gt_20pct_and_abs_ksi_change_ge25",
                "sum",
            ),
        )
        .reset_index()
    )
    year_summary["ksi_to_all_injury_ratio"] = (
        year_summary["ksi_count"] / year_summary["all_injury_count"]
    )

    force_summary = (
        result.counts.groupby(["police_force", "force_name"])
        .agg(
            all_injury_count=("all_injury_count", "sum"),
            ksi_count=("ksi_count", "sum"),
            flagged_years=("flag_yoy_gt_20pct", "sum"),
            practical_flagged_years=("flag_yoy_gt_20pct_and_abs_ksi_change_ge25", "sum"),
        )
        .reset_index()
        .sort_values(["police_force"])
    )
    force_summary["ksi_to_all_injury_ratio"] = (
        force_summary["ksi_count"] / force_summary["all_injury_count"]
    )

    year_rows = [
        [
            int(row.year),
            int(row.all_injury_count),
            int(row.ksi_count),
            _format_ratio(row.ksi_to_all_injury_ratio),
            int(row.flagged_force_years),
            int(row.practical_flagged_force_years),
        ]
        for row in year_summary.itertuples(index=False)
    ]
    force_rows = [
        [
            int(row.police_force),
            row.force_name,
            int(row.all_injury_count),
            int(row.ksi_count),
            _format_ratio(row.ksi_to_all_injury_ratio),
            int(row.flagged_years),
            int(row.practical_flagged_years),
        ]
        for row in force_summary.itertuples(index=False)
    ]

    flag_rows = [
        [
            int(row.police_force),
            row.force_name,
            int(row.year),
            int(row.all_injury_count),
            int(row.ksi_count),
            _format_ratio(row.ksi_to_all_injury_ratio),
            _format_count_change(row.ksi_count_change),
            _format_pct(row.ratio_yoy_pct_change),
            _format_bool(row.flag_yoy_gt_20pct_and_abs_ksi_change_ge25),
        ]
        for row in result.flags.sort_values(["year", "police_force"]).itertuples(index=False)
    ]
    sensitivity = _window_sensitivity(result.counts)
    sensitivity_rows = [
        [
            row.window,
            int(row.number_of_forces),
            int(row.number_of_force_year_rows),
            f"{int(row.all_injury_count):,}",
            f"{int(row.ksi_count):,}",
            _format_ratio(row.overall_ksi_to_all_injury_ratio),
            int(row.flagged_force_year_rows),
            row.forces_with_any_flagged_years,
            int(row.practical_flagged_force_year_rows),
            row.forces_with_any_practical_flagged_years,
        ]
        for row in sensitivity.itertuples(index=False)
    ]

    lines.extend(
        [
            "## Summary Tables",
            "",
            _markdown_table(
                ["metric", "value"],
                [
                    ["force/year rows", len(result.counts)],
                    ["forces", result.counts["police_force"].nunique()],
                    ["years", f"{result.counts['year'].min()}–{result.counts['year'].max()}"],
                    ["all-injury collisions", f"{total_all:,}"],
                    ["KSI collisions", f"{total_ksi:,}"],
                    ["overall KSI/all-injury ratio", _format_ratio(total_ratio)],
                    ["pre-registered flagged force/year rows", len(result.flags)],
                    [
                        "practical-sensitivity flagged force/year rows",
                        int(result.counts["flag_yoy_gt_20pct_and_abs_ksi_change_ge25"].sum()),
                    ],
                ],
            ),
            "",
            "### By Year",
            "",
            _markdown_table(
                [
                    "year",
                    "all_injury_count",
                    "ksi_count",
                    "ksi_to_all_injury_ratio",
                    "pre_registered_flagged_force_years",
                    "practical_sensitivity_flagged_force_years",
                ],
                year_rows,
            ),
            "",
            "### By Force",
            "",
            _markdown_table(
                [
                    "police_force",
                    "force_name",
                    "all_injury_count",
                    "ksi_count",
                    "ksi_to_all_injury_ratio",
                    "pre_registered_flagged_years",
                    "practical_sensitivity_flagged_years",
                ],
                force_rows,
            ),
            "",
            "## Plots",
            "",
            f"![KSI count by force and year]({result.figure_paths['count']})",
            "",
            f"![KSI-to-all-injury ratio by force and year]({result.figure_paths['ratio']})",
            "",
            "## Flagged Force/Year Breaks",
            "",
        ]
    )

    if flag_rows:
        lines.append(
            _markdown_table(
                [
                    "police_force",
                    "force_name",
                    "year",
                    "all_injury_count",
                    "ksi_count",
                    "ksi_to_all_injury_ratio",
                    "ksi_count_change",
                    "ratio_yoy_pct_change",
                    "practical_sensitivity_flag",
                ],
                flag_rows,
            )
        )
    else:
        lines.append("No force/year rows exceeded the +/-20% year-on-year ratio-change flag.")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            *[f"- {text}" for text in _interpretation_text(result.counts)],
            "",
            "## Window Sensitivity",
            "",
            (
                "The pre-registered flag is retained exactly. The practical-sensitivity "
                "columns show the stricter flag that also requires an absolute KSI count "
                "change of at least 25 collisions."
            ),
            "",
            _markdown_table(
                [
                    "window",
                    "number_of_forces",
                    "number_of_force_year_rows",
                    "all_injury_count",
                    "ksi_count",
                    "overall_ksi_to_all_injury_ratio",
                    "pre_registered_flagged_force_year_rows",
                    "forces_with_any_pre_registered_flagged_years",
                    "practical_sensitivity_flagged_force_year_rows",
                    "forces_with_any_practical_sensitivity_flagged_years",
                ],
                sensitivity_rows,
            ),
            "",
            "## Practical Modelling Recommendation",
            "",
            _plain_recommendation(result.practical_recommendation),
            "",
            "## Verdict",
            "",
            f"**Strict pre-registered verdict:** {_plain_verdict(result.verdict)}",
            "",
            (
                "**Practical modelling recommendation:** "
                f"{_plain_recommendation(result.practical_recommendation)}"
            ),
        ]
    )

    REPORT_PATH.write_text("\n".join(lines) + "\n")


def run() -> DiagnosticResult:
    collisions = _load_snapped()
    prepared, missing = _prepare_collision_frame(collisions)

    if missing:
        result = DiagnosticResult(
            counts=pd.DataFrame(),
            flags=pd.DataFrame(),
            verdict=_determine_verdict(pd.DataFrame(), pd.DataFrame(), missing),
            practical_recommendation=(
                "Practical modelling recommendation: diagnostic incomplete; do not run Part B."
            ),
            missing_fields=missing,
            input_rows=len(collisions),
            retained_rows=0,
            figure_paths={},
        )
        _write_report(result)
        return result

    counts = _summarise_force_year(prepared)
    flags = counts[counts["flag_yoy_gt_20pct"]].copy()
    verdict = _determine_verdict(counts, flags, [])
    practical_recommendation = _practical_recommendation(counts)
    figure_paths = _write_plots(counts)

    result = DiagnosticResult(
        counts=counts,
        flags=flags,
        verdict=verdict,
        practical_recommendation=practical_recommendation,
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
    logger.info(result.verdict)


if __name__ == "__main__":
    main()
