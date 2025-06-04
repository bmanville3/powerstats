# Overview

This repo contains my project for CS4365/6365 Introduction to Enterprise Computing (Su’2025) at Georgia Tech

## Pre-commit
### Set-up

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
