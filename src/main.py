from utils.webscrapper import Web_Scrapper
from utils.cleaner import Cleaner
import pandas as pd

def main():
    scrapper = Web_Scrapper()
    national_src = scrapper.scrape_summary("medal-standings.htm")
    national_src.to_csv('data/country.csv')
    gdp = scrapper.scrape_gdp()
    gdp.to_csv("data/gdp.csv")

    mapper_class = Cleaner()
    joined_df = mapper_class.join_gdp(gdp, national_src)
    joined_df.to_csv("data/country_medal_gdp.csv")

    teams = pd.read_excel("src/resources/Teams.xlsx")
    maps = mapper_class.join_aggregate_teams(teams, joined_df)
    maps.to_csv("data/teams_country_gdp.csv")

    continent_addition = mapper_class.convert_continent(maps)

    continent_addition.to_csv("data/final_olympic_cont.csv")
    print("Finished Data Processing")


main()