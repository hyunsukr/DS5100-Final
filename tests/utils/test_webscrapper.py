## Methods to test the webscrapper class

from src.utils.webscrapper import Web_Scrapper
import pandas as pd

def test_scrape_gdp():
    """
    Test the web scraper method for scrapping the most recent GDP data.
    """
    webscrapper = Web_Scrapper()
    scrapped_gdp = webscrapper.scrape_gdp()
    gdp = scrapped_gdp["GDP"].map(lambda x: int(x[1:].replace(",","")))
    pop = scrapped_gdp["Population"].map(lambda x: int(x.replace(",","")))
    gdp_per_cap = round(gdp/pop).astype(int)
    
    pulled_gdp_per_cap = scrapped_gdp["GDP per capita"].map(lambda x: int(x[1:].replace(",","")))
    
    ## Make sure the data pulled was correctly calculated based on definition
    assert set(scrapped_gdp.columns) == set(['Country', 'GDP', 'GDP abbreviated', 'GDP growth', 'Population', 'GDP per capita'])
    assert scrapped_gdp.equals(scrapped_gdp.dropna())
    assert gdp_per_cap.equals(pulled_gdp_per_cap)


def test_scarpe_summary():
    """
    Test the 2021 Tokyo Olympics Web Scrapping Method
    """
    webscrapper = Web_Scrapper()
    scrapped_olympic = webscrapper.scrape_summary('https://olympics.com/en/olympic-games/tokyo-2020/medals')

    computed_total = scrapped_olympic["Gold"].astype(int) + scrapped_olympic["Silver"].astype(int) + scrapped_olympic["Bronze"].astype(int)

    sanity_check_medal_count = sum(scrapped_olympic["Total"].astype(int) > 500)

    ## Dimension check
    assert set(scrapped_olympic) == set(['Name', 'Gold', 'Silver', 'Bronze', 'Total'])
    assert scrapped_olympic.equals(scrapped_olympic.dropna())

    ## Make sure total was calculated correctly by the offical olympic website
    assert computed_total.equals(scrapped_olympic["Total"].astype(int))
    assert sanity_check_medal_count == 0

def test_scrape_gdp_history():
    """
    Test scrapping historical GDP
    """
    webscrapper = Web_Scrapper()
    history = webscrapper.scrape_gdp_history(['2020','1961'])

    # Make sure that the dataframe does not include years that were not given to the method
    assert sum(history["Year"].astype(int) < 1961) == 0

    # Make sure that no more than 500 countries were pulled (quality check)
    assert history.shape[0] < 500

def test_scrape_history():
    """
    Test historical olympic web scrapping.
    All Summer olympics were pulled from the offical olympics website.
    """
    webscrapper = Web_Scrapper()
    history = webscrapper.scrape_history()

    # Compute the total number of medals based on data pulled
    computed_total = history["Gold"].astype(int) + history["Silver"].astype(int) + history["Bronze"].astype(int)

    sanity_check_medal_count = sum(history["Total"].astype(int) > 500)

    # Dimension check
    assert set(history.columns) == set(['Name','Gold','Silver','Bronze','Total','Year','Location','NOC'])
    
    # Data quality check of total medals summing to the correct amount
    assert computed_total.equals(history["Total"].astype(int))

    # Data quality check that no country had more than 500 medals.
    assert sanity_check_medal_count == 0
