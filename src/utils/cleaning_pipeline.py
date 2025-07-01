import logging
import sqlite3

import pandas as pd

from src.utils.utils import POWERSTATS

logger = logging.getLogger(__name__)

### File paths — update these as needed ###
DATA_DIR = (POWERSTATS / "data").absolute()
CSV_FILE = DATA_DIR / "raw/openpowerlifting-2025-05-31-c2a0b8b0.csv"
DB_FILE = DATA_DIR / "sqlite/powerlifting.db"
SCHEMA_PATH = DATA_DIR / "sqlite/schema.txt"
##################################


### Load all initial stuff ###

# load csv file
dtype_overrides = {
    "Age": "float32",
    "Best3BenchKg": "float32",
    "Best3DeadliftKg": "float32",
    "Best3SquatKg": "float32",
    "BodyweightKg": "float32",
    "Date": "string",
    "Dots": "float32",
    "Equipment": "string",
    "Event": "string",
    "Federation": "string",
    "Name": "string",
    "Place": "string",
    "Sanctioned": "string",
    "Sex": "string",
    "Tested": "string",
    "TotalKg": "float32",
    "Wilks": "float32",
}


def generate_database() -> None:
    if not CSV_FILE.exists():
        raise ValueError(
            "Please download the openpowerlifting-2025-05-31-c2a0b8b0.csv "
            + "(other dates are acceptable) from https://gitlab.com/openpowerlifting/opl-data"
        )
    elif DB_FILE.exists():
        raise ValueError(
            f"Database {DB_FILE} already exists. Please rename the existing database "
            + "or choose a new database name"
        )
    elif not SCHEMA_PATH.exists():
        raise ValueError(f"Could not find schema at {SCHEMA_PATH}")
    logger.info("Loading CSV %s...", CSV_FILE)
    df = pd.read_csv(CSV_FILE, dtype=dtype_overrides)

    # make database file
    logger.info("Connection to %s...", DB_FILE)
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()

    # create tables from schema file
    logger.info("Creating tables...")
    with open(SCHEMA_PATH, "r") as schema_file:
        cur.executescript(schema_file.read())
    ##################################

    ### Fill the meet table ###

    # Load CSV
    logger.info("Loading CSV %s...", CSV_FILE)
    df = pd.read_csv(CSV_FILE, dtype=dtype_overrides, usecols=dtype_overrides.keys())

    # Drop rows with nulls in any required column
    required_fields = [k for k in dtype_overrides if k != "Tested"]
    df = df.dropna(subset=required_fields)

    # Clean Sex: convert conflicting entries to 'Mx'
    logger.info("Cleaning Sex values...")
    sex_counts = df.groupby("Name")["Sex"].nunique()
    ambiguous_names = sex_counts[sex_counts > 1].index
    df.loc[df["Name"].isin(ambiguous_names), "Sex"] = "Mx"

    # Convert Tested to boolean
    df["Tested"] = df["Tested"].map(
        lambda x: "yes" if str(x).strip().lower() == "yes" else "no"
    )

    # Filter to only SBD events and Raw equipment and then drop it
    df = df[(df["Event"] == "SBD") & (df["Equipment"] == "Raw")]
    df = df.drop(columns=["Event", "Equipment"])

    logger.info("%s rows in database", len(df))

    # Create DB + results table
    logger.info("Creating SQLite DB and results table...")
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    # Insert cleaned data
    logger.info("Inserting results...")
    df.to_sql("results", conn, if_exists="append", index=False)

    # Done
    conn.commit()
    conn.close()
    logger.info("Done. Database saved to: %s", DB_FILE)


if __name__ == "__main__":
    generate_database()
