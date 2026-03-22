from report_types import MedianCoffeeReport
from models import CoffeeRecord


def test_median_report():
    data = [
        CoffeeRecord("Павел Новиков", 300),
        CoffeeRecord("Павел Новиков", 350),
        CoffeeRecord("Елена Волкова", 250),
    ]

    report = MedianCoffeeReport()
    result = report.generate(data)

    assert result == [
        {"student": "Павел Новиков", "median_coffee": 325},
        {"student": "Елена Волкова", "median_coffee": 250},
    ]
