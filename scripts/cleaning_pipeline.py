import logging
import sqlite3

import numpy as np
import pandas as pd
from path_finder_helper import find_data_dir

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

### File paths — update these as needed ###
DATA_DIR = find_data_dir().absolute()
CSV_FILE = DATA_DIR / "raw/openpowerlifting-2025-05-31-c2a0b8b0.csv"
DB_FILE = DATA_DIR / "sqlite/powerlifting.db"
SCHEMA_PATH = DATA_DIR / "sqlite/schema.txt"

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
##################################


### Load all initial stuff ###

# load csv file
dtype_overrides = {
    # Strings (categorical or freeform text)
    "Name": "string",
    "Sex": "string",
    "Event": "string",
    "Equipment": "string",
    "AgeClass": "string",
    "BirthYearClass": "string",
    "Division": "string",
    "WeightClassKg": "string",
    "Place": "string",
    "Tested": "string",
    "Country": "string",
    "State": "string",
    "Federation": "string",
    "ParentFederation": "string",
    "Date": "string",  # gets dropped so just reading it as a string
    "MeetCountry": "string",
    "MeetState": "string",
    "MeetName": "string",
    "Sanctioned": "string",
    # Floats (numeric performance or body data, optional)
    "Age": "float32",
    "BodyweightKg": "float32",
    "Squat1Kg": "float32",
    "Squat2Kg": "float32",
    "Squat3Kg": "float32",
    "Squat4Kg": "float32",
    "Best3SquatKg": "float32",
    "Bench1Kg": "float32",
    "Bench2Kg": "float32",
    "Bench3Kg": "float32",
    "Bench4Kg": "float32",
    "Best3BenchKg": "float32",
    "Deadlift1Kg": "float32",
    "Deadlift2Kg": "float32",
    "Deadlift3Kg": "float32",
    "Deadlift4Kg": "float32",
    "Best3DeadliftKg": "float32",
    "TotalKg": "float32",
    "Dots": "float32",
    "Wilks": "float32",
    "Glossbrenner": "float32",
    "Goodlift": "float32",
}

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

# Deduplicate and insert into meets
logger.info("Processing meets...")
meet_cols = ["Federation", "MeetCountry", "MeetState", "MeetName", "Sanctioned"]
meets = (
    df[meet_cols].drop_duplicates().dropna(subset=["Federation"]).reset_index(drop=True)
)
meets = meets.copy()  # explicitly copying
# Try to extract the meet type
conditions = [
    meets["MeetName"].str.contains("National", case=False, na=False),
    meets["MeetName"].str.contains("Regional", case=False, na=False),
    meets["MeetName"].str.contains("State", case=False, na=False),
]
choices = ["National", "Regional", "State"]
meets["MeetType"] = np.select(conditions, choices, default="Unknown")
meets["meet_id"] = (
    meets.index + 1
)  # need to do this manually for later even though sql does it automatically
meets.to_sql("meets", conn, if_exists="append", index=False)
##################################


### Fill the lifters table ###

# Deduplicate and insert into lifters
logger.info("Processing lifters...")
# Step 1: Work with relevant columns
lifter_cols = ["Name", "Sex", "Country", "State"]
lifter_df = (
    df[lifter_cols]
    .drop_duplicates()
    .dropna(subset=["Name", "Sex"])
    .reset_index(drop=True)
)
lifter_df = lifter_df.copy()  # explicitly copying

# Step 2: Find names with multiple sexes
sex_counts = lifter_df.groupby("Name")["Sex"].nunique()
ambiguous_names = sex_counts[sex_counts > 1].index

# Step 3: Set Sex to "MX" for those names
lifter_df.loc[lifter_df["Name"].isin(ambiguous_names), "Sex"] = "Mx"

# Step 4: Drop duplicates and insert into DB
lifters = (
    lifter_df.drop_duplicates().drop_duplicates(subset=["Name"]).reset_index(drop=True)
)
lifters["lifter_id"] = lifters.index + 1
lifters.to_sql("lifters", conn, if_exists="append", index=False)
##################################


### Merge back IDs for meets and lifters ###

logger.info("Merging foreign keys...")
df = df.merge(meets, on=meet_cols, how="left")
df = df.merge(lifters, on=lifter_cols, how="left")
##################################


### Fill the results table ###

# Create and insert results
logger.info("Inserting results...")
result_cols = [
    "lifter_id",
    "meet_id",
    "Event",
    "Equipment",
    "Age",
    "Division",
    "BodyweightKg",
    "WeightClassKg",
    "Squat1Kg",
    "Squat2Kg",
    "Squat3Kg",
    "Squat4Kg",
    "Best3SquatKg",
    "Bench1Kg",
    "Bench2Kg",
    "Bench3Kg",
    "Bench4Kg",
    "Best3BenchKg",
    "Deadlift1Kg",
    "Deadlift2Kg",
    "Deadlift3Kg",
    "Deadlift4Kg",
    "Best3DeadliftKg",
    "TotalKg",
    "Place",
    "Dots",
    "Wilks",
    "Tested",
]
results = (
    df[result_cols]
    .drop_duplicates()
    .dropna(subset=["lifter_id", "meet_id", "Event", "Equipment", "Place"])
    .reset_index(drop=True)
)
results.to_sql("results", conn, if_exists="append", index=False)
##################################


### Finalize ###
conn.commit()
conn.close()
logger.info("Done. Database saved to: %s", DB_FILE)
##################################
