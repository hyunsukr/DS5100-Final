## imports
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
from progressbar import ProgressBar
pbar = ProgressBar()

class Web_Scrapper():
    def __init__(self, baselink="https://olympics.com/tokyo-2020/olympic-games/en/results/all-sports/", country={}):
        self.baselink = baselink
        self.country = country
    
    def scrape_summary(self, url_query):
        """
        A method to scrape the table data from the https://olympics.com/tokyo-2020/olympic-games/en/results/all-sports/medal-standings.htm
        The data will be a summary table with each countries gold, silver, and bronze medal pulled.

        :param: url_query <string> = the endpoint of the url

        :returns: <dataframe> = A data frame containing the summary statistics of each country and medals earned.
        """
        URL = self.baselink + url_query
        r = requests.get(URL)
        # Read the data content as html
        soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
        # Get the ul tag by the id specific for the 7 day forcast
        table = soup.find("table", {"id": "medal-standing-table"})
        parsed_rows = []
        individuallinks = []
        for row in table.findAll("tr"):
            temp = []
            table_elements = row.findAll("td")
            for el in range(0, len(table_elements)):
                text_element = table_elements[el].get_text().replace("\n", '')
                temp.append(text_element)
                if el == 1:
                    link = table_elements[el].find("a", href=True)
                    link = 'https://olympics.com/tokyo-2020/olympic-games/en/results/all-sports/' + link["href"].split('/')[-1]
                    individuallinks.append([link, text_element])
            parsed_rows.append(temp)

        columns = ["Rank", "Team/NOC", "Gold", "Silver", "Bronze", "Total", "Rank by Total", "Abbreviation"]
        df = pd.DataFrame(parsed_rows[1:], columns = columns)
        return individuallinks, df

    def scrape_country(self, country):
        """
        A method to gather more specific information about the medals earned for each country. The parser will gather information about
        which sport recieved which medal for each country.

        The parser will update the class's dictionary, which is a key value mapping where the key is the name of the country and the
        value is the dataframe containing the information for that country. 

        :param: country <List<List<URL, Country Name>> : A list of lists that is composed of the url for the soruce and country name

        :return: None
        """
        for link in pbar(country):
            r = requests.get(link[0])
            # Read the data content as html
            soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
            # Get the ul tag by the id specific for the 7 day forcast
            table = soup.find("table")
            nation_entries = []
            rows = table.findAll("tr")
            for i in range(0,len(rows) -1):
                temp = []
                sportCol = rows[i].findAll('th')[0].get_text().replace("\n","")
                temp.append(sportCol)
                table_elements = rows[i].findAll("td")
                for el in range(0, len(table_elements)):
                    text_element = table_elements[el].get_text().replace("\n", '')
                    temp.append(text_element)
                nation_entries.append(temp)
            columns = ["Discipline", "F", "M", "Total"]
            df = pd.DataFrame(nation_entries[1:], columns = columns)
            self.country[link[1]] = df
    

    def get_country_df(self, country):
        """
        A getter method for the countries individual winnings

        :param: country <string> = Key being used to get the value from the dicitionary

        :return: Dataframe = The dataframe for medal winnings for the parameter country
        """
        return self.country[country]
