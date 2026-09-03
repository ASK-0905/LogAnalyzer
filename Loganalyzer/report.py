import json
from typing import Generator


def format_report(
    entries: Generator[dict, None, None],
    fmt: str = "text",
) -> str:

    results = list(entries)

    if not results:

        return "No log entries found matching the filters."

    if fmt == "json":

        return json.dumps(

            [
                {
                    "timestamp": item[
                        "timestamp"
                    ].isoformat(),

                    "level": item["level"],

                    "message": item["message"],
                }

                for item in results

            ],

            indent=4,

        )

    report = []

    report.append("=" * 60)

    report.append("LOG ANALYZER REPORT")

    report.append("=" * 60)

    for item in results:

        report.append(
            f"[{item['level']}] "
            f"{item['timestamp']} "
            f"{item['message']}"
        )

    report.append("")

    report.append(
        f"Total Entries : {len(results)}"
    )

    return "\n".join(report)