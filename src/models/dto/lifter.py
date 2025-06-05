# THIS CLASS WAS GENERATE WITH generate_database_classes.py
# ANYTHING YOU ADD HERE MAY BE OVERWRITTEN IN THE FUTURE
from dataclasses import dataclass


@dataclass
class Lifter:
    lifter_id: int
    name: str
    sex: str
    country: str | None
    state: str | None
