import pandas as pd
import pycountry_convert as pc
import json


class Cleaner():
    def __init__(self):
        # Opening JSON Mapping file
        with open('src/resources/mapping.json') as json_file:
            mapping = json.load(json_file)

        with open('src/resources/mapping_continents.json') as json_file:
            cont_map = json.load(json_file)

        self.continent_maps = cont_map
        self.country_maps = mapping

    def join_gdp(self, gdp, olympic):
        temp_olympic = olympic.copy()
        temp_olympic["Country"] = temp_olympic["Name"].str[4:].map(self.country_maps)
        joined = pd.merge(temp_olympic, gdp, how='left', on='Country')
        return joined

    def join_aggregate_teams(self, teams, olympic):
        teams = teams.groupby("NOC")["Discipline"].count().reset_index()
        temp = olympic.copy()
        temp['tempName'] = temp["Name"].str[4:]
        joined = pd.merge(temp, teams, how='inner', left_on='tempName', right_on='NOC')
        joined = joined.drop(columns=["tempName"])
        return joined
    
    def get_continents_map(self, name):
        try:
            country_code = pc.country_name_to_country_alpha2(name, cn_name_format="default")
            continent_name = pc.country_alpha2_to_continent_code(country_code)
            return continent_name
        except:
            if name == 'ROC' or name == "Republic of Korea" or name == "Chinese Taipei" or name == "Hong Kong, China":
                return "AS"
            else:
                return "Not Available"

    def get_full_continent_map(self, code):
        try:
            return self.continent_maps[code]
        except:
            return 'Not Available'

    def convert_continent(self, dataframe):
        continents = dataframe["NOC"].map(lambda x: self.get_continents_map(x)).map(lambda x: self.get_full_continent_map(x))
        new_final = dataframe.copy()
        new_final["Continents"] = continents
        return new_final


