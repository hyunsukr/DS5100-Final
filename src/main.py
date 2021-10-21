from utils.webscrapper import Web_Scrapper
import pandas as pd

def main():
    scrapper = Web_Scrapper()
    national_src = scrapper.scrape_summary("medal-standings.htm")
    national_src.to_csv('country.csv')
    # print(summary_df)
    # scrapper.scrape_country(national_src)
    # single_USA = scrapper.get_country_df("United States of America")
    # print(single_USA)


main()