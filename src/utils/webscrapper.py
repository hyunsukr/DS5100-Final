## imports
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
from progressbar import ProgressBar
pbar = ProgressBar()
import json

class Web_Scrapper():
    def __init__(self, baselink="https://olympics.com/tokyo-2020/olympic-games/en/results/all-sports/", history = {}):
        self.baselink = baselink
        with open('src/resources/history.json') as json_file:
            history = json.load(json_file)
        self.history = history
    
    def scrape_gdp(self):
        URL = "https://www.worldometers.info/gdp/gdp-by-country/" # specify URL of website we want to scrape
        r = requests.get(URL) #http requests tot ehs specified url and save it in R
        soup = BeautifulSoup(r.content, 'html5lib')
        templist = []
        # Locating the table on the website 
        table = soup.find_all('table')[0]
        # using a for loop to iterate over the columns in the table to
        # generate the text 
        for child in soup.find_all('table')[0].children:
            for td in child:
                for tr in td:
                    if not isinstance(tr, str):
                        templist.append(tr.get_text())
        country = []
        vals = []
        other_val = []
        percent = []
        temp = []
        other = []
        for i in range(0,len(templist[9:])):
            if i % 8 == 0:
                country.append(templist[9:][i])
            elif i%8 == 1:
                vals.append(templist[9:][i])
            elif i%8 == 2:
                other_val.append(templist[9:][i])
            elif i%8 == 3:
                percent.append(templist[9:][i])
            elif i%8 == 4:
                temp.append(templist[9:][i])
            elif i%8 == 5:
                other.append(templist[9:][i])
            d = {'Country': country, 'GDP': vals,'GDP abbreviated': other_val,'GDP growth': percent,'Population': temp,'GDP per capita': other}
        df = pd.DataFrame(d)
        return df
    
    def scrape_history(self):
        ## Not Tested Yet
        time_series = pd.DataFrame()
        for i in pbar(self.history.values()):
            df = self.scrape_summary(i)
            df["Year"] = i.split('/')[5].split('-')[-1]
            df["Location"] = "".join(i.split('/')[5].split('-')[:-1]).upper()
            time_series = time_series.append(df)

        time_series["NOC"] = time_series["Name"].str[4:]
        return time_series



    def scrape_summary(self, url_query):
        """
        A method to scrape the table data from the https://olympics.com/tokyo-2020/olympic-games/en/results/all-sports/medal-standings.htm
        The data will be a summary table with each countries gold, silver, and bronze medal pulled.

        :param: url_query <string> = the endpoint of the url

        :returns: <dataframe> = A data frame containing the summary statistics of each country and medals earned.
        """
        r = requests.get(url_query)
        # Read the data content as html
        soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
        # Get the ul tag by the id specific for the 7 day forcast
        countries = soup.find_all("div", {"class" : 'styles__CountryWrapper-sc-fehzzg-4 dVfDKJ'})
        medals = soup.find_all("div", {"class" : 'Medalstyles__Wrapper-sc-1tu6huk-0 kXFxTL'})
        data = []
        for i in range(0, len(countries)):
            data.append([countries[i].get_text(), \
                            medals[i*4].get_text() if medals[i*4].get_text() != '-' else 0, \
                            medals[i*4 + 1].get_text() if medals[i*4 + 1].get_text() != '-' else 0, \
                            medals[i*4 + 2].get_text() if medals[i*4 + 2].get_text() != '-' else 0, \
                            medals[i*4 + 3].get_text() if medals[i*4 + 3].get_text() != '-' else 0]) 
        df = pd.DataFrame(data, columns = ['Name', 'Gold', 'Silver', 'Bronze', 'Total'])
        return df
    
