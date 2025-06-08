# How To

## Raw

### Where to download data

The raw data can be downloaded as a csv at [https://www.openpowerlifting.org/](https://www.openpowerlifting.org/). There are also more links for data exploration at [`powerstats/data/raw/additional_links.md`](raw/additional_links.md).

### Where to place the raw data

Once the raw data has been downloaded, place it under [`powerstats/data/raw/`](raw/).

### Metadata

[`powerstats/data/raw/raw_metadata.md`](raw/raw_metadata.md) contains descriptions about the data found in the raw dataset.

### Examples

You can find example data under [`powerstats/data/raw/raw_example.md`](raw/raw_example.md).

## SQL

### Generate the SQL Database

After you have placed the raw data in [`powerstats/data/raw/`](raw/), go to [`powerstats/scripts/cleaning_pipeline.py`](../scripts/cleaning_pipeline.py). You may have to change the `CSV_FILE` variable to match the name of the downloaded dataset. Currently, it is set to
`CSV_FILE = DATA_DIR / "raw/openpowerlifting-2025-05-31-c2a0b8b0.csv"`. Once everything is name correctly, run the script.

To run the script, `cd` into the [`powerstats/scripts`](../scripts/) directory and run `python cleaning_pipeline.py`.

### Where to place the SQL database

The SQL database should download at
`DB_FILE = DATA_DIR / "sqlite/powerlifting.db"`. That is, it should download to `powerstats/data/sqlite/powerlifting.db`.
If it does not download here, please move it as the other scripts expect it to be here.

### Metadata

The metadata for this database is the same as the original raw data. Look under [`powerstats/data/raw/raw_metadata.md`](raw/raw_metadata.md) to find it. The schema of the database is under [`powerstats/data/sqlite/schema.txt`](sqlite/schema.txt).

### Examples

You can find example data under [`powerstats/data/sqlite/sqlite_example.md`](sqlite/sqlite_example.md).
