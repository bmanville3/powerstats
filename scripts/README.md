# Scripts
There are two scripts right now: [`powerstats/scripts/cleaning_pipeline.py`](./cleaning_pipeline.py) and [`powerstats/scripts/generate_database_classes.py`](./generate_database_classes.py).

## cleaning_pipeline.py
This script needs to be ran initially after downloading the dataset. It is responsible for loading the sqlite3 database. For more instructions, see [`powerstats/data/README.md`](../data/README.md).

## generate_database_classes.py

This script does not need to be ran as it has already been done. It is responsible for generate [DTOs](../src/models/dto/) and [table wrapper class](../src/database/tables/dto_table/).