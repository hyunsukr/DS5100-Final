import pandas as pd
import pycountry_convert as pc
import json


class Cleaner():
    def __init__(self):
        """
        class init.
        """
        # Opening JSON Mapping file
        with open('src/resources/mapping.json') as json_file:
            mapping = json.load(json_file)

        with open('src/resources/mapping_continents.json') as json_file:
            cont_map = json.load(json_file)

        self.continent_maps = cont_map
        self.country_maps = mapping

    def join_gdp(self, gdp, olympic, join_cols=['Country']):
        """
        Merges the GDP dataframe with the olympic data frame based on the country name

        :param: gdp <dataframe> = a pandas dataframe that has the scrapped data from the recent GDP website.
        :param: olympic <dataframe> = a pandas dataframe that has teh scrapped olympic data. 

        :returns: <dataframe> = A merged dataframe that all the information from gdp and olympic data.
        """
        temp_olympic = olympic.copy()
        ## Rename the country based on maps as shown in src/resources/mapping.json
        temp_olympic["Country"] = temp_olympic["Name"].str[4:].map(self.country_maps)
        joined = pd.merge(temp_olympic, gdp, how='left', on=join_cols)
        return joined

    def join_aggregate_teams(self, teams, olympic):
        """
        Merges the team information for each country with the olympic dataframe.
        The team dataframe was pulled from kaggle due to the olympic website being redesigned recently.

        :param: teams <dataframe> = a pandas dataframe that has the participating teams for each country in the 2021 Tokyo Olympics
        :param: olympic <dataframe> = a pandas dataframe that had medal count and other information related to olympics

        :returns: <dataframe> = A merged dataframe with a summary of how many teams there were for each country. 
        """
        ## Collect how many teams were associated with each country.
        teams = teams.groupby("NOC")["Discipline"].count().reset_index()
        temp = olympic.copy()
        temp['tempName'] = temp["Name"].str[4:]
        joined = pd.merge(temp, teams, how='inner', left_on='tempName', right_on='NOC')
        joined = joined.drop(columns=["tempName"])
        return joined
    
    def get_continents_map(self, name):
        """
        Getter method to get the continent based on a country

        :param: name <string> = name of the country

        :returns: <string> Returns the contient associated with the country
        """
        try:
            country_code = pc.country_name_to_country_alpha2(name, cn_name_format="default")
            continent_name = pc.country_alpha2_to_continent_code(country_code)
            return continent_name
        ## Some names have different names from the package that was utilized
        ## Except claus has all the countries that didn't have a 1 : 1 mapping to the pycountry package.
        except:
            if name in ['ROC',"Republic of Korea","Chinese Taipei","Hong Kong, China","Soviet Union","United Arab Republic"]:
                return "AS"
            elif name in ["German Democratic Republic (Germany)", "Yugoslavia", "Czechoslovakia", "Kosovo", "Serbia and Montenegro", "Bohemia"]:
                return "EU"
            elif name in ["Virgin Islands, US","West Indies Federation"]:
                return "NA"
            elif name in ['Netherlands Antilles']:
                return 'SA'
            elif name in ['Australasia']:
                 return "OC"
            else:
                return "Not Available"

    def get_full_continent_map(self, code):
        """
        Getter method to get the actual continent from the continent code from the src/resources/mapping_continents.json file.

        :param: code <string> the continent code

        :returns: <string> = the actual contient where AS will give a country code of ASIA
        """
        try:
            return self.continent_maps[code]
        except:
            return 'Not Available'

    def convert_continent(self, dataframe):
        """
        Method to kick off all the functions for generating the continent each country is in.
        First get the continent code from get_contients_map, then get the full name from full_continent_map

        :param: dataframe <dataframe> a dataframe contianing the NOC column, which has the country name from the olympics website

        :returns: <dataframe> a dataframe with a new column created called Continents.
        """
        continents = dataframe["NOC"].map(lambda x: self.get_continents_map(x)).map(lambda x: self.get_full_continent_map(x))
        new_final = dataframe.copy()
        new_final["Continents"] = continents
        return new_final


