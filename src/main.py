from utils.webscrapper import Web_Scrapper
from utils.cleaner import Cleaner
import pandas as pd
import json

def main():
    scrapper = Web_Scrapper()
    national_src = scrapper.scrape_summary("medal-standings.htm")
    national_src.to_csv('country.csv')
    gdp = scrapper.scrape_gdp()
    gdp.to_csv("gdp.csv")
    # Opening JSON Mapping file
    with open('mapping.json') as json_file:
        data = json.load(json_file)
    
        country_mapping = data

    mapper_class = Cleaner(data)
    joined_df = mapper_class.join_gdp(gdp, national_src)
    joined_df.to_csv("country_medal_gdp.csv")


main()