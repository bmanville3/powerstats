import os
import sys
from pathlib import Path

import pandas as pd
from path_finder_helper import find_data_dir

from src.database.tables.dto_table.result import ResultTable
from src.models.dto.lifter import Lifter
from src.models.dto.result import Result
from src.models.ml.lifter_dataset import is_valid_result

sys.path.insert(1, os.path.realpath(os.path.pardir))
from src.database.database import Database
from src.database.tables.dto_table.lifter import LifterTable


def normalize_name(first: str, last: str) -> str:
    return f"{first.strip().lower()} {last.strip().lower()}"


def normalize_lifter_name(lifter_name: str) -> str:
    parts = lifter_name.strip().split()

    if len(parts) < 2:
        return lifter_name.strip().lower()

    # Try to detect common patterns
    last_name = parts[-1].lower()
    first_tokens = parts[:-1]

    # If the first tokens are initials, join them
    if all(len(tok) == 2 and tok.endswith('.') for tok in first_tokens):
        first_initials = ''.join(tok[0] for tok in first_tokens)
        return f"{first_initials.lower()} {last_name}"

    # Otherwise assume it's a full name
    first_name = first_tokens[0].lower()
    return f"{first_name} {last_name}"


def get_known_users() -> list[tuple[list[Result], Lifter]]:
    directory = find_data_dir() / "usapl_drug_testing_results"

    # Step 1: Build set of normalized full names for failed tests
    failing_names_set: set[str] = set()
    for csv_file in Path(directory).glob("*.csv"):
        try:
            df = pd.read_csv(csv_file)
            if {"First Name", "Last Name", "Status"}.issubset(df.columns):
                for _, row in df.iterrows():
                    if str(row["Status"]).strip().upper() == "FAIL":
                        full_name = normalize_name(row["First Name"], row["Last Name"])
                        failing_names_set.add(full_name)
            else:
                print(f"Skipping {csv_file.name} (missing columns)")
        except Exception as e:
            print(f"Failed to read {csv_file.name}: {e}")

    print(f"Number of unique failing full names: {len(failing_names_set)}")

    # Step 2: Load OpenPowerlifting lifters and results
    database = Database()
    result_table = ResultTable(database)
    lifter_table = LifterTable(database)

    all_results = list(filter(is_valid_result, result_table.get_all()))
    all_lifters = lifter_table.get_all()

    lifter_id_to_result_and_lifter: dict[int, tuple[list[Result], Lifter]] = {}
    for lifter in all_lifters:
        if lifter.sex == "Mx":
            continue
        lifter_id_to_result_and_lifter[lifter.lifter_id] = ([], lifter)

    for result in all_results:
        if result.lifter_id in lifter_id_to_result_and_lifter:
            lifter_id_to_result_and_lifter[result.lifter_id][0].append(result)

    # Step 3: Match normalized full names
    saved = []
    for results, lifter in lifter_id_to_result_and_lifter.values():
        if not results:
            continue
        norm_name = normalize_lifter_name(lifter.name)
        if norm_name in failing_names_set:
            saved.append((results, lifter))

    return saved


if __name__ == "__main__":
    print(get_known_users())
