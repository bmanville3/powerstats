# Overview

This repo contains my project for CS4365/6365 Introduction to Enterprise Computing (Su’2025) at Georgia Tech.

## Project Goal

The goal of this project is to derive a data driven algorithm to predict drug-use in raw powerlifting.

## Final Report

[Final Report](./final_report/CS_4365___Final_Project___Powerstats.pdf)

## Running Python Files

It is recommend to run all files in this [`powerstats/src/`](./src/) as a module from the `powerstats/` directory. Python's module resolver can be frustrating sometimes when you try to run something directly. Running `python src/main.py` is almost certainly going to throw errors about not finding a package. To fix this, run `python -m src.main`.

## Getting started

It is recommended to read this entire README before jumping into thing.

### Video Presentation + Demo

[https://youtu.be/6kNLL7KJAYY](https://youtu.be/6kNLL7KJAYY)

There are timestamps marking the presentation end the demo start.

### The Main File
[`powerstats/src/main.py`](./src/main.py) is the main runner for this project and has a CLI explaining components of the project. Please resort to it for running all analyses (run `python -m src.main --help` from `powerstats/` for help).

### The GUI
[`powerstats/src/gui.py`](./src/gui.py) will run a GUI to input user data into. The GUI is easy to use and self documenting. Simply enter each result from a user as the fields request, select which model to use, and click the "Calculate" button. This will run the inputted data through the selected model and output a probability from 0 to 1 of the user using drugs.

Note: A date is asked to be inputted with each result, but the date itself does not matter as long as they give the correct ordering of results. That is, if Y happened before X, then it should be date(Y) is before date(X) but it does not matter exactly what date(Y) or date(X) is.

### Running an LLM on the GUI

To run an LLM on the GUI, you need to edit the [`powerstats/openai_config.env`](./openai_config.env) file and fill in the appropriate fields. If you choose to use OpenAI to host your LLM, you will need to add your API key. If you choose to host it locally, you will need to add the local URL to your server (note this has not been tested - code may need to be changed for this).

### Getting the dataset
The dataset can be found at [https://openpowerlifting.gitlab.io/opl-csv/](https://openpowerlifting.gitlab.io/opl-csv/). For more information, see [`powerstats/data/README.md`](./data/README.md). For more links, see [`powerstats/data/raw/additional_links.md`](./data/raw/additional_links.md).

### Loading the Dataset
 For information on loading the dataset, see [`powerstats/data/README.md`](./data/README.md).


### Dependencies
All dependencies have been listed in [`requirements.txt`](./requirements.txt). For reproducibility, the exact versions have also been given. Please install these dependencies before continuing.

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

## Results from the Models

Graphical results from the models can be found at [`powerstats/graphs/models/`](./graphs/models/). For an explanation of the results, see [`powerstats/graphs/models/README.md`](./graphs/models/README.md).

## License

This page uses data from the OpenPowerlifting project, https://www.openpowerlifting.org.
You may download a copy of the data at https://gitlab.com/openpowerlifting/opl-data.
