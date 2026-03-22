import csv
from argparse import ArgumentParser
from pathlib import Path

from tabulate import tabulate

from models import CoffeeRecord
from report_types import BaseReport, MedianCoffeeReport

REPORTS: dict[str, type[BaseReport]] = {
    "median-coffee": MedianCoffeeReport,
}


def validate_paths(paths: list[str]) -> list[Path]:
    validated = []
    for p in paths:
        path = Path(p)

        if path.suffix.lower() != ".csv":
            raise ValueError(f"{p} is not a .csv file")

        if not path.exists():
            raise FileNotFoundError(f"{p} does not exist")

        validated.append(path)

    return validated


def load_csvs(paths: list[Path]) -> list[CoffeeRecord]:
    records: list[CoffeeRecord] = []

    for path in paths:
        with path.open("r", encoding="utf-8") as f:
            reader: csv.DictReader = csv.DictReader(f)

            records.extend(
                CoffeeRecord(
                    student=row["student"], coffee_spent=int(row["coffee_spent"])
                )
                for row in reader
            )

    return records


def get_report(report_name: str):
    try:
        return REPORTS[report_name]()
    except KeyError as err:
        raise ValueError(f"Unknown report: {report_name}") from err


def generate_report(paths, report_name):
    paths = validate_paths(paths)
    data = load_csvs(paths)

    report = get_report(report_name)
    return report.generate(data)


def main():
    parser = ArgumentParser(description="Make a report from csv files")
    parser.add_argument("--files", nargs="+", required=True)
    parser.add_argument("--report", required=True, choices=REPORTS.keys())

    args = parser.parse_args()
    generated_report = generate_report(args.files, args.report)
    print(tabulate(generated_report, headers="keys", floatfmt=".2f", tablefmt="grid"))


if __name__ == "__main__":
    main()
