from dataclasses import dataclass

from src.models.dto.result import Result


@dataclass
class ResultSubset:
    best3_bench_kg: float
    best3_deadlift_kg: float
    best3_squat_kg: float
    total_kg: float
    bodyweight_kg: float
    age: float
    sex: str
    date: str

    def to_partial_result(self) -> Result:
        return Result(
            result_id=None, # type: ignore
            name=None, # type: ignore
            sex=self.sex,
            age=self.age,
            bodyweight_kg=self.bodyweight_kg,
            best3_bench_kg=self.best3_bench_kg,
            best3_deadlift_kg=self.best3_deadlift_kg,
            best3_squat_kg=self.best3_squat_kg,
            wilks=None, # type: ignore
            dots=None, # type: ignore
            federation=None, # type: ignore
            place=None, # type: ignore
            tested=None, # type: ignore
            total_kg=self.total_kg,
            date=self.date,
            sanctioned=None, # type: ignore
        )

    @classmethod
    def from_full_result(cls, result: Result) -> 'ResultSubset':
        return cls(best3_bench_kg = result.best3_bench_kg,
            best3_deadlift_kg = result.best3_deadlift_kg,
            best3_squat_kg = result.best3_squat_kg,
            total_kg = result.total_kg,
            bodyweight_kg = result.bodyweight_kg,
            age = result.age,
            sex = result.sex,
            date = result.date
        )

    def __str__(self) -> str:
        return f"Date {self.date}. Total {self.total_kg}kg. Age {self.age}. Bodyweight {self.bodyweight_kg}kg. Sex {self.sex}. S/B/D {self.best3_squat_kg}/{self.best3_bench_kg}/{self.best3_deadlift_kg} (kgs)."
