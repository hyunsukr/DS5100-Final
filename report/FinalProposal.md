# Project Report

## INTRODUCTION
With the 2021 Tokyo Olympics there is data available on the official website for the olympics. We hope that we can accomplish data mining, processing of data, and turn data into information then knowledge. 

## THE DATA
For this project, we pulled data from a variety of sources. Originally, we were planning on scraping the medal count for each country, as well as which events the medals were won in from the official Tokyo Olympics website (https://olympics.com/en/olympic-games/tokyo-2020/medals). However, the website has changed since we first started our project, so we can no longer scrape the data related to which sports the medals were won in. We decided to adjust our plan slightly, and now we are going to supplement our data with Kaggle’s dataset on the Tokyo Olympics (https://www.kaggle.com/arjunprasadsarkhel/2021-olympics-in-tokyo). We are going to pull the Athletes and Teams datasets down, aggregate them by country, and add the number of teams and individual athletes each country has to our dataset. Finally, we scraped data for the GDP of each country (https://www.worldometers.info/gdp/gdp-by-country/ ) and added this to our dataset. We are very interested in how each of these factors affect the medal count for each country. 
Because we are pulling from three different data sources, we have had to do some pre-processing of the data. The original dataset and the Kaggle datasets do come from the same original source, so it is easy to match up the country names. However, the country names from the Olympics datasets and the GDP data do not match up one-to-one, so there is some additional processing that will have to be done there to ensure that we have properly joined our datasets without losing any valuable data. 

## EXPERIMENTAL DESIGN
The Olympic data pulled will have medal count by country, categories, and athletes. Along with the Olympics data the GDP dataset will contain the national GDP for each country. And lastly, using a groupby function on the information of the athletes and their country we will be able to get a count of athletes per country. We will then combine these three datasets using an inner join. We will then start analysing the data trying to establish a correlation between the medal count and both of the new features. We plan on doing visualizations of a color coded world map and scatterplots to reinforce our statements

##PROJECT MANAGEMENT
We will collaborate through the entire project. We will have weekly cadence zoom meetings to check and verify our work progress so that we can deliver on time. The main milestones will be data mining, data processing, feature engineering, analysis of data, presentation preparation. All communication will be either through slack or messages. 

Data Mining: Max, Said
Data Processing/Feature Engineering: Max, Said
Data Analysis & Presentation: Reilly and Sydney
Testing, Documentation, Presentation: All
Github Branch (PR) Manager: Max

## RESULTS
The results will be displayed through a video that encompasses our findings. In our findings, we will display portions of the cleaned data as well visuals to accompany our analysis of the data. To visualize the data, we hope to utilize various plots and visualizations. We plan on using a map plot to color in the countries represented in the Olympics and then color by density. We plan on using a stacked line plot to view the total medal counts by metal type. We plan on looking into visualizations for GDP such as scatter plots, density plots, and sizing scatter plots by variables such as medal count and GDP. 

## TESTING
There will be many steps of data transformation / engineering, which will be done through python functions and operations. With the operations done we will need to do unit testing to check whether the functions operate correctly.

Along with python unit testing, we will also conduct sanity checks about the data itself so see if the data pulled seems to be correct. 

During the stage of data transformation / engineering, many pandas and numpy operations were used to transform the data. For all the transformations of the code, our team wrote simple unit tests to check each logical operation being done on the dataset. This ensured us that all the steps were being done correctly and we could be ready for any changes to the data. 

Along with the python unit testing, we also conducted sanity checks with the data itself and processed data to see if the data pulled was correctly pulled.

## OUTCOME
Our goal for this project is to find the relationship between different variables and countries on how they related to medals earned as well as providing a visual representation of the data from the Tokyo Olympics. It’s not common to see summary statistics of the olympic data provided online, which we plan to create visualizations as well as summary statistics of the data pulled. 

## PROBLEMS AND PROGRESS
We have made significant progress on our project so far. We have successfully scraped two different data sources and downloaded an additional two sets from Kaggle. That data has all been cleaned, processed, and joined into a single dataset. We are continuing to meet weekly to make sure we are communicating and making progress on our project. 
We have run into a few problems up to this point. Our biggest issue was that the Tokyo Olympics website has been redesigned since we first started our project, so we lost the ability to scrape data that we were originally planning on using in our analysis. Additionally, because we are using data from different sources, we have had to do some manual work in order to make sure all of our data is being joined properly into a single dataset. 

