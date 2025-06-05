import os
import sys
from pathlib import Path

sys.path.insert(1, os.path.realpath(os.path.pardir))

from src.utils import find_dir


def find_data_dir() -> Path:
    return find_dir("data")


def find_src_dir() -> Path:
    return find_dir("src")


def find_tables_dir() -> Path:
    return find_src_dir() / "database" / "tables"


def find_models_dir() -> Path:
    return find_src_dir() / "models"
