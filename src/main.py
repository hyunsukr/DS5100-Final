from utils.webscrapper import Web_Scrapper
from utils.cleaner import Cleaner
import pandas as pd
import numpy as np

def main():
    ## Create the helper classes
    print("Kicking off Data Pipeline \n")
    scrapper = Web_Scrapper()
    mapper_class = Cleaner()

    ## Pull the historical data from the olympics website
    print("Collecting Historical Olympic Data \n")
    history = scrapper.scrape_history()
    history = mapper_class.convert_continent(history)
    history.to_csv('data/time_series.csv')

    ## Collect historical data from the historical GDP website.
    print("Collecting Historical GDP Data \n")
    gdp_history = scrapper.scrape_gdp_history(list(np.unique(history["Year"])))

    gdp_history.to_csv('data/gdp_timeseries.csv')

    ## Merge the GDP data with Olympic History 
    ## Both GDP and Olympic are from the historical sources
    print("Mergeing GDP with Olympic History\n")
    joined_history = mapper_class.join_gdp(gdp_history, history,['Country','Year'])
    joined_history.to_csv('data/history_olympic_with_gdp.csv')

    ## Focus in on Tokyo Olympics
    print("Kicking off most recent tokyo dataset with updated GDP databse\n")
    ## Web Scrape the olympics 2020 Tokyo Olympics
    national_src = scrapper.scrape_summary('https://olympics.com/en/olympic-games/tokyo-2020/medals')
    national_src.to_csv('data/country.csv')

    ## Scrape the GDP data (most recent GDP)
    gdp = scrapper.scrape_gdp()
    gdp.to_csv("data/gdp.csv")

    ## Conduct data engineering
    mapper_class = Cleaner()
    joined_df = mapper_class.join_gdp(gdp, national_src)
    joined_df.to_csv("data/country_medal_gdp.csv")

    teams = pd.read_excel("src/resources/Teams.xlsx")
    maps = mapper_class.join_aggregate_teams(teams, joined_df)
    maps.to_csv("data/teams_country_gdp.csv")

    continent_addition = mapper_class.convert_continent(maps)

    continent_addition.to_csv("data/final_olympic_cont.csv")
    print("Finished Data Processing")


if __name__ == "__main__":
    main()