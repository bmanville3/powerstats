from pathlib import Path

KG_TO_LB: float = 2.20462


def find_dir(target: str) -> Path:
    current = Path.cwd()
    while not (current / target).is_dir():
        if current.parent == current:
            raise FileNotFoundError(
                f"Directory '{target}' not found in any parent of {Path.cwd()}"
            )
        current = current.parent
    return current / target


POWERSTATS = find_dir("powerstats").absolute()


def get_lb_from_kg(kg: float) -> float:
    return kg * KG_TO_LB


def get_kg_from_lb(lb: float) -> float:
    return lb / KG_TO_LB
