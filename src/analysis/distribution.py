import logging
import statistics
from typing import Iterable

import matplotlib.pyplot as plt

from src.database.database import Database
from src.database.tables.dto_table.lifter import LifterTable
from src.database.tables.dto_table.result import ResultTable
from src.models.dto.result import Result
from src.utils import find_dir, get_lb_from_kg

logger = logging.getLogger(__name__)


def extract_valid(values: Iterable[float | None]) -> list[float]:
    return [v for v in values if v is not None and v > 0]

def plot_all_distributions(results: list[Result], prefixes: list[str]) -> None:
    attributes = [
        ("best3_squat_kg", "Best 3 Squat (kg)"),
        ("best3_bench_kg", "Best 3 Bench (kg)"),
        ("best3_deadlift_kg", "Best 3 Deadlift (kg)"),
        ("total_kg", "Total (kg)"),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle(f"{' - '.join(prefixes)} - Distribution of Lifts", fontsize=16)

    for ax, (attribute, xlabel) in zip(axes.flat, attributes):
        values = extract_valid([getattr(r, attribute) for r in results])
        if not values:
            ax.set_title(f"{xlabel} - No Data")
            continue

        avg = statistics.mean(values)
        stddev = statistics.stdev(values) if len(values) > 1 else 0.0
        med = statistics.median(values)
        mode = statistics.mode(values)

        ax.hist(values, bins=70, color='steelblue', edgecolor='black', alpha=0.7, range=(0, max(values) + int (stddev / 2)))
        ax.set_title(f"{xlabel} - ({len(values):,} total)\nMean: {avg:.1f}kgs | Median: {med:.1f}kgs | Mode: {mode:.1f}kgs | Std: {stddev:.1f}kgs" +
                    f"\nMean: {get_lb_from_kg(avg):.1f}lbs | Median: {get_lb_from_kg(med):.1f}lbs | Mode: {get_lb_from_kg(mode):.1f}lbs | Std: {get_lb_from_kg(stddev):.1f}lbs")
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Count of Lifts")
        ax.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    path = find_dir("graphs") / f"distribution/{'/'.join(prefixes[:-1])}"
    if not path.exists():
        path.mkdir(parents=True)
    path = path / f'{prefixes[-1]}_graph'
    logger.info("Saving graph at %s", str(path))
    plt.savefig(path)
    plt.clf()

def main() -> None:
    database = Database()
    result_table = ResultTable(database)
    lifter_table = LifterTable(database)
    id_to_sex = {lifter.lifter_id: lifter.sex for lifter in lifter_table.get_all()}
    types_of_sex = set(id_to_sex.values())
    assert len(types_of_sex) == 3
    assert "Mx" in types_of_sex and "M" in types_of_sex and "F" in types_of_sex

    sexes = [("M", "Male"), ("F", "Female"), ("Mx", "Mx")]
    equipment_types = [("Raw", "Raw"), ("Wraps", "Wraps"), ("Single-ply", "Single-ply"), ("Multi-ply", "Multi-ply")]
    tested_cat = [("Yes", "Tested"), (None, "Untested")]
    event_type = [("SBD", "Full Power"), (None, "Any Event Type")]

    combo_len = len(sexes) * len(equipment_types) * len(tested_cat) * len(event_type)

    full_results = result_table.get_all()
    i = 0
    for (sex, sex_name) in sexes:
        gen_results: list[Result] = list(filter(lambda res: id_to_sex[res.lifter_id] == sex, full_results))
        for (eq_t, eq_name) in equipment_types:
            eq_gen_results: list[Result] = list(filter(lambda res: res.equipment == eq_t, gen_results))
            for (tested, tested_name) in tested_cat:
                tested_eq_gen_results: list[Result] = list(filter(lambda res: res.tested == tested, eq_gen_results))
                for (ev_t, ev_name) in event_type:
                    event_tested_eq_gen_results: list[Result]
                    if ev_t is not None:
                        event_tested_eq_gen_results = list(filter(lambda res: res.event == ev_t, tested_eq_gen_results))
                    else:
                        event_tested_eq_gen_results = tested_eq_gen_results
                    filters = [eq_name, ev_name, tested_name, sex_name]
                    logger.info("Graphing distribution %d/%d. Filters: %s", i + 1, combo_len, filters)
                    plot_all_distributions(event_tested_eq_gen_results, filters)
                    i += 1

if __name__ == "__main__":
    main()
