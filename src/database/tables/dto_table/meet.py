# THIS CLASS WAS GENERATE WITH generate_database_classes.py
# ANYTHING YOU ADD HERE MAY BE OVERWRITTEN IN THE FUTURE
from typing import Type

from src.database.tables.table import Comparator, Table
from src.models.dto.meet import Meet


class MeetTable(Table[Meet]):
    @classmethod
    def get_create_table_script(cls) -> str:
        return """CREATE TABLE IF NOT EXISTS meets (
    meet_id INTEGER PRIMARY KEY AUTOINCREMENT,
    Federation TEXT NOT NULL,
    MeetCountry TEXT,
    MeetState TEXT,
    MeetName TEXT,
    Sanctioned TEXT,
    MeetType TEXT
);"""

    @classmethod
    def get_table_name(cls) -> str:
        return "meets"

    @classmethod
    def get_model_class(cls) -> Type[Meet]:
        return Meet

    def get_by_federation(self, value: str) -> list[Meet]:
        return self.get_all_from_attribute("Federation", value)

    def get_where_federation_ge(self, value: str) -> list[Meet]:
        return self.get_all_from_attributes_with_comparator((("Federation", Comparator.GE, value),))

    def get_where_federation_le(self, value: str) -> list[Meet]:
        return self.get_all_from_attributes_with_comparator((("Federation", Comparator.LE, value),))

    def get_where_federation_in_range(self, lower_inclusive: str, upper_inclusive: str) -> list[Meet]:
        return self.get_all_from_attributes_with_comparator((("Federation", Comparator.GE, lower_inclusive), ("Federation", Comparator.LE, upper_inclusive)))

    def get_by_meet_country(self, value: str) -> list[Meet]:
        return self.get_all_from_attribute("MeetCountry", value)

    def get_where_meet_country_ge(self, value: str) -> list[Meet]:
        return self.get_all_from_attributes_with_comparator((("MeetCountry", Comparator.GE, value),))

    def get_where_meet_country_le(self, value: str) -> list[Meet]:
        return self.get_all_from_attributes_with_comparator((("MeetCountry", Comparator.LE, value),))

    def get_where_meet_country_in_range(self, lower_inclusive: str, upper_inclusive: str) -> list[Meet]:
        return self.get_all_from_attributes_with_comparator((("MeetCountry", Comparator.GE, lower_inclusive), ("MeetCountry", Comparator.LE, upper_inclusive)))

    def get_by_meet_state(self, value: str) -> list[Meet]:
        return self.get_all_from_attribute("MeetState", value)

    def get_where_meet_state_ge(self, value: str) -> list[Meet]:
        return self.get_all_from_attributes_with_comparator((("MeetState", Comparator.GE, value),))

    def get_where_meet_state_le(self, value: str) -> list[Meet]:
        return self.get_all_from_attributes_with_comparator((("MeetState", Comparator.LE, value),))

    def get_where_meet_state_in_range(self, lower_inclusive: str, upper_inclusive: str) -> list[Meet]:
        return self.get_all_from_attributes_with_comparator((("MeetState", Comparator.GE, lower_inclusive), ("MeetState", Comparator.LE, upper_inclusive)))

    def get_by_meet_name(self, value: str) -> list[Meet]:
        return self.get_all_from_attribute("MeetName", value)

    def get_where_meet_name_ge(self, value: str) -> list[Meet]:
        return self.get_all_from_attributes_with_comparator((("MeetName", Comparator.GE, value),))

    def get_where_meet_name_le(self, value: str) -> list[Meet]:
        return self.get_all_from_attributes_with_comparator((("MeetName", Comparator.LE, value),))

    def get_where_meet_name_in_range(self, lower_inclusive: str, upper_inclusive: str) -> list[Meet]:
        return self.get_all_from_attributes_with_comparator((("MeetName", Comparator.GE, lower_inclusive), ("MeetName", Comparator.LE, upper_inclusive)))

    def get_by_sanctioned(self, value: str) -> list[Meet]:
        return self.get_all_from_attribute("Sanctioned", value)

    def get_where_sanctioned_ge(self, value: str) -> list[Meet]:
        return self.get_all_from_attributes_with_comparator((("Sanctioned", Comparator.GE, value),))

    def get_where_sanctioned_le(self, value: str) -> list[Meet]:
        return self.get_all_from_attributes_with_comparator((("Sanctioned", Comparator.LE, value),))

    def get_where_sanctioned_in_range(self, lower_inclusive: str, upper_inclusive: str) -> list[Meet]:
        return self.get_all_from_attributes_with_comparator((("Sanctioned", Comparator.GE, lower_inclusive), ("Sanctioned", Comparator.LE, upper_inclusive)))

    def get_by_meet_type(self, value: str) -> list[Meet]:
        return self.get_all_from_attribute("MeetType", value)

    def get_where_meet_type_ge(self, value: str) -> list[Meet]:
        return self.get_all_from_attributes_with_comparator((("MeetType", Comparator.GE, value),))

    def get_where_meet_type_le(self, value: str) -> list[Meet]:
        return self.get_all_from_attributes_with_comparator((("MeetType", Comparator.LE, value),))

    def get_where_meet_type_in_range(self, lower_inclusive: str, upper_inclusive: str) -> list[Meet]:
        return self.get_all_from_attributes_with_comparator((("MeetType", Comparator.GE, lower_inclusive), ("MeetType", Comparator.LE, upper_inclusive)))

    def get_by_unique_meet_id(self, value: int) -> Meet | None:
        results = self.get_all_from_attribute("meet_id", value)
        if not results:
            return None
        if len(results) > 1:
            raise ValueError("Multiple results returned for unique query")
        return results[0]
