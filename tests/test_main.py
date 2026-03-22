import pytest

from main import REPORTS, generate_report, get_report, load_csvs, validate_paths
from models import CoffeeRecord


def test_validate_paths(tmp_path):
    file1 = tmp_path / "history.csv"
    file2 = tmp_path / "chemistry.csv"

    file1.touch()
    file2.touch()

    paths = [str(file1), str(file2)]

    validated = validate_paths(paths)

    assert validated == [file1, file2]


@pytest.mark.parametrize(
    "filename, should_exist, expected_exception",
    [
        ("nonexistent.csv", False, FileNotFoundError),
        ("wrong_suffix.txt", True, ValueError),
    ],
)
def test_validate_paths_errors(tmp_path, filename, should_exist, expected_exception):
    file = tmp_path / filename

    if should_exist:
        file.write_text("data")

    with pytest.raises(expected_exception):
        validate_paths([str(file)])


def test_load_csvs(tmp_path):
    file1 = tmp_path / "history.csv"
    file1.write_text("student,coffee_spent\nПавел Новиков,300\n")

    file2 = tmp_path / "chemistry.csv"
    file2.write_text("student,coffee_spent\nЕлена Волкова,250\n")

    result = load_csvs([file1, file2])

    assert result == [
        CoffeeRecord(student="Павел Новиков", coffee_spent=300),
        CoffeeRecord(student="Елена Волкова", coffee_spent=250),
    ]


@pytest.mark.parametrize("report_name, expected_class", list(REPORTS.items()))
def test_get_report(report_name, expected_class):
    report = get_report(report_name)
    assert isinstance(report, expected_class)


def test_get_report_nonexistent_report():
    with pytest.raises(ValueError, match="Unknown report") as exc_info:
        get_report("median-sleep-key-error")

    assert isinstance(exc_info.value.__cause__, KeyError)


def test_generate_report(tmp_path):
    file = tmp_path / "history.csv"
    file.write_text(
        "student,coffee_spent\nПавел Новиков,300\nПавел Новиков,350\nЕлена Волкова,250\n"
    )

    result = generate_report([str(file)], "median-coffee")

    assert result == [
        {"student": "Павел Новиков", "median_coffee": 325},
        {"student": "Елена Волкова", "median_coffee": 250},
    ]


def test_generate_report_empty(tmp_path):
    file = tmp_path / "empty.csv"
    file.write_text("student,coffee_spent\n")

    result = generate_report([str(file)], "median-coffee")

    assert result == []
