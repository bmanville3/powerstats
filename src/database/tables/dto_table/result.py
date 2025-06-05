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
    lifter_id INTEGER NOT NULL,
    meet_id INTEGER NOT NULL,
    Event TEXT NOT NULL,
    Equipment TEXT NOT NULL,
    Age REAL,
    Division TEXT,
    BodyweightKg REAL,
    WeightClassKg REAL,
    Squat1Kg REAL,
    Squat2Kg REAL,
    Squat3Kg REAL,
    Squat4Kg REAL,
    Best3SquatKg REAL,
    Bench1Kg REAL,
    Bench2Kg REAL,
    Bench3Kg REAL,
    Bench4Kg REAL,
    Best3BenchKg REAL,
    Deadlift1Kg REAL,
    Deadlift2Kg REAL,
    Deadlift3Kg REAL,
    Deadlift4Kg REAL,
    Best3DeadliftKg REAL,
    TotalKg REAL,
    Place TEXT NOT NULL,
    Dots REAL,
    Wilks REAL,
    Tested TEXT,

    FOREIGN KEY (lifter_id) REFERENCES lifters(lifter_id),
    FOREIGN KEY (meet_id) REFERENCES meets(meet_id)
);"""

    @classmethod
    def get_table_name(cls) -> str:
        return "results"

    @classmethod
    def get_model_class(cls) -> Type[Result]:
        return Result


    def get_by_lifter_id(self, value: int) -> list[Result]:
        return self.get_all_from_attribute("lifter_id", value)

    def get_where_lifter_id_ge(self, value: int) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("lifter_id", Comparator.GE, value),))

    def get_where_lifter_id_le(self, value: int) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("lifter_id", Comparator.LE, value),))

    def get_where_lifter_id_in_range(self, lower_inclusive: int, upper_inclusive: int) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("lifter_id", Comparator.GE, lower_inclusive), ("lifter_id", Comparator.LE, upper_inclusive)))

    def get_by_meet_id(self, value: int) -> list[Result]:
        return self.get_all_from_attribute("meet_id", value)

    def get_where_meet_id_ge(self, value: int) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("meet_id", Comparator.GE, value),))

    def get_where_meet_id_le(self, value: int) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("meet_id", Comparator.LE, value),))

    def get_where_meet_id_in_range(self, lower_inclusive: int, upper_inclusive: int) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("meet_id", Comparator.GE, lower_inclusive), ("meet_id", Comparator.LE, upper_inclusive)))

    def get_by_event(self, value: str) -> list[Result]:
        return self.get_all_from_attribute("Event", value)

    def get_where_event_ge(self, value: str) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Event", Comparator.GE, value),))

    def get_where_event_le(self, value: str) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Event", Comparator.LE, value),))

    def get_where_event_in_range(self, lower_inclusive: str, upper_inclusive: str) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Event", Comparator.GE, lower_inclusive), ("Event", Comparator.LE, upper_inclusive)))

    def get_by_equipment(self, value: str) -> list[Result]:
        return self.get_all_from_attribute("Equipment", value)

    def get_where_equipment_ge(self, value: str) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Equipment", Comparator.GE, value),))

    def get_where_equipment_le(self, value: str) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Equipment", Comparator.LE, value),))

    def get_where_equipment_in_range(self, lower_inclusive: str, upper_inclusive: str) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Equipment", Comparator.GE, lower_inclusive), ("Equipment", Comparator.LE, upper_inclusive)))

    def get_by_age(self, value: float) -> list[Result]:
        return self.get_all_from_attribute("Age", value)

    def get_where_age_ge(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Age", Comparator.GE, value),))

    def get_where_age_le(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Age", Comparator.LE, value),))

    def get_where_age_in_range(self, lower_inclusive: float, upper_inclusive: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Age", Comparator.GE, lower_inclusive), ("Age", Comparator.LE, upper_inclusive)))

    def get_by_division(self, value: str) -> list[Result]:
        return self.get_all_from_attribute("Division", value)

    def get_where_division_ge(self, value: str) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Division", Comparator.GE, value),))

    def get_where_division_le(self, value: str) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Division", Comparator.LE, value),))

    def get_where_division_in_range(self, lower_inclusive: str, upper_inclusive: str) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Division", Comparator.GE, lower_inclusive), ("Division", Comparator.LE, upper_inclusive)))

    def get_by_bodyweight_kg(self, value: float) -> list[Result]:
        return self.get_all_from_attribute("BodyweightKg", value)

    def get_where_bodyweight_kg_ge(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("BodyweightKg", Comparator.GE, value),))

    def get_where_bodyweight_kg_le(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("BodyweightKg", Comparator.LE, value),))

    def get_where_bodyweight_kg_in_range(self, lower_inclusive: float, upper_inclusive: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("BodyweightKg", Comparator.GE, lower_inclusive), ("BodyweightKg", Comparator.LE, upper_inclusive)))

    def get_by_weight_class_kg(self, value: float) -> list[Result]:
        return self.get_all_from_attribute("WeightClassKg", value)

    def get_where_weight_class_kg_ge(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("WeightClassKg", Comparator.GE, value),))

    def get_where_weight_class_kg_le(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("WeightClassKg", Comparator.LE, value),))

    def get_where_weight_class_kg_in_range(self, lower_inclusive: float, upper_inclusive: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("WeightClassKg", Comparator.GE, lower_inclusive), ("WeightClassKg", Comparator.LE, upper_inclusive)))

    def get_by_squat1_kg(self, value: float) -> list[Result]:
        return self.get_all_from_attribute("Squat1Kg", value)

    def get_where_squat1_kg_ge(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Squat1Kg", Comparator.GE, value),))

    def get_where_squat1_kg_le(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Squat1Kg", Comparator.LE, value),))

    def get_where_squat1_kg_in_range(self, lower_inclusive: float, upper_inclusive: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Squat1Kg", Comparator.GE, lower_inclusive), ("Squat1Kg", Comparator.LE, upper_inclusive)))

    def get_by_squat2_kg(self, value: float) -> list[Result]:
        return self.get_all_from_attribute("Squat2Kg", value)

    def get_where_squat2_kg_ge(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Squat2Kg", Comparator.GE, value),))

    def get_where_squat2_kg_le(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Squat2Kg", Comparator.LE, value),))

    def get_where_squat2_kg_in_range(self, lower_inclusive: float, upper_inclusive: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Squat2Kg", Comparator.GE, lower_inclusive), ("Squat2Kg", Comparator.LE, upper_inclusive)))

    def get_by_squat3_kg(self, value: float) -> list[Result]:
        return self.get_all_from_attribute("Squat3Kg", value)

    def get_where_squat3_kg_ge(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Squat3Kg", Comparator.GE, value),))

    def get_where_squat3_kg_le(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Squat3Kg", Comparator.LE, value),))

    def get_where_squat3_kg_in_range(self, lower_inclusive: float, upper_inclusive: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Squat3Kg", Comparator.GE, lower_inclusive), ("Squat3Kg", Comparator.LE, upper_inclusive)))

    def get_by_squat4_kg(self, value: float) -> list[Result]:
        return self.get_all_from_attribute("Squat4Kg", value)

    def get_where_squat4_kg_ge(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Squat4Kg", Comparator.GE, value),))

    def get_where_squat4_kg_le(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Squat4Kg", Comparator.LE, value),))

    def get_where_squat4_kg_in_range(self, lower_inclusive: float, upper_inclusive: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Squat4Kg", Comparator.GE, lower_inclusive), ("Squat4Kg", Comparator.LE, upper_inclusive)))

    def get_by_best3_squat_kg(self, value: float) -> list[Result]:
        return self.get_all_from_attribute("Best3SquatKg", value)

    def get_where_best3_squat_kg_ge(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Best3SquatKg", Comparator.GE, value),))

    def get_where_best3_squat_kg_le(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Best3SquatKg", Comparator.LE, value),))

    def get_where_best3_squat_kg_in_range(self, lower_inclusive: float, upper_inclusive: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Best3SquatKg", Comparator.GE, lower_inclusive), ("Best3SquatKg", Comparator.LE, upper_inclusive)))

    def get_by_bench1_kg(self, value: float) -> list[Result]:
        return self.get_all_from_attribute("Bench1Kg", value)

    def get_where_bench1_kg_ge(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Bench1Kg", Comparator.GE, value),))

    def get_where_bench1_kg_le(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Bench1Kg", Comparator.LE, value),))

    def get_where_bench1_kg_in_range(self, lower_inclusive: float, upper_inclusive: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Bench1Kg", Comparator.GE, lower_inclusive), ("Bench1Kg", Comparator.LE, upper_inclusive)))

    def get_by_bench2_kg(self, value: float) -> list[Result]:
        return self.get_all_from_attribute("Bench2Kg", value)

    def get_where_bench2_kg_ge(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Bench2Kg", Comparator.GE, value),))

    def get_where_bench2_kg_le(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Bench2Kg", Comparator.LE, value),))

    def get_where_bench2_kg_in_range(self, lower_inclusive: float, upper_inclusive: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Bench2Kg", Comparator.GE, lower_inclusive), ("Bench2Kg", Comparator.LE, upper_inclusive)))

    def get_by_bench3_kg(self, value: float) -> list[Result]:
        return self.get_all_from_attribute("Bench3Kg", value)

    def get_where_bench3_kg_ge(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Bench3Kg", Comparator.GE, value),))

    def get_where_bench3_kg_le(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Bench3Kg", Comparator.LE, value),))

    def get_where_bench3_kg_in_range(self, lower_inclusive: float, upper_inclusive: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Bench3Kg", Comparator.GE, lower_inclusive), ("Bench3Kg", Comparator.LE, upper_inclusive)))

    def get_by_bench4_kg(self, value: float) -> list[Result]:
        return self.get_all_from_attribute("Bench4Kg", value)

    def get_where_bench4_kg_ge(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Bench4Kg", Comparator.GE, value),))

    def get_where_bench4_kg_le(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Bench4Kg", Comparator.LE, value),))

    def get_where_bench4_kg_in_range(self, lower_inclusive: float, upper_inclusive: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Bench4Kg", Comparator.GE, lower_inclusive), ("Bench4Kg", Comparator.LE, upper_inclusive)))

    def get_by_best3_bench_kg(self, value: float) -> list[Result]:
        return self.get_all_from_attribute("Best3BenchKg", value)

    def get_where_best3_bench_kg_ge(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Best3BenchKg", Comparator.GE, value),))

    def get_where_best3_bench_kg_le(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Best3BenchKg", Comparator.LE, value),))

    def get_where_best3_bench_kg_in_range(self, lower_inclusive: float, upper_inclusive: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Best3BenchKg", Comparator.GE, lower_inclusive), ("Best3BenchKg", Comparator.LE, upper_inclusive)))

    def get_by_deadlift1_kg(self, value: float) -> list[Result]:
        return self.get_all_from_attribute("Deadlift1Kg", value)

    def get_where_deadlift1_kg_ge(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Deadlift1Kg", Comparator.GE, value),))

    def get_where_deadlift1_kg_le(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Deadlift1Kg", Comparator.LE, value),))

    def get_where_deadlift1_kg_in_range(self, lower_inclusive: float, upper_inclusive: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Deadlift1Kg", Comparator.GE, lower_inclusive), ("Deadlift1Kg", Comparator.LE, upper_inclusive)))

    def get_by_deadlift2_kg(self, value: float) -> list[Result]:
        return self.get_all_from_attribute("Deadlift2Kg", value)

    def get_where_deadlift2_kg_ge(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Deadlift2Kg", Comparator.GE, value),))

    def get_where_deadlift2_kg_le(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Deadlift2Kg", Comparator.LE, value),))

    def get_where_deadlift2_kg_in_range(self, lower_inclusive: float, upper_inclusive: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Deadlift2Kg", Comparator.GE, lower_inclusive), ("Deadlift2Kg", Comparator.LE, upper_inclusive)))

    def get_by_deadlift3_kg(self, value: float) -> list[Result]:
        return self.get_all_from_attribute("Deadlift3Kg", value)

    def get_where_deadlift3_kg_ge(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Deadlift3Kg", Comparator.GE, value),))

    def get_where_deadlift3_kg_le(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Deadlift3Kg", Comparator.LE, value),))

    def get_where_deadlift3_kg_in_range(self, lower_inclusive: float, upper_inclusive: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Deadlift3Kg", Comparator.GE, lower_inclusive), ("Deadlift3Kg", Comparator.LE, upper_inclusive)))

    def get_by_deadlift4_kg(self, value: float) -> list[Result]:
        return self.get_all_from_attribute("Deadlift4Kg", value)

    def get_where_deadlift4_kg_ge(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Deadlift4Kg", Comparator.GE, value),))

    def get_where_deadlift4_kg_le(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Deadlift4Kg", Comparator.LE, value),))

    def get_where_deadlift4_kg_in_range(self, lower_inclusive: float, upper_inclusive: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Deadlift4Kg", Comparator.GE, lower_inclusive), ("Deadlift4Kg", Comparator.LE, upper_inclusive)))

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

    def get_by_place(self, value: str) -> list[Result]:
        return self.get_all_from_attribute("Place", value)

    def get_where_place_ge(self, value: str) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Place", Comparator.GE, value),))

    def get_where_place_le(self, value: str) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Place", Comparator.LE, value),))

    def get_where_place_in_range(self, lower_inclusive: str, upper_inclusive: str) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Place", Comparator.GE, lower_inclusive), ("Place", Comparator.LE, upper_inclusive)))

    def get_by_dots(self, value: float) -> list[Result]:
        return self.get_all_from_attribute("Dots", value)

    def get_where_dots_ge(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Dots", Comparator.GE, value),))

    def get_where_dots_le(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Dots", Comparator.LE, value),))

    def get_where_dots_in_range(self, lower_inclusive: float, upper_inclusive: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Dots", Comparator.GE, lower_inclusive), ("Dots", Comparator.LE, upper_inclusive)))

    def get_by_wilks(self, value: float) -> list[Result]:
        return self.get_all_from_attribute("Wilks", value)

    def get_where_wilks_ge(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Wilks", Comparator.GE, value),))

    def get_where_wilks_le(self, value: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Wilks", Comparator.LE, value),))

    def get_where_wilks_in_range(self, lower_inclusive: float, upper_inclusive: float) -> list[Result]:
        return self.get_all_from_attributes_with_comparator((("Wilks", Comparator.GE, lower_inclusive), ("Wilks", Comparator.LE, upper_inclusive)))

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
