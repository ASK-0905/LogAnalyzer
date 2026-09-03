import argparse
import functools
import time
from datetime import datetime
from typing import Any, Callable

from .exceptions import LogAnalyzerError
from .filters import filter_entries
from .parser import read_log_file
from .report import format_report


def timer(func: Callable) -> Callable:

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:

        start = time.perf_counter()

        result = func(*args, **kwargs)

        end = time.perf_counter()

        print(
            f"\n[timer] "
            f"{func.__name__} "
            f"completed in "
            f"{end-start:.4f} seconds"
        )

        return result

    return wrapper


def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(
        description="Log Analyzer CLI"
    )

    parser.add_argument(
        "--file",
        required=True,
    )

    parser.add_argument(
        "--level",
        default="ALL",
        choices=[
            "ALL",
            "INFO",
            "WARN",
            "ERROR",
        ],
    )

    parser.add_argument(
        "--from",
        dest="from_dt",
    )

    parser.add_argument(
        "--to",
        dest="to_dt",
    )

    parser.add_argument(
        "--format",
        dest="fmt",
        default="text",
        choices=[
            "text",
            "json",
        ],
    )

    return parser.parse_args()


def validate_args(
    args: argparse.Namespace,
) -> None:

    fmt = "%Y-%m-%d %H:%M:%S"

    if args.from_dt:

        args.from_dt = datetime.strptime(
            args.from_dt,
            fmt,
        )

    if args.to_dt:

        args.to_dt = datetime.strptime(
            args.to_dt,
            fmt,
        )


@timer
def run_analysis(
    args: argparse.Namespace,
) -> None:

    entries = read_log_file(
        args.file
    )

    filtered = filter_entries(
        entries,
        args.level,
        args.from_dt,
        args.to_dt,
    )

    report = format_report(
        filtered,
        args.fmt,
    )

    print(report)


def main() -> None:

    args = parse_args()

    try:

        validate_args(args)

        run_analysis(args)

    except ValueError:

        print(
            "Invalid date format.\n"
            "Use YYYY-MM-DD HH:MM:SS"
        )

    except LogAnalyzerError as error:

        print(error)