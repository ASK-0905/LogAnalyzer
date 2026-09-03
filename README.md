# Log Analyzer CLI

A command-line tool for analyzing server log files.

---

## Features

- Read large log files using generators
- Filter by log level
- Filter by date range
- JSON Output
- Text Output
- Timer Decorator
- Custom Exceptions
- argparse CLI
- Type Hints

---

## Installation

pip install -r requirements.txt

---

## Usage

python main.py --file sample.log

python main.py --file sample.log --level ERROR

python main.py --file sample.log --format json

python main.py --file sample.log --from "2024-06-10 08:10:00"

python main.py --help

---

## Package Structure

log_analyzer/

parser.py

filters.py

report.py

exceptions.py

cli.py