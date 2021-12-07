## Methods to test the cleaner class

from src.utils.cleaner import Cleaner
import pandas as pd


def test_join_gdp_single():
    """
    Test when given a contient the correct continent is mapped based on the mapping_contients.json file in src/resources
    """
    cleaner = Cleaner()
    north_america = 'NA'
    continent = cleaner.get_full_continent_map(north_america)

    not_available = 'A wrong country code'
    incorrect_continent = cleaner.get_full_continent_map(not_available)

    assert continent == 'North America'
    assert incorrect_continent == 'Not Available'

def test_get_continents_map():
    """
    Test whether if in a different format we correctly say NA. United States is not a continent
    """
    cleaner = Cleaner()
    country_name = 'United States of America'
    continent_code = cleaner.get_continents_map(country_name)
    assert continent_code == 'NA'
    
def test_get_continents_map_exceptions():
    """
    Test the except clause of the get continents.
    There were many countries with different mappings from the olympics website, which was the motivation behind the except case.
    """
    cleaner = Cleaner()
    country_russia = 'ROC'
    continent_russia = cleaner.get_continents_map(country_russia)

    country_korea = "Republic of Korea"
    continent_korea = cleaner.get_continents_map(country_korea)

    country_not_real = 'Not a Real Country'
    continent_not_real = cleaner.get_continents_map(country_not_real)
    
    country_eu_pass = 'German Democratic Republic (Germany)'
    continent_eu_pass = cleaner.get_continents_map(country_eu_pass)

    country_na_pass = 'Virgin Islands, US'
    continent_na_pass = cleaner.get_continents_map(country_na_pass)

    country_sa_pass = 'Netherlands Antilles'
    continent_sa_pass = cleaner.get_continents_map(country_sa_pass)

    country_oc_pass = 'Australasia'
    continent_oc_pass = cleaner.get_continents_map(country_oc_pass)

    assert continent_russia == 'AS'
    assert continent_korea == 'AS'
    assert continent_eu_pass == 'EU'
    assert continent_na_pass == 'NA'
    assert continent_sa_pass == 'SA'
    assert continent_oc_pass == 'OC'
    assert continent_not_real == 'Not Available'

def test_convert_continent():
    """
    Check if the conutries are correctly mapped to their respective contients.
    """
    cleaner = Cleaner()
    sample_df = pd.DataFrame(['United States of America', 'Republic of Korea'], columns = ['NOC'])
    convert_names = cleaner.convert_continent(sample_df)

    correct_dataframe = pd.DataFrame([['United States of America', 'North America'], ['Republic of Korea', 'Asia']], columns = ['NOC', 'Continents'])

    # Check dataframe didn't change dimensions
    assert convert_names.shape == (2,2)
    assert convert_names.equals(correct_dataframe)

def test_convert_continent_not_available():
    """
    Check if incorrect country names will be mapped to not avaiable
    """
    cleaner = Cleaner()
    sample_df = pd.DataFrame(['United States of America', 'Republic of DS5100'], columns = ['NOC'])
    convert_names = cleaner.convert_continent(sample_df)

    correct_dataframe = pd.DataFrame([['United States of America', 'North America'], ['Republic of DS5100', 'Not Available']], columns = ['NOC', 'Continents'])

    # Check for no dimensional change
    assert convert_names.shape == (2,2)
    assert convert_names.equals(correct_dataframe)

def test_join_gdp():
    """
    Test the merge method in cleaner based on gdp.
    """
    cleaner = Cleaner()
    sample_df = pd.DataFrame([['USA United States of America', 10], ['CAN Canada',20], ['DS 5100Group',30]], columns = ['Name','Medal'])
    sample_gdp = pd.DataFrame([['United States', 100], ['Canada',100]], columns = ['Country', 'GDP'])
    joined_df = cleaner.join_gdp(sample_gdp, sample_df)

    correct_dataframe = pd.DataFrame([['USA United States of America', 10,'United States', 100], \
                                         ['CAN Canada',20,'Canada',100], \
                                         ['DS 5100Group',30, None, None]], columns = ['Name','Medal', 'Country', 'GDP'])

    # Dimension check
    assert joined_df.shape == (3,4)
    assert set(joined_df.columns) == set(['Name', 'Country', 'Medal', 'GDP'])
    assert joined_df.equals(correct_dataframe)

def test_join_aggregate_teams():
    """
    Test is sports were collected correctly (sports weren't doble counted)
    Test whetehr the dataframe merge was conducted correctly.
    """
    cleaner = Cleaner()
    sample_teams = pd.DataFrame([['United States', 'Some Sport1', 'United States of America', 'Men'], \
                                    ['United States', 'Some Sport2', 'United States of America', 'Women'], \
                                    ['Canada', 'Some Sport', 'Canada', 'Men'], \
                                    ['Puerto Rico', 'Some Sport', 'Puerto Rico', 'Women']], columns = ['Name','Discipline', 'NOC', 'Event'])

    sample_olympic = pd.DataFrame([['USA United States of America', 1], \
                                    ['CAN Canada', 2]], columns = ['Name', 'Medal'])

    joined_teams = cleaner.join_aggregate_teams(sample_teams, sample_olympic)

    correct_dataframe = pd.DataFrame([['USA United States of America', 1, 'United States of America', 2], \
                                    ['CAN Canada', 2, 'Canada', 1]], columns = ['Name', 'Medal', 'NOC', 'Discipline'])

    # dimension check
    assert joined_teams.shape == (2, 4)
    assert set(joined_teams.columns) == set(['Name', 'NOC', 'Discipline', 'Medal'])
    assert joined_teams.equals(correct_dataframe)


