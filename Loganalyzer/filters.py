from datetime import datetime
from typing import Generator, Optional

from .exceptions import (
    InvalidDateFormatError,
    InvalidLogLevelError,
)

VALID_LEVELS = {
    "ALL",
    "INFO",
    "WARN",
    "ERROR",
}


def filter_entries(
    entries: Generator[dict, None, None],
    level: str = "ALL",
    from_dt: Optional[datetime] = None,
    to_dt: Optional[datetime] = None,
) -> Generator[dict, None, None]:

    if level not in VALID_LEVELS:

        raise InvalidLogLevelError(
            f"Invalid log level: {level}"
        )

    if (
        from_dt
        and to_dt
        and from_dt > to_dt
    ):

        raise InvalidDateFormatError(
            "--from must be earlier than --to"
        )

    for entry in entries:

        if (
            level != "ALL"
            and entry["level"] != level
        ):
            continue

        if (
            from_dt
            and entry["timestamp"] < from_dt
        ):
            continue

        if (
            to_dt
            and entry["timestamp"] > to_dt
        ):
            continue

        yield entry