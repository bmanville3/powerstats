import argparse
import logging
from typing import Any

from src.analysis import distribution
from src.database.database import Database
from src.database.tables.dto_table.result import ResultTable
from src.database.tables.table import Table
from src.models.ml.trainer import train_models

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(
    description="CLI to run statistics on lifters. All generated graphs are placed under the graphs directory."
)
parser.add_argument(
    "-d",
    "--distribution",
    action="store_true",
    help="Graphs distributions of lifters. Graphs are placed under the graphs/distributions directory",
)
parser.add_argument(
    "--display_database_heads",
    action="store_true",
    help="Prints the heads of each table in the database to the command line",
)
parser.add_argument(
    "--train",
    action="append",
    choices=["LSTM"],
    help="Trains a new model on the openpowerlifting dataset.",
)

if __name__ == "__main__":
    args = parser.parse_args()
    logger.debug("args: %s", args)
    if args.display_database_heads:
        database = Database()
        all_tables: list[Table[Any]] = [ResultTable(database)]
        for table in all_tables:
            head = table.get_head()
            print(f"Head of {table.get_table_name()} table:\n")
            for i, row in enumerate(head):
                print(f"{i}:\t{row}")
            print()
    if args.distribution:
        logger.info("Going into distribution main()")
        distribution.main()
    if args.train:
        models: set[str] = set(args.train)
        logger.info("Attempting to train the following models: %s", models)
        train_models(models)
