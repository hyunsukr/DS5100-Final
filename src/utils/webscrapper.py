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
        """
        Class init.
        """
        self.baselink = baselink
        with open('src/resources/history.json') as json_file:
            history = json.load(json_file)
        self.history = history
    
    def scrape_gdp_history(self, years):
        """
        Method to kick off data pull for the years that the olympic data pull was pulled for.

        :param: years <list> = A list containig the years that the script needs to pull GDP data for. 

        :returns: <dataframe> = A data frame for each countries GDP, GDP growth, and all the years that the user inserted. 
        """
        time_series = pd.DataFrame()
        pbar.start()
        for i in pbar(range(0,len(years))):
            if int(years[i]) > 1949:
                df = self.scrape_gdp_economy(years[i])
                time_series = time_series.append(df)

        return time_series


    def scrape_gdp_economy(self, year):
        """
        A method to scrape the table data for historical data.
        The data will be a summary table with of each countries GDP, GDP growth, and Year

        :param: year <string> = Year to pull. The parameter 2020 will pull the GDP related information for the year 2020

        :returns: <dataframe> = A data frame containing the summary statistics of each countries GDP, GDP growth, and Year
        """
        URL = 'https://countryeconomy.com/gdp?year=' + year
        r = requests.get(URL) #http requests tot ehs specified url and save it in R
        soup = BeautifulSoup(r.content, 'html5lib')
        tables = soup.find_all('table', {'id':'tbA'})
        tables_percap = soup.find_all('table', {'id':'tbPC'})
        tempList = []
        for table in tables:
            for child in table.children:
                for td in child:
                    for tr in td:
                        tempList.append(tr.get_text())
        
        second_tempList = []
        for table in tables_percap:
            for child in table.children:
                for td in child:
                    for tr in td:
                        second_tempList.append(tr.get_text())
        tempList = tempList[5:len(tempList)-1]
        second_tempList = second_tempList[6:len(second_tempList) - 1]

        country = []
        year = []
        amount = []
        growth = []

        country_percap = []
        year_percap = []
        amount_percap = []
        growth_percap = []
        
        for i in range(0,len(tempList)):
            if i % 8 == 0:
                country.append(" ".join(tempList[i].split()[:-1]))
            elif i % 8 == 1:
                year.append(tempList[i])
            elif i % 8 == 4:
                if tempList[i] == '':
                    amount.append('$0M')
                else:
                    amount.append(tempList[i])
            elif i % 8 == 6:
                growth.append(tempList[i])
        
        for i in range(0,len(second_tempList)):
            if i % 10 == 0:
                country_percap.append(" ".join(second_tempList[i].split()[:-1]))
            elif i % 10 == 1:
                year_percap.append(second_tempList[i])
            elif i % 10 == 4:
                if second_tempList[i] == '':
                    amount_percap.append('$0')
                else:
                    amount_percap.append(second_tempList[i])
            elif i % 10 == 8:
                growth_percap.append(second_tempList[i])

        d = {'Country': country, 'GDP': amount,'GDP growth': growth, 'Year': year}
        df = pd.DataFrame(d)

        d_percap = {'Country': country_percap, 'Year': year_percap, 'GDP per capita': amount_percap,'GDP per capita growth': growth_percap}
        df_percap = pd.DataFrame(d_percap)
        ## Remove Data Quality Issue
        df = df[df["Country"] != 'Liechtenstein']
        df_percap = df_percap[df_percap["Country"] != 'Liechtenstein']

        ## Change to numeric
        df["GDP"] = df["GDP"].map(lambda x: int(x[1:].replace(",","").replace('M',''))*1000000)

        ## Change to numeric
        df_percap["GDP per capita"] = df_percap["GDP per capita"].map(lambda x: int(x[1:].replace(",","")))

        merged = pd.merge(df, df_percap, how='inner', on=['Country','Year'])
        return merged
    
    def scrape_gdp(self):
        """
        Method to scrap the most recent GDP data.

        :returns: <dataframe> = A dataframe that has each countries name and GDP (GDP, GDP abbreviated, GDP growth, Population, GDP per capita)
        """
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
        ## Lists to capture row data
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
        """
        A method to scrape the historical data from the https://olympics.com/en/olympic-games
        This method gets all the links for all the summer olympics that have past.

        :returns: <dataframe> = A data frame containing the summary statistics of each country and medals earned for all summer olympic games
        """
        time_series = pd.DataFrame()
        pbar.start()
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
    
