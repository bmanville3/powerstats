import logging
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(1, os.path.realpath(os.path.pardir))
from path_finder_helper import find_models_dir, find_tables_dir

from src.database.tables.table_builder import ColumnBuilder, TableBuilder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODELS_DIR = find_models_dir().absolute()
if not MODELS_DIR.exists():
    raise ValueError("Models directory does not exist for some reason")
MODELS_DIR = MODELS_DIR / "dto"
if not MODELS_DIR.exists():
    MODELS_DIR.mkdir(parents=True)

with open(f"{MODELS_DIR}/__init__.py", "w") as f:
    f.write("")

TABLE_DIR = find_tables_dir().absolute()
if not TABLE_DIR.exists():
    raise ValueError("Table directory does not exist for some reason")
TABLE_DIR = TABLE_DIR / "dto_table"
if not TABLE_DIR.exists():
    TABLE_DIR.mkdir(parents=True)
with open(f"{TABLE_DIR}/__init__.py", "w") as f:
    f.write("")

meets = (
    TableBuilder("meets", "Meet")
    .add_column(
        ColumnBuilder("meet_id", ColumnBuilder.Type.INTEGER)
        .add_attribute(ColumnBuilder.Attribute.PRIMARY_KEY)
        .add_attribute(ColumnBuilder.Attribute.AUTOINCREMENT)
    )
    .add_column(
        ColumnBuilder("Federation", ColumnBuilder.Type.TEXT).add_attribute(
            ColumnBuilder.Attribute.NOT_NULL
        )
    )
    .add_column(ColumnBuilder("MeetCountry", ColumnBuilder.Type.TEXT))
    .add_column(ColumnBuilder("MeetState", ColumnBuilder.Type.TEXT))
    .add_column(ColumnBuilder("MeetName", ColumnBuilder.Type.TEXT))
    .add_column(ColumnBuilder("Sanctioned", ColumnBuilder.Type.TEXT))
    .add_column(ColumnBuilder("MeetType", ColumnBuilder.Type.TEXT))
)

lifters = (
    TableBuilder("lifters", "Lifter")
    .add_column(
        ColumnBuilder("lifter_id", ColumnBuilder.Type.INTEGER)
        .add_attribute(ColumnBuilder.Attribute.PRIMARY_KEY)
        .add_attribute(ColumnBuilder.Attribute.AUTOINCREMENT)
    )
    .add_column(
        ColumnBuilder("Name", ColumnBuilder.Type.TEXT)
        .add_attribute(ColumnBuilder.Attribute.NOT_NULL)
        .add_attribute(ColumnBuilder.Attribute.UNIQUE)
    )
    .add_column(
        ColumnBuilder("Sex", ColumnBuilder.Type.TEXT).add_attribute(
            ColumnBuilder.Attribute.NOT_NULL
        )
    )
    .add_column(ColumnBuilder("Country", ColumnBuilder.Type.TEXT))
    .add_column(ColumnBuilder("State", ColumnBuilder.Type.TEXT))
)

results = (
    TableBuilder("results", "Result")
    .add_column(
        ColumnBuilder("result_id", ColumnBuilder.Type.INTEGER)
        .add_attribute(ColumnBuilder.Attribute.PRIMARY_KEY)
        .add_attribute(ColumnBuilder.Attribute.AUTOINCREMENT)
    )
    .add_column(
        ColumnBuilder("lifter_id", ColumnBuilder.Type.INTEGER).add_attribute(
            ColumnBuilder.Attribute.NOT_NULL
        ),
        foreign_table="lifters",
    )
    .add_column(
        ColumnBuilder("meet_id", ColumnBuilder.Type.INTEGER).add_attribute(
            ColumnBuilder.Attribute.NOT_NULL
        ),
        foreign_table="meets",
    )
    .add_column(
        ColumnBuilder("Event", ColumnBuilder.Type.TEXT).add_attribute(
            ColumnBuilder.Attribute.NOT_NULL
        )
    )
    .add_column(
        ColumnBuilder("Equipment", ColumnBuilder.Type.TEXT).add_attribute(
            ColumnBuilder.Attribute.NOT_NULL
        )
    )
    .add_column(ColumnBuilder("Age", ColumnBuilder.Type.REAL))
    .add_column(ColumnBuilder("Division", ColumnBuilder.Type.TEXT))
    .add_column(ColumnBuilder("BodyweightKg", ColumnBuilder.Type.REAL))
    .add_column(ColumnBuilder("WeightClassKg", ColumnBuilder.Type.REAL))
    .add_column(ColumnBuilder("Squat1Kg", ColumnBuilder.Type.REAL))
    .add_column(ColumnBuilder("Squat2Kg", ColumnBuilder.Type.REAL))
    .add_column(ColumnBuilder("Squat3Kg", ColumnBuilder.Type.REAL))
    .add_column(ColumnBuilder("Squat4Kg", ColumnBuilder.Type.REAL))
    .add_column(ColumnBuilder("Best3SquatKg", ColumnBuilder.Type.REAL))
    .add_column(ColumnBuilder("Bench1Kg", ColumnBuilder.Type.REAL))
    .add_column(ColumnBuilder("Bench2Kg", ColumnBuilder.Type.REAL))
    .add_column(ColumnBuilder("Bench3Kg", ColumnBuilder.Type.REAL))
    .add_column(ColumnBuilder("Bench4Kg", ColumnBuilder.Type.REAL))
    .add_column(ColumnBuilder("Best3BenchKg", ColumnBuilder.Type.REAL))
    .add_column(ColumnBuilder("Deadlift1Kg", ColumnBuilder.Type.REAL))
    .add_column(ColumnBuilder("Deadlift2Kg", ColumnBuilder.Type.REAL))
    .add_column(ColumnBuilder("Deadlift3Kg", ColumnBuilder.Type.REAL))
    .add_column(ColumnBuilder("Deadlift4Kg", ColumnBuilder.Type.REAL))
    .add_column(ColumnBuilder("Best3DeadliftKg", ColumnBuilder.Type.REAL))
    .add_column(ColumnBuilder("TotalKg", ColumnBuilder.Type.REAL))
    .add_column(
        ColumnBuilder("Place", ColumnBuilder.Type.TEXT).add_attribute(
            ColumnBuilder.Attribute.NOT_NULL
        )
    )
    .add_column(ColumnBuilder("Dots", ColumnBuilder.Type.REAL))
    .add_column(ColumnBuilder("Wilks", ColumnBuilder.Type.REAL))
    .add_column(ColumnBuilder("Tested", ColumnBuilder.Type.TEXT))
)


def format_with_ruff(file_path: str | Path) -> None:
    try:
        subprocess.run(
            ["ruff", "check", file_path, "--no-cache", "--extend-select=I", "--fix"],
            check=True
        )
        logger.info(f"Formatted {file_path} successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error formatting {file_path}: {e}")


# Generate data classes

model_import = """# THIS CLASS WAS GENERATE WITH generate_database_classes.py
# ANYTHING YOU ADD HERE MAY BE OVERWRITTEN IN THE FUTURE
from dataclasses import dataclass\n\n
"""
with open(MODELS_DIR / "meet.py", "w") as f:
    f.write(model_import)
    f.write(meets.generate_python_class())
    f.write("\n")

with open(MODELS_DIR / "result.py", "w") as f:
    f.write(model_import)
    f.write(results.generate_python_class())
    f.write("\n")

with open(MODELS_DIR / "lifter.py", "w") as f:
    f.write(model_import)
    f.write(lifters.generate_python_class())
    f.write("\n")

format_with_ruff(MODELS_DIR)

# Generate table classes
table_import = """# THIS CLASS WAS GENERATE WITH generate_database_classes.py
# ANYTHING YOU ADD HERE MAY BE OVERWRITTEN IN THE FUTURE
from typing import Type

from src.database.tables.table import Comparator, Table
{}\n\n
"""
with open(TABLE_DIR / "meet.py", "w") as f:
    f.write(
        table_import.format(
            f"from src.models.dto.meet import {meets._python_class_name}"
        )
    )
    f.write(meets.generate_table_class())
    f.write("\n")

with open(TABLE_DIR / "result.py", "w") as f:
    f.write(
        table_import.format(
            f"from src.models.dto.result import {results._python_class_name}"
        )
    )
    f.write(results.generate_table_class())
    f.write("\n")

with open(TABLE_DIR / "lifter.py", "w") as f:
    f.write(
        table_import.format(
            f"from src.models.dto.lifter import {lifters._python_class_name}"
        )
    )
    f.write(lifters.generate_table_class())
    f.write("\n")

format_with_ruff(TABLE_DIR)
