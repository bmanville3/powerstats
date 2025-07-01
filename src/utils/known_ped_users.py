import logging
from datetime import datetime, timedelta
from pathlib import Path
from random import sample
from typing import List

import pandas as pd

from src.database.database import Database
from src.database.tables.dto_table.result import ResultTable
from src.models.dto.result import Result
from src.models.ml.lifter_dataset import IS_CLEAN_LABEL, IS_USING_LABEL
from src.utils.utils import POWERSTATS

logger = logging.getLogger(__name__)

MONTH_PATCHES = {"Sept": "Sep"}


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
    if all(len(tok) == 2 and tok.endswith(".") for tok in first_tokens):
        first_initials = "".join(tok[0] for tok in first_tokens)
        return f"{first_initials.lower()} {last_name}"

    # Otherwise assume it's a full name
    first_name = first_tokens[0].lower()
    return f"{first_name} {last_name}"


def filter_results(
    name_to_date: dict[str, str], all_results: list[Result]
) -> dict[str, list[Result]]:
    collected: dict[str, list[Result]] = {}
    for result in all_results:
        name = normalize_lifter_name(result.name)
        date_str = name_to_date.get(name)
        if not date_str:
            continue
        for wrong, right in MONTH_PATCHES.items():
            date_str = date_str.replace(wrong, right)

        test_date = None
        for fmt in ("%d-%b-%Y", "%d-%B-%Y", "%m-%d-%Y", "%m/%d/%Y"):
            try:
                test_date = datetime.strptime(date_str, fmt).date()
                break
            except ValueError:
                continue
        if test_date is None:
            logger.debug(f"Could not parse test date for {name}: {date_str}")
            continue

        try:
            result_date = datetime.strptime(result.date, "%Y-%m-%d").date()
        except ValueError:
            logger.debug(f"Skipping result with invalid date: {result.date}")
            continue

        if result_date > test_date + timedelta(days=5):
            continue

        collected.setdefault(name, []).append(result)

    return collected


def get_known_users() -> List[tuple[list[Result], float]]:
    """
    Gets a sorted list (by date) of results where the last item
    in the list is the date the lifter tested positive/negative for PEDs.
    Returns a list of tuples: (results, label), where label=1 means FAIL, 0 means PASS.
    Ensures equal number of passing and failing users.
    """
    directory = POWERSTATS / "data/usapl_drug_testing_results"

    # Step 1: Build dict of normalized full names -> fail/pass date
    failing_names_to_date: dict[str, str] = {}
    passing_names_to_date: dict[str, str] = {}
    for csv_file in Path(directory).glob("*.csv"):
        try:
            df = pd.read_csv(csv_file)
            if {"First Name", "Last Name", "Status", "Date"}.issubset(df.columns):
                for _, row in df.iterrows():
                    try:
                        full_name = normalize_name(row["First Name"], row["Last Name"])
                        status = str(row["Status"]).strip().upper()
                        if status == "FAIL":
                            failing_names_to_date[full_name] = row["Date"]
                        elif status == "PASS":
                            passing_names_to_date[full_name] = row["Date"]
                    except Exception as inner_e:
                        logger.debug("Failed to read row %s: %s", row, inner_e)
            else:
                logger.error("Skipping %s (missing columns)", csv_file.name)
        except Exception as e:
            logger.error("Failed to read %s: %s", csv_file.name, e)
    logger.info(
        "Number of unique failing full names: %s. Number of unique passing full names: %s",
        len(failing_names_to_date),
        len(passing_names_to_date),
    )

    # Step 2: Load OpenPowerlifting results
    database = Database()
    result_table = ResultTable(database)
    all_results = result_table.get_all()

    failing_users = filter_results(failing_names_to_date, all_results)
    passing_users = filter_results(passing_names_to_date, all_results)

    # Sample the same number of passing users as failing users
    fail_count = len(failing_users)
    passing_keys = sample(list(passing_users.keys()), fail_count)
    passing_users = {k: passing_users[k] for k in passing_keys}

    # Build sorted and labeled result lists
    def sorted_labeled_results(
        user_dict: dict[str, list[Result]], label: float
    ) -> List[tuple[list[Result], float]]:
        return [
            (sorted(results, key=lambda res: res.date), label)
            for results in user_dict.values()
        ]

    labeled_fails = sorted_labeled_results(failing_users, label=IS_USING_LABEL)
    labeled_passes = sorted_labeled_results(passing_users, label=IS_CLEAN_LABEL)

    logger.info(
        "Returning %s failing and %s passing users",
        len(labeled_fails),
        len(labeled_passes),
    )
    return labeled_fails + labeled_passes


if __name__ == "__main__":
    print(get_known_users())
