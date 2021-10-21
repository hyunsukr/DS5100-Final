from utils.webscrapper import Web_Scrapper
import pandas as pd

def main():
    scrapper = Web_Scrapper()
    national_src = scrapper.scrape_summary("medal-standings.htm")
    national_src.to_csv('country.csv')
    gdp = scrapper.scrape_gdp()
    gdp.to_csv("gdp.csv")

main()