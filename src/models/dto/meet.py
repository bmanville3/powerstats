# THIS CLASS WAS GENERATE WITH generate_database_classes.py
# ANYTHING YOU ADD HERE MAY BE OVERWRITTEN IN THE FUTURE
from dataclasses import dataclass


@dataclass
class Meet:
    meet_id: int
    federation: str
    meet_country: str | None
    meet_state: str | None
    meet_name: str | None
    sanctioned: str | None
    meet_type: str | None
