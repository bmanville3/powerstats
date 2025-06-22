import logging
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List

import pandas as pd
from path_finder_helper import find_data_dir

from src.database.tables.dto_table.result import ResultTable
from src.models.dto.result import Result

sys.path.insert(1, os.path.realpath(os.path.pardir))
from src.database.database import Database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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


def get_known_users() -> List[List[Result]]:
    """
    Gets a sorted list (by date) of results where the last item
    in the list is the date the lifter tested positive for PEDs.
    """
    directory = find_data_dir() / "usapl_drug_testing_results"

    # Step 1: Build dict of normalized full names -> fail date
    failing_names_to_date: dict[str, str] = {}
    for csv_file in Path(directory).glob("*.csv"):
        try:
            df = pd.read_csv(csv_file)
            if {"First Name", "Last Name", "Status", "Date"}.issubset(df.columns):
                for _, row in df.iterrows():
                    if str(row["Status"]).strip().upper() == "FAIL":
                        full_name = normalize_name(row["First Name"], row["Last Name"])
                        failing_names_to_date[full_name] = row["Date"]
            else:
                logger.error(f"Skipping {csv_file.name} (missing columns)")
        except Exception as e:
            logger.error(f"Failed to read {csv_file.name}: {e}")
    logger.info("Number of unique failing full names: %s", len(failing_names_to_date))

    # Step 2: Load OpenPowerlifting results
    database = Database()
    result_table = ResultTable(database)
    all_results = result_table.get_all()
    logger.info("Got %s results from database", len(all_results))

    saved: dict[str, list[Result]] = {}
    MONTH_PATCHES = {"Sept": "Sep"}
    for result in all_results:
        name = normalize_lifter_name(result.name)
        fail_date_str = failing_names_to_date.get(name)
        if not fail_date_str:
            continue
        for wrong, right in MONTH_PATCHES.items():
            fail_date_str = fail_date_str.replace(wrong, right)

        # Parse the fail date robustly
        fail_date = None
        for fmt in ("%d-%b-%Y", "%d-%B-%Y", "%m-%d-%Y", "%m/%d/%Y"):
            try:
                fail_date = datetime.strptime(fail_date_str, fmt).date()
                break
            except ValueError:
                continue
        if fail_date is None:
            logger.warning(f"Could not parse fail date for {name}: {fail_date_str}")
            continue

        # Parse result date
        try:
            result_date = datetime.strptime(result.date, "%Y-%m-%d").date()
        except ValueError:
            logger.warning(f"Skipping result with invalid date: {result.date}")
            continue

        # Skip results more than 5 days after fail date
        if result_date > fail_date + timedelta(days=5):
            continue

        saved.setdefault(name, []).append(result)

    # Sort each list by date
    list_saved = [
        sorted(result_list, key=lambda res: res.date)
        for result_list in saved.values()
    ]

    logger.info("Total known PED users after filtering: %s", len(list_saved))
    return list_saved


if __name__ == "__main__":
    print(get_known_users())
