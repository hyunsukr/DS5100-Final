import pandas as pd

class Cleaner():
    def __init__(self, mapping):
        self.country_maps = mapping

    def join_gdp(self, gdp, olympic):
        temp_olympic = olympic.copy()
        # temp_olypmic["Country"] = temp_olypmic["Name"].str[3:].map(self.country_maps)
        temp_olympic["Country"] = temp_olympic["Name"].str[4:].map(self.country_maps)
        joined = pd.merge(temp_olympic, gdp, how='left', on='Country')
        return joined

    