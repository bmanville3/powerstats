import logging
import subprocess
from pathlib import Path

from src.database.tables.table_builder import ColumnBuilder, TableBuilder
from src.utils.utils import POWERSTATS

logger = logging.getLogger(__name__)


def generate_database_classes() -> None:
    MODELS_DIR = (POWERSTATS / "src/models").absolute()
    if not MODELS_DIR.exists():
        raise ValueError("Models directory does not exist for some reason")
    MODELS_DIR = MODELS_DIR / "dto"
    if not MODELS_DIR.exists():
        MODELS_DIR.mkdir(parents=True)

    with open(f"{MODELS_DIR}/__init__.py", "w") as f:
        f.write("")

    TABLE_DIR = (POWERSTATS / "src/database/tables/").absolute()
    if not TABLE_DIR.exists():
        raise ValueError("Table directory does not exist for some reason")
    TABLE_DIR = TABLE_DIR / "dto_table"
    if not TABLE_DIR.exists():
        TABLE_DIR.mkdir(parents=True)
    with open(f"{TABLE_DIR}/__init__.py", "w") as f:
        f.write("")
    results = (
        TableBuilder("results", "Result")
        .add_column(
            ColumnBuilder("result_id", ColumnBuilder.Type.INTEGER)
            .add_attribute(ColumnBuilder.Attribute.PRIMARY_KEY)
            .add_attribute(ColumnBuilder.Attribute.AUTOINCREMENT)
        )
        .add_column(
            ColumnBuilder("Name", ColumnBuilder.Type.TEXT).add_attribute(
                ColumnBuilder.Attribute.NOT_NULL
            )
        )
        .add_column(
            ColumnBuilder("Sex", ColumnBuilder.Type.TEXT).add_attribute(
                ColumnBuilder.Attribute.NOT_NULL
            )
        )
        .add_column(
            ColumnBuilder("Age", ColumnBuilder.Type.REAL).add_attribute(
                ColumnBuilder.Attribute.NOT_NULL
            )
        )
        .add_column(
            ColumnBuilder("BodyweightKg", ColumnBuilder.Type.REAL).add_attribute(
                ColumnBuilder.Attribute.NOT_NULL
            )
        )
        .add_column(
            ColumnBuilder("Best3SquatKg", ColumnBuilder.Type.REAL).add_attribute(
                ColumnBuilder.Attribute.NOT_NULL
            )
        )
        .add_column(
            ColumnBuilder("Best3BenchKg", ColumnBuilder.Type.REAL).add_attribute(
                ColumnBuilder.Attribute.NOT_NULL
            )
        )
        .add_column(
            ColumnBuilder("Best3DeadliftKg", ColumnBuilder.Type.REAL).add_attribute(
                ColumnBuilder.Attribute.NOT_NULL
            )
        )
        .add_column(
            ColumnBuilder("TotalKg", ColumnBuilder.Type.REAL).add_attribute(
                ColumnBuilder.Attribute.NOT_NULL
            )
        )
        .add_column(
            ColumnBuilder("Wilks", ColumnBuilder.Type.REAL).add_attribute(
                ColumnBuilder.Attribute.NOT_NULL
            )
        )
        .add_column(
            ColumnBuilder("Dots", ColumnBuilder.Type.REAL).add_attribute(
                ColumnBuilder.Attribute.NOT_NULL
            )
        )
        .add_column(
            ColumnBuilder("Federation", ColumnBuilder.Type.TEXT).add_attribute(
                ColumnBuilder.Attribute.NOT_NULL
            )
        )
        .add_column(
            ColumnBuilder("Sanctioned", ColumnBuilder.Type.TEXT).add_attribute(
                ColumnBuilder.Attribute.NOT_NULL
            )
        )
        .add_column(
            ColumnBuilder("Place", ColumnBuilder.Type.TEXT).add_attribute(
                ColumnBuilder.Attribute.NOT_NULL
            )
        )
        .add_column(
            ColumnBuilder("Date", ColumnBuilder.Type.TEXT).add_attribute(
                ColumnBuilder.Attribute.NOT_NULL
            )
        )
        .add_column(
            ColumnBuilder("Tested", ColumnBuilder.Type.TEXT).add_attribute(
                ColumnBuilder.Attribute.NOT_NULL
            )
        )
    )

    def format_with_ruff(file_path: str | Path) -> None:
        try:
            subprocess.run(
                [
                    "ruff",
                    "format",
                    file_path,
                ],
                check=True,
            )
            subprocess.run(
                [
                    "ruff",
                    "check",
                    file_path,
                    "--no-cache",
                    "--extend-select=I",
                    "--fix",
                ],
                check=True,
            )
            logger.info(f"Formatted {file_path} successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error formatting {file_path}: {e}")

    # Generate data classes

    model_import = """# THIS CLASS WAS GENERATE WITH generate_database_classes.py
# ANYTHING YOU ADD HERE MAY BE OVERWRITTEN IN THE FUTURE
from dataclasses import dataclass\n\n
"""

    with open(MODELS_DIR / "result.py", "w") as f:
        f.write(model_import)
        f.write(results.generate_python_class())
        f.write("\n")

    format_with_ruff(MODELS_DIR)

    # Generate table classes
    table_import = """# THIS CLASS WAS GENERATE WITH generate_database_classes.py
# ANYTHING YOU ADD HERE MAY BE OVERWRITTEN IN THE FUTURE
from typing import Type

from src.database.tables.table import Comparator, Table
{}\n\n
"""

    with open(TABLE_DIR / "result.py", "w") as f:
        f.write(
            table_import.format(
                f"from src.models.dto.result import {results._python_class_name}"
            )
        )
        f.write(results.generate_table_class())
        f.write("\n")

    format_with_ruff(TABLE_DIR)


if __name__ == "__main__":
    generate_database_classes()
