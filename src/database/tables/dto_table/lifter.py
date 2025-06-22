# THIS CLASS WAS GENERATE WITH generate_database_classes.py
# ANYTHING YOU ADD HERE MAY BE OVERWRITTEN IN THE FUTURE
from typing import Type

from src.database.tables.table import Comparator, Table
from src.models.dto.lifter import Lifter


class LifterTable(Table[Lifter]):
    @classmethod
    def get_create_table_script(cls) -> str:
        return """CREATE TABLE IF NOT EXISTS lifters (
    lifter_id INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL UNIQUE,
    Sex TEXT NOT NULL,
    Country TEXT,
    State TEXT
);"""

    @classmethod
    def get_table_name(cls) -> str:
        return "lifters"

    @classmethod
    def get_model_class(cls) -> Type[Lifter]:
        return Lifter

    def get_by_sex(self, value: str) -> list[Lifter]:
        return self.get_all_from_attribute("Sex", value)

    def get_where_sex_ge(self, value: str) -> list[Lifter]:
        return self.get_all_from_attributes_with_comparator(
            (("Sex", Comparator.GE, value),)
        )

    def get_where_sex_le(self, value: str) -> list[Lifter]:
        return self.get_all_from_attributes_with_comparator(
            (("Sex", Comparator.LE, value),)
        )

    def get_where_sex_in_range(
        self, lower_inclusive: str, upper_inclusive: str
    ) -> list[Lifter]:
        return self.get_all_from_attributes_with_comparator(
            (
                ("Sex", Comparator.GE, lower_inclusive),
                ("Sex", Comparator.LE, upper_inclusive),
            )
        )

    def get_by_country(self, value: str) -> list[Lifter]:
        return self.get_all_from_attribute("Country", value)

    def get_where_country_ge(self, value: str) -> list[Lifter]:
        return self.get_all_from_attributes_with_comparator(
            (("Country", Comparator.GE, value),)
        )

    def get_where_country_le(self, value: str) -> list[Lifter]:
        return self.get_all_from_attributes_with_comparator(
            (("Country", Comparator.LE, value),)
        )

    def get_where_country_in_range(
        self, lower_inclusive: str, upper_inclusive: str
    ) -> list[Lifter]:
        return self.get_all_from_attributes_with_comparator(
            (
                ("Country", Comparator.GE, lower_inclusive),
                ("Country", Comparator.LE, upper_inclusive),
            )
        )

    def get_by_state(self, value: str) -> list[Lifter]:
        return self.get_all_from_attribute("State", value)

    def get_where_state_ge(self, value: str) -> list[Lifter]:
        return self.get_all_from_attributes_with_comparator(
            (("State", Comparator.GE, value),)
        )

    def get_where_state_le(self, value: str) -> list[Lifter]:
        return self.get_all_from_attributes_with_comparator(
            (("State", Comparator.LE, value),)
        )

    def get_where_state_in_range(
        self, lower_inclusive: str, upper_inclusive: str
    ) -> list[Lifter]:
        return self.get_all_from_attributes_with_comparator(
            (
                ("State", Comparator.GE, lower_inclusive),
                ("State", Comparator.LE, upper_inclusive),
            )
        )

    def get_by_unique_lifter_id(self, value: int) -> Lifter | None:
        results = self.get_all_from_attribute("lifter_id", value)
        if not results:
            return None
        if len(results) > 1:
            raise ValueError("Multiple results returned for unique query")
        return results[0]

    def get_by_unique_name(self, value: str) -> Lifter | None:
        results = self.get_all_from_attribute("Name", value)
        if not results:
            return None
        if len(results) > 1:
            raise ValueError("Multiple results returned for unique query")
        return results[0]
