#!/usr/bin/env python
# coding: utf-8

# # Load Data

# ## For countries

# In[1]:


#Download data from "https://github.com/CSSEGISandData/COVID-19.git"

confirmedCsv = "COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
recoveredCsv = "COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
deathsCsv = "COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"

try:
    f = open(confirmedCsv)
except IOError:
    print('Download data from "https://github.com/CSSEGISandData/COVID-19.git"')
    assert False
finally:
    f.close()


# In[2]:


import pandas as pd

confirmedDf = pd.read_csv(confirmedCsv)
recoveredDf = pd.read_csv(recoveredCsv)
deathsDf = pd.read_csv(deathsCsv)


# In[3]:


populationOfCountries = "population_by_country_2020.csv"

populationDf = pd.read_csv(populationOfCountries)


# ## Load for Italy

# In[4]:


provinceCsv = "covid19-in-italy/covid19_italy_province.csv"
regionCsv = "covid19-in-italy/covid19_italy_region.csv"

try:
    f = open(confirmedCsv)
except IOError:
    print('Download data from "https://www.kaggle.com/sudalairajkumar/covid19-in-italy"')
    assert False
finally:
    f.close()

provinceDf = pd.read_csv(provinceCsv)
regionDf = pd.read_csv(regionCsv)   


# ## Load for USA

# In[5]:


usDataCsv = "us-counties.csv"
# Data can be downloaded from : https://www.kaggle.com/fireballbyedimyrnmom/us-counties-covid-19-dataset
usDf = pd.read_csv(usDataCsv) 
usDf_group_by_date = usDf.groupby('date').sum()
#print(usDf_group_by_date)
total_infected_us_timeseries = usDf_group_by_date['cases']
total_removed_us_timeseries = usDf_group_by_date['deaths']


# ## Analyze statewise for India 
# 
# Download data from - https://www.kaggle.com/sudalairajkumar/covid19-in-india

# In[6]:


from datetime import datetime

covidDataFile = "covid19-in-india/covid_19_india.csv"
populationFile = "covid19-in-india/population_india_census2011.csv"
hospitalBedsFile = "covid19-in-india/HospitalBedsIndia.csv"
icmrTestingFile = "covid19-in-india/ICMRTestingDetails.csv"

try:
    f = open(covidDataFile)
except IOError:
    print('Download data from "https://www.kaggle.com/sudalairajkumar/covid19-in-india"')
    assert False
finally:
    f.close()
    
    
def parser(x):
    return datetime.strptime(x, '%d/%m/%y')

def icmrDateParser(x):
    return datetime.strptime(x, '%d/%m/%y %H:%M')

covidIndiaDataDf = pd.read_csv(covidDataFile, parse_dates=[1], index_col=1, squeeze=True, date_parser=parser)
indiaPopulationDf = pd.read_csv(populationFile)
hospitalBedsDf = pd.read_csv(hospitalBedsFile)
icmrTestingDf = pd.read_csv(icmrTestingFile, parse_dates=[1], date_parser=icmrDateParser)

