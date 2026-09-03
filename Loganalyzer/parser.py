import os
from datetime import datetime
from typing import Generator

from .exceptions import (
    LogFileNotFoundError,
    MalformedLineError,
)

LOG_LEVELS = {"INFO", "WARN", "ERROR"}


def parse_line(line: str) -> dict:

    parts = line.split(" ", 3)

    if len(parts) < 4:
        raise MalformedLineError(
            f"Malformed line: {line}"
        )

    date_str, time_str, level, message = parts

    if level not in LOG_LEVELS:
        raise MalformedLineError(
            f"Unknown log level: {level}"
        )

    try:

        timestamp = datetime.strptime(
            f"{date_str} {time_str}",
            "%Y-%m-%d %H:%M:%S"
        )

    except ValueError:

        raise MalformedLineError(
            f"Invalid timestamp: {date_str} {time_str}"
        )

    return {
        "timestamp": timestamp,
        "level": level,
        "message": message,
    }


def read_log_file(
    file_path: str,
    max_errors: int = 10,
) -> Generator[dict, None, None]:

    if os.path.isdir(file_path):
        raise LogFileNotFoundError(
            f"{file_path} is a directory."
        )

    if not os.path.isfile(file_path):
        raise LogFileNotFoundError(
            f"File not found: {file_path}"
        )

    error_count = 0

    with open(file_path, "r", encoding="utf-8") as file:

        for line_number, line in enumerate(file, start=1):

            line = line.strip()

            if not line:
                continue

            try:

                yield parse_line(line)

            except MalformedLineError as error:

                error_count += 1

                print(
                    f"Warning (Line {line_number}): {error}"
                )

                if error_count > max_errors:

                    raise MalformedLineError(
                        f"Too many malformed lines (> {max_errors})"
                    )