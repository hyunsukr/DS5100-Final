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

Terminal output 
```
tests/utils/test_cleaner.py::test_join_gdp_single PASSED [  9%]
tests/utils/test_cleaner.py::test_get_continents_map PASSED [ 18%]
tests/utils/test_cleaner.py::test_get_continents_map_exceptions PASSED [ 27%]
tests/utils/test_cleaner.py::test_convert_continent PASSED [ 36%]
tests/utils/test_cleaner.py::test_convert_continent_not_available PASSED [ 45%]
tests/utils/test_cleaner.py::test_join_gdp PASSED [ 54%]
tests/utils/test_cleaner.py::test_join_aggregate_teams PASSED [ 63%]
tests/utils/test_webscrapper.py::test_scrape_gdp PASSED [ 72%]
tests/utils/test_webscrapper.py::test_scarpe_summary PASSED [ 81%]
tests/utils/test_webscrapper.py::test_scrape_gdp_history PASSED [ 90%]
tests/utils/test_webscrapper.py::test_scrape_history PASSED [100%]
```

Currently the repo is performing as follows.

| Name | Stmts | Miss | Cover|
| :--- | :---: | :---: | :--: |
| src/__init__.py | 0 | 0 | 100% |
| src/main.py | 34  | 34 | 0 |
| src/utils/__init__.py | 0 | 0 | 100% |
| src/utils/cleaner.py | 50 | 0 | 100% |
| src/utils/webscrapper.py  | 135 | 0 | 100% |
| TOTAL | 219 | 24 | 84% |


After running the code, you may deactivate the virtual env by running the following.
```
deactivate
```


## How to Run the datapull
To start the data pull and gather all Tokyo Olympic data you must run the main.py file after activating the virtual environments.

```
python src/main.py 
```
