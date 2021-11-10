from utils.webscrapper import Web_Scrapper
from utils.cleaner import Cleaner
import pandas as pd
import numpy as np

def main():
    print("Kicking off Data Pipeline \n")
    scrapper = Web_Scrapper()
    mapper_class = Cleaner()

    ## History
    print("Collecting Historical Olympic Data \n")
    history = scrapper.scrape_history()
    history = mapper_class.convert_continent(history)
    history.to_csv('data/time_series.csv')

    ## History GDP
    print("Collecting Historical GDP Data \n")
    gdp_history = scrapper.scrape_gdp_history(list(np.unique(history["Year"])))

    gdp_history.to_csv('data/gdp_timeseries.csv')

    ## Merging GDP with History
    print("Mergeing GDP with Olympic History\n")
    joined_history = mapper_class.join_gdp(gdp_history, history,['Country','Year'])
    joined_history.to_csv('data/history_olympic_with_gdp.csv')

    ## Tokyo
    print("Kicking off most recent tokyo dataset with updated GDP databse\n")
    national_src = scrapper.scrape_summary('https://olympics.com/en/olympic-games/tokyo-2020/medals')
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


if __name__ == "__main__":
    main()