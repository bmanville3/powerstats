# THIS CLASS WAS GENERATE WITH generate_database_classes.py
# ANYTHING YOU ADD HERE MAY BE OVERWRITTEN IN THE FUTURE
from dataclasses import dataclass


@dataclass
class Result:
    result_id: int
    name: str
    sex: str
    age: float
    bodyweight_kg: float
    best3_squat_kg: float
    best3_bench_kg: float
    best3_deadlift_kg: float
    total_kg: float
    wilks: float
    dots: float
    federation: str
    sanctioned: str
    place: str
    date: str
    tested: str
