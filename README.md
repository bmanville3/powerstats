# Overview

This repo contains my project for CS4365/6365 Introduction to Enterprise Computing (Su’2025) at Georgia Tech.

## Project Goal

The goal of this project is to derive a data driven algorithm to predict drug-use in raw powerlifting.

## Running Python Files

It is recommend to run all files in this [`powerstats/src/`](./src/) directory with the `-m` flag. Python's module resolver can be frustrating sometimes when you try to run something directly. Running `python src/main.py` is almost certainly going to throw errors about not finding a package. To fix this, run `python -m src.main`. It is recommended to run all files in this directory from the `powerstats/` directory.

The scripts in [`powerstats/scripts/`](./scripts/) should be directly runnable with `python {script_name}`. It is recommended to run these files directly in the `powerstats/scripts/` directory without the `-m` flag.

## Getting started

### The Main File
[`powerstats/src/main.py`](./src/main.py) is the main runner for this project. Please resort to it for running all anlyses. Pass the `--help` flag when running it to see what all can be done. It is recommended to run it like `python -m src.main` from the `powerstats/` directory.

### Getting the dataset
The dataset can be found at [https://openpowerlifting.gitlab.io/opl-csv/](https://openpowerlifting.gitlab.io/opl-csv/). For more information, see [`powerstats/data/README.md`](./data/README.md). For more links, see [`powerstats/data/raw/additional_links.md`](./data/raw/additional_links.md).

### Scripts - Loading the Dataset
Besides from `main.py`, there are also some scripts at [`powerstats/scripts/`](./scripts/) that must be run. The main script that need to be ran is [`powerstats/scripts/cleaning_pipeline.py`](./scripts/cleaning_pipeline.py) to load the dataset. For more information on loading the dataset, see [`powerstats/data/README.md`](./data/README.md). For more information on scripts, see [`powerstats/scripts/README.md`](./scripts/README.md).


### Dependencies
All dependencies have been listed in [`requirements.txt`](./requirements.txt). For reproducability, the exact versions have also been given. Please install these dependencies before continuing.

### Pre-commit Set-up

1) Pip install the requirements which will install `pre-commit`:
```
pip install -r requirements.txt
```

2) Once `pre-commit` is installed, run the following command to configure the pre-commit hook.
```
pre-commit install
```

3) Now when typing `git commit`, `pre-commit` will run on all staged files. To run on all files in the project, run
```
pre-commit run --all-files
```

## License

This page uses data from the OpenPowerlifting project, https://www.openpowerlifting.org.
You may download a copy of the data at https://gitlab.com/openpowerlifting/opl-data.
