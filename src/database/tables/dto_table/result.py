# THIS CLASS WAS GENERATE WITH generate_database_classes.py
# ANYTHING YOU ADD HERE MAY BE OVERWRITTEN IN THE FUTURE
from typing import Type

from src.database.tables.table import Comparator, Table
from src.models.dto.result import Result


class ResultTable(Table[Result]):
    @classmethod
    def get_create_table_script(cls) -> str:
        return """CREATE TABLE IF NOT EXISTS results (
    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Sex TEXT NOT NULL,
    Age REAL NOT NULL,
    BodyweightKg REAL NOT NULL,
    Best3SquatKg REAL NOT NULL,
    Best3BenchKg REAL NOT NULL,
    Best3DeadliftKg REAL NOT NULL,
    TotalKg REAL NOT NULL,
    Wilks REAL NOT NULL,
    Dots REAL NOT NULL,
    Federation TEXT NOT NULL,
    Sanctioned TEXT NOT NULL,
    Place TEXT NOT NULL,
    Date TEXT NOT NULL,
    Tested TEXT NOT NULL
);"""

    @classmethod
    def get_table_name(cls) -> str:
        return "results"

    @classmethod
    def get_model_class(cls) -> Type[Result]:
        return Result

    def get_by_name(self, value: str) -> list[Result]:
        return self.get_all_from_attribute("Name", value)

    def get_where_name_ge(self, value: str) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Name", Comparator.GE, value),))

    def get_where_name_le(self, value: str) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Name", Comparator.LE, value),))

    def get_where_name_in_range(self, lower_inclusive: str, upper_inclusive: str) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Name", Comparator.GE, lower_inclusive), ("Name", Comparator.LE, upper_inclusive)))

    def get_by_sex(self, value: str) -> list[Result]:
        return self.get_all_from_attribute("Sex", value)

    def get_where_sex_ge(self, value: str) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Sex", Comparator.GE, value),))

    def get_where_sex_le(self, value: str) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Sex", Comparator.LE, value),))

    def get_where_sex_in_range(self, lower_inclusive: str, upper_inclusive: str) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Sex", Comparator.GE, lower_inclusive), ("Sex", Comparator.LE, upper_inclusive)))

    def get_by_age(self, value: float) -> list[Result]:
        return self.get_all_from_attribute("Age", value)

    def get_where_age_ge(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Age", Comparator.GE, value),))

    def get_where_age_le(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Age", Comparator.LE, value),))

    def get_where_age_in_range(self, lower_inclusive: float, upper_inclusive: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Age", Comparator.GE, lower_inclusive), ("Age", Comparator.LE, upper_inclusive)))

    def get_by_bodyweight_kg(self, value: float) -> list[Result]:
        return self.get_all_from_attribute("BodyweightKg", value)

    def get_where_bodyweight_kg_ge(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("BodyweightKg", Comparator.GE, value),))

    def get_where_bodyweight_kg_le(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("BodyweightKg", Comparator.LE, value),))

    def get_where_bodyweight_kg_in_range(self, lower_inclusive: float, upper_inclusive: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("BodyweightKg", Comparator.GE, lower_inclusive), ("BodyweightKg", Comparator.LE, upper_inclusive)))

    def get_by_best3_squat_kg(self, value: float) -> list[Result]:
        return self.get_all_from_attribute("Best3SquatKg", value)

    def get_where_best3_squat_kg_ge(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Best3SquatKg", Comparator.GE, value),))

    def get_where_best3_squat_kg_le(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Best3SquatKg", Comparator.LE, value),))

    def get_where_best3_squat_kg_in_range(self, lower_inclusive: float, upper_inclusive: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Best3SquatKg", Comparator.GE, lower_inclusive), ("Best3SquatKg", Comparator.LE, upper_inclusive)))

    def get_by_best3_bench_kg(self, value: float) -> list[Result]:
        return self.get_all_from_attribute("Best3BenchKg", value)

    def get_where_best3_bench_kg_ge(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Best3BenchKg", Comparator.GE, value),))

    def get_where_best3_bench_kg_le(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Best3BenchKg", Comparator.LE, value),))

    def get_where_best3_bench_kg_in_range(self, lower_inclusive: float, upper_inclusive: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Best3BenchKg", Comparator.GE, lower_inclusive), ("Best3BenchKg", Comparator.LE, upper_inclusive)))

    def get_by_best3_deadlift_kg(self, value: float) -> list[Result]:
        return self.get_all_from_attribute("Best3DeadliftKg", value)

    def get_where_best3_deadlift_kg_ge(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Best3DeadliftKg", Comparator.GE, value),))

    def get_where_best3_deadlift_kg_le(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Best3DeadliftKg", Comparator.LE, value),))

    def get_where_best3_deadlift_kg_in_range(self, lower_inclusive: float, upper_inclusive: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Best3DeadliftKg", Comparator.GE, lower_inclusive), ("Best3DeadliftKg", Comparator.LE, upper_inclusive)))

    def get_by_total_kg(self, value: float) -> list[Result]:
        return self.get_all_from_attribute("TotalKg", value)

    def get_where_total_kg_ge(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("TotalKg", Comparator.GE, value),))

    def get_where_total_kg_le(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("TotalKg", Comparator.LE, value),))

    def get_where_total_kg_in_range(self, lower_inclusive: float, upper_inclusive: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("TotalKg", Comparator.GE, lower_inclusive), ("TotalKg", Comparator.LE, upper_inclusive)))

    def get_by_wilks(self, value: float) -> list[Result]:
        return self.get_all_from_attribute("Wilks", value)

    def get_where_wilks_ge(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Wilks", Comparator.GE, value),))

    def get_where_wilks_le(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Wilks", Comparator.LE, value),))

    def get_where_wilks_in_range(self, lower_inclusive: float, upper_inclusive: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Wilks", Comparator.GE, lower_inclusive), ("Wilks", Comparator.LE, upper_inclusive)))

    def get_by_dots(self, value: float) -> list[Result]:
        return self.get_all_from_attribute("Dots", value)

    def get_where_dots_ge(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Dots", Comparator.GE, value),))

    def get_where_dots_le(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Dots", Comparator.LE, value),))

    def get_where_dots_in_range(self, lower_inclusive: float, upper_inclusive: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Dots", Comparator.GE, lower_inclusive), ("Dots", Comparator.LE, upper_inclusive)))

    def get_by_federation(self, value: str) -> list[Result]:
        return self.get_all_from_attribute("Federation", value)

    def get_where_federation_ge(self, value: str) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Federation", Comparator.GE, value),))

    def get_where_federation_le(self, value: str) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Federation", Comparator.LE, value),))

    def get_where_federation_in_range(self, lower_inclusive: str, upper_inclusive: str) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Federation", Comparator.GE, lower_inclusive), ("Federation", Comparator.LE, upper_inclusive)))

    def get_by_sanctioned(self, value: str) -> list[Result]:
        return self.get_all_from_attribute("Sanctioned", value)

    def get_where_sanctioned_ge(self, value: str) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Sanctioned", Comparator.GE, value),))

    def get_where_sanctioned_le(self, value: str) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Sanctioned", Comparator.LE, value),))

    def get_where_sanctioned_in_range(self, lower_inclusive: str, upper_inclusive: str) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Sanctioned", Comparator.GE, lower_inclusive), ("Sanctioned", Comparator.LE, upper_inclusive)))

    def get_by_place(self, value: str) -> list[Result]:
        return self.get_all_from_attribute("Place", value)

    def get_where_place_ge(self, value: str) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Place", Comparator.GE, value),))

    def get_where_place_le(self, value: str) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Place", Comparator.LE, value),))

    def get_where_place_in_range(self, lower_inclusive: str, upper_inclusive: str) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Place", Comparator.GE, lower_inclusive), ("Place", Comparator.LE, upper_inclusive)))

    def get_by_date(self, value: str) -> list[Result]:
        return self.get_all_from_attribute("Date", value)

    def get_where_date_ge(self, value: str) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Date", Comparator.GE, value),))

    def get_where_date_le(self, value: str) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Date", Comparator.LE, value),))

    def get_where_date_in_range(self, lower_inclusive: str, upper_inclusive: str) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Date", Comparator.GE, lower_inclusive), ("Date", Comparator.LE, upper_inclusive)))

    def get_by_tested(self, value: str) -> list[Result]:
        return self.get_all_from_attribute("Tested", value)

    def get_where_tested_ge(self, value: str) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Tested", Comparator.GE, value),))

    def get_where_tested_le(self, value: str) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Tested", Comparator.LE, value),))

    def get_where_tested_in_range(self, lower_inclusive: str, upper_inclusive: str) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Tested", Comparator.GE, lower_inclusive), ("Tested", Comparator.LE, upper_inclusive)))

    def get_by_unique_result_id(self, value: int) -> Result | None:
        results = self.get_all_from_attribute("result_id", value)
        if not results:
            return None
        if len(results) > 1:
            raise ValueError("Multiple results returned for unique query")
        return results[0]
