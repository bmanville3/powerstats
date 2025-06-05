# THIS CLASS WAS GENERATE WITH generate_database_classes.py
# ANYTHING YOU ADD HERE MAY BE OVERWRITTEN IN THE FUTURE
from dataclasses import dataclass


@dataclass
class Result:
    result_id: int
    lifter_id: int
    meet_id: int
    event: str
    equipment: str
    age: float | None
    division: str | None
    bodyweight_kg: float | None
    weight_class_kg: float | None
    squat1_kg: float | None
    squat2_kg: float | None
    squat3_kg: float | None
    squat4_kg: float | None
    best3_squat_kg: float | None
    bench1_kg: float | None
    bench2_kg: float | None
    bench3_kg: float | None
    bench4_kg: float | None
    best3_bench_kg: float | None
    deadlift1_kg: float | None
    deadlift2_kg: float | None
    deadlift3_kg: float | None
    deadlift4_kg: float | None
    best3_deadlift_kg: float | None
    total_kg: float | None
    place: str
    dots: float | None
    wilks: float | None
    tested: str | None
