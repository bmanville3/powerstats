import argparse
import logging
from typing import Any

from src.analysis import distribution
from src.database.database import Database
from src.database.tables.dto_table.result import ResultTable
from src.database.tables.table import Table
from src.llm_interface import test_llm
from src.models.ml.trainer import test_models, train_models
from src.utils.cleaning_pipeline import generate_database
from src.utils.database_classes import generate_database_classes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
MODELS = ["LSTM", "RNN", "Bidirectional_LSTM"]

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
    choices=MODELS,
    help="Trains a new model on the openpowerlifting dataset.",
)
parser.add_argument(
    "--test",
    action="append",
    choices=MODELS,
    help="Tests a saved model on the openpowerlifting dataset.",
)
parser.add_argument(
    "--train_test_all",
    action="store_true",
    help="Trains and tests all models from scratch",
)
parser.add_argument(
    "--regenerate", action="store_true", help="Regenerates the database and dto classes"
)
parser.add_argument(
    "--test_llm", action="store_true", help="Tests the LLM on the true test data"
)

if __name__ == "__main__":
    args = parser.parse_args()
    logger.debug("args: %s", args)
    if args.regenerate:
        generate_database()
        generate_database_classes()
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
    if args.train_test_all:
        models_tt = set(MODELS)
        logger.info("Training and testing models: %s", models_tt)
        train_models(models_tt)
        test_models(models_tt)
    else:
        if args.train:
            models_to_train: set[str] = set(args.train)
            logger.info("Attempting to train the following models: %s", models_to_train)
            train_models(models_to_train)
        if args.test:
            models_to_test: set[str] = set(args.test)
            logger.info("Attempting to test the following models: %s", models_to_test)
            test_models(models_to_test)
    if args.test_llm:
        test_llm()
