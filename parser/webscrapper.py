## imports
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np

## URL Specification
URL = "https://olympics.com/tokyo-2020/olympic-games/en/results/all-sports/medal-standings.htm"
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
print("Full Data")
print(df.head())

national_level = []
for link in individuallinks[0:2]:
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
    national_level.append([link[1], df])
print("Nation: ", national_level[0][0])
print("DF: \n", national_level[0][1])
