## Methods to test the webscrapper class

from src.utils.webscrapper import Web_Scrapper
import pandas as pd

from src.utils.cleaner import Cleaner
import pandas as pd

def test_scrape_gdp():
    webscrapper = Web_Scrapper()
    scrapped_gdp = webscrapper.scrape_gdp()
    gdp = scrapped_gdp["GDP"].map(lambda x: int(x[1:].replace(",","")))
    pop = scrapped_gdp["Population"].map(lambda x: int(x.replace(",","")))
    gdp_per_cap = round(gdp/pop).astype(int)
    
    pulled_gdp_per_cap = scrapped_gdp["GDP per capita"].map(lambda x: int(x[1:].replace(",","")))
    assert set(scrapped_gdp.columns) == set(['Country', 'GDP', 'GDP abbreviated', 'GDP growth', 'Population', 'GDP per capita'])
    assert scrapped_gdp.equals(scrapped_gdp.dropna())
    assert gdp_per_cap.equals(pulled_gdp_per_cap)


def test_scarpe_summary():
    webscrapper = Web_Scrapper()
    scrapped_olympic = webscrapper.scrape_summary('https://olympics.com/en/olympic-games/tokyo-2020/medals')

    computed_total = scrapped_olympic["Gold"].astype(int) + scrapped_olympic["Silver"].astype(int) + scrapped_olympic["Bronze"].astype(int)

    sanity_check_medal_count = sum(scrapped_olympic["Total"].astype(int) > 500)

    assert set(scrapped_olympic) == set(['Name', 'Gold', 'Silver', 'Bronze', 'Total'])
    assert scrapped_olympic.equals(scrapped_olympic.dropna())
    assert computed_total.equals(scrapped_olympic["Total"].astype(int))
    assert sanity_check_medal_count == 0

def test_scrape_history():
    webscrapper = Web_Scrapper()
    history = webscrapper.scrape_history()

    computed_total = history["Gold"].astype(int) + history["Silver"].astype(int) + history["Bronze"].astype(int)

    sanity_check_medal_count = sum(history["Total"].astype(int) > 500)

    assert set(history.columns) == set(['Name','Gold','Silver','Bronze','Total','Year','Location','NOC'])
    assert computed_total.equals(history["Total"].astype(int))
    assert sanity_check_medal_count == 0


    