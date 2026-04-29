"""
Logging helpers for road_risk.

The project mostly creates module loggers with ``logging.getLogger(__name__)``.
This module centralises handler setup so entry points can send those existing
loggers to a per-run file under ``<repo>/logs``.

Typical use from a script entry point:

    from road_risk.utils.logger import configure_logging, get_logger

    configure_logging("log_run.log")
    logger = get_logger(__name__)

Or as a thin wrapper:

    from road_risk.utils.logger import RoadRiskLogger

    logger = RoadRiskLogger(__name__, filename="log_evals.log")
    logger.info("Run started")
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
LOG_DIR = _ROOT / "logs"
DEFAULT_FORMAT = "%(asctime)s  %(levelname)-8s  %(name)s  %(message)s"
DEFAULT_DATEFMT = "%Y-%m-%d %H:%M:%S"


def _coerce_level(level: int | str) -> int:
    """Return a logging level from either an int or a level name."""
    if isinstance(level, int):
        return level

    resolved = logging.getLevelName(level.upper())
    if isinstance(resolved, int):
        return resolved
    raise ValueError(f"Unknown logging level: {level!r}")


def resolve_log_path(filename: str | Path | None = None) -> Path:
    """
    Resolve a log filename/path.

    Relative paths are placed under ``_ROOT/logs``. Absolute paths are accepted
    for one-off overrides. Parent directories are created by configure_logging.
    """
    if filename is None:
        filename = "road_risk.log"

    path = Path(filename)
    if not path.is_absolute():
        path = LOG_DIR / path
    return path


def configure_logging(
    filename: str | Path | None = None,
    *,
    level: int | str = logging.INFO,
    console: bool = True,
    reset: bool = True,
    mode: str = "w",
    fmt: str = DEFAULT_FORMAT,
    datefmt: str = DEFAULT_DATEFMT,
) -> Path:
    """
    Configure root logging for a run and return the file path.

    Parameters
    ----------
    filename:
        Log filename or path. Relative paths are written under ``_ROOT/logs``.
    level:
        Logging level as ``logging.INFO`` or a string such as ``"INFO"``.
    console:
        Also emit logs to stderr.
    reset:
        Remove and close existing root handlers first. This lets a new run
        switch from one log file to another safely.
    mode:
        File open mode. Defaults to ``"w"`` so repeated runs overwrite the
        named file; use ``"a"`` to append.
    """
    log_path = resolve_log_path(filename)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    log_level = _coerce_level(level)
    root = logging.getLogger()
    root.setLevel(log_level)

    if reset:
        for handler in root.handlers[:]:
            root.removeHandler(handler)
            handler.close()

    formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)

    file_handler = logging.FileHandler(log_path, mode=mode, encoding="utf-8")
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)

    if console:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(log_level)
        stream_handler.setFormatter(formatter)
        root.addHandler(stream_handler)

    return log_path


def get_logger(
    name: str | None = None,
    *,
    filename: str | Path | None = None,
    configure: bool = False,
    level: int | str = logging.INFO,
    console: bool = True,
    reset: bool = True,
    mode: str = "w",
) -> logging.Logger:
    """
    Return a named logger, optionally configuring handlers first.

    Use ``configure=True`` at script boundaries when you want to choose the
    output file in the same call.
    """
    if configure:
        configure_logging(
            filename,
            level=level,
            console=console,
            reset=reset,
            mode=mode,
        )

    return logging.getLogger(name)


class RoadRiskLogger:
    """
    Small wrapper around ``logging.Logger`` with convenient file setup.

    It exposes common logging methods directly while preserving access to the
    underlying stdlib logger via the ``logger`` attribute.
    """

    def __init__(
        self,
        name: str | None = None,
        *,
        filename: str | Path | None = None,
        level: int | str = logging.INFO,
        console: bool = True,
        reset: bool = True,
        mode: str = "w",
    ) -> None:
        self.log_path: Path | None = None
        if filename is not None:
            self.log_path = configure_logging(
                filename,
                level=level,
                console=console,
                reset=reset,
                mode=mode,
            )
        self.logger = logging.getLogger(name or self._caller_name())

    @staticmethod
    def _caller_name() -> str:
        """Infer the importing module name for ``RoadRiskLogger()`` calls."""
        frame = sys._getframe(2)
        return str(frame.f_globals.get("__name__", "road_risk"))

    def reset_logpath(
        self,
        filename: str | Path | None = None,
        *,
        level: int | str = logging.INFO,
        console: bool = True,
        mode: str = "w",
    ) -> Path:
        """
        Reset root logging to a new file and return the resolved path.

        Because module loggers propagate to the root logger, calling this from
        one orchestrating module after imports redirects logs from all existing
        ``RoadRiskLogger()`` instances to the new file.
        """
        self.log_path = configure_logging(
            filename,
            level=level,
            console=console,
            reset=True,
            mode=mode,
        )
        return self.log_path

    def debug(self, msg: object, *args: object, **kwargs: object) -> None:
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg: object, *args: object, **kwargs: object) -> None:
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg: object, *args: object, **kwargs: object) -> None:
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg: object, *args: object, **kwargs: object) -> None:
        self.logger.error(msg, *args, **kwargs)

    def exception(self, msg: object, *args: object, **kwargs: object) -> None:
        self.logger.exception(msg, *args, **kwargs)

    def critical(self, msg: object, *args: object, **kwargs: object) -> None:
        self.logger.critical(msg, *args, **kwargs)

    def log(self, level: int, msg: object, *args: object, **kwargs: object) -> None:
        self.logger.log(level, msg, *args, **kwargs)

    def setLevel(self, level: int | str) -> None:  # noqa: N802 - mirrors logging API
        self.logger.setLevel(_coerce_level(level))

    def addHandler(self, handler: logging.Handler) -> None:  # noqa: N802
        self.logger.addHandler(handler)

    def removeHandler(self, handler: logging.Handler) -> None:  # noqa: N802
        self.logger.removeHandler(handler)

    def __getattr__(self, name: str) -> object:
        return getattr(self.logger, name)


__all__ = [
    "LOG_DIR",
    "RoadRiskLogger",
    "configure_logging",
    "get_logger",
    "logging",
    "resolve_log_path",
]
