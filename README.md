# DS5100-Final

This repo is for the final project for DS5100 for the Online MSDS proogram. 


## Inital Analysis
Exploratory Analysis can be found in the notebook pathed `analysis/jupyter_notebooks_eda.ipynb`

Regression Analysis of notebooks can be found in the notebook pathed `analysis/jupyter_notebooks/regression.ipynb`

Any pictures or resources generated from the notebooks can be downloaded in the folder pathed `analysis/resources/`



## Setting up and running the datapull
The repo is configured to use a virtual environment for the sake of package dependencies. Please run the commandas to set up the virtual env.
```
python -m venv venv
source venv/bin/actiavte
pip install -r requirments.txt 
```

To run tests for the repo please use the commands.
```
pytest --cov=src/ tests/ -vv
```

Currently the repo is performing as follows.

| Name | Stmts | Miss | Cover|
| :--- | :---: | :---: | :--: |
| src/__init__.py | 0 | 0 | 100% |
| src/main.py | 19  | 19 | 0 |
| src/utils/__init__.py | 0 | 0 | 100% |
| src/utils/cleaner.py | 50 | 0 | 100% |
| src/utils/webscrapper.py  | 66 | 0 | 100% |
| TOTAL | 139 | 23 | 83% |


After running the code, you may deactivate the virtual env by running the following.
```
deactivate
```


## How to Run the datapull
To start the data pull and gather all Tokyo Olympic data you must run the main.py file after activating the virtual environments.

```
python src/main.py 
```
