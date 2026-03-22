from abc import ABC, abstractmethod
from collections import defaultdict
from statistics import median
from typing import TypeVar

from models import CoffeeRecord

T = TypeVar("T")


class BaseReport[T](ABC):
    """
    Abstract base class for report generators.

    Subclasses must implement 'generate' to transform input data
    into a list of dictionaries suitable for display.
    """

    @abstractmethod
    def generate(self, data: list[T]) -> list[dict]:
        pass


class MedianCoffeeReport(BaseReport[CoffeeRecord]):
    """Report that computes the median coffee spending per student."""

    def generate(self, data: list[CoffeeRecord]) -> list[dict]:
        totals = defaultdict(list)

        for row in data:
            totals[row.student].append(row.coffee_spent)

        result = [
            {"student": student, "median_coffee": median(values)}
            for student, values in totals.items()
        ]

        return sorted(result, key=lambda row: row["median_coffee"], reverse=True)
