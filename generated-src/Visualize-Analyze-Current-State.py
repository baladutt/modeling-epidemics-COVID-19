#!/usr/bin/env python
# coding: utf-8

# # Visualize current state - plot COVID data

# In[1]:


countryToAnalyze = "India"
stateToAnalyze ="Karnataka"


# In[2]:


get_ipython().run_line_magic('run', './Load-Data.ipynb')


# In[3]:


#from pandas_profiling import ProfileReport

##profile = ProfileReport(confirmedDf, title='Confirmed - Pandas Profiling Report', html={'style':{'full_width':True}})
#profile = ProfileReport(confirmedDf)

#profile
##profile.to_widgets()
##profile.to_notebook_iframe()


# In[4]:


from matplotlib import pyplot
get_ipython().run_line_magic('matplotlib', 'inline')

pyplot.style.use("fivethirtyeight")# for pretty graphs

# Increase the default plot size and set the color scheme
pyplot.rcParams['figure.figsize'] = 8, 15

confirmedTSDf = confirmedDf.loc[confirmedDf["Country/Region"] == countryToAnalyze].T[4:]
pyplot.figure(1)
pyplot.plot(confirmedTSDf)
pyplot.xticks(rotation=90)


# In[5]:


get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
print(confirmedTSDf.values.flatten())
dy_dt= np.diff(confirmedTSDf.values.flatten())
print(dy_dt)
f, ax = pyplot.subplots(figsize=(12, 8))
pyplot.plot(dy_dt, label="dy/dt")
pyplot.legend()


# In[6]:


d2y_dt2= np.diff(dy_dt)
f, ax = pyplot.subplots(figsize=(12, 8))
pyplot.plot(d2y_dt2, label="d2y/dt2")
pyplot.legend()


# ## Compute SEIR parametes - alpha, beta, gamma

# In[7]:


countries = list([countryToAnalyze, "Pakistan"])
pyplot.figure(1)

#This is incomplete - WIP
for country in countries:
    print(country)
    confirmedTSDf = confirmedDf.loc[confirmedDf["Country/Region"] == country].T[4:]
    recoveredTSDf = recoveredDf.loc[recoveredDf["Country/Region"] == country].T[4:]
    deathsTSDf = deathsDf.loc[deathsDf["Country/Region"] == country].T[4:]
    removedArr = recoveredTSDf.values + deathsTSDf.values
    dR_dt= np.diff(removedArr.flatten())
    confirmedArr = confirmedTSDf[1:].values.flatten()
    confirmedArr[confirmedArr == 0] = 0.0001 # to prevent divide by zero
    gamma = dR_dt / confirmedArr
    #print(confirmedTSDf)
    #print(recoveredTSDf)
    #print(removedArr)
    #print("dr_dt",dR_dt)
    #print(gamma)
    pyplot.plot(gamma, label="gamma for "+country)
    
pyplot.legend()


# # Analyze statewise for India 

# ## Capacity for maximum

# In[8]:


get_ipython().run_line_magic('matplotlib', 'inline')


hospitalBedsDf.dropna(axis=0, how='all', inplace=True)
hospitalBedsDf = hospitalBedsDf.fillna(-1)
hospitalBedsDf = hospitalBedsDf.loc[hospitalBedsDf["State/UT"] != "All India"]
hospitalBedsDf["State / Union Territory"] = hospitalBedsDf["State/UT"]

populationHospitalBedsdf = pd.merge(indiaPopulationDf, hospitalBedsDf, on=['State / Union Territory'])
states = populationHospitalBedsdf["State / Union Territory"]

fig, ax1 = pyplot.subplots(figsize=(20,10))

color = 'tab:red'
ax1.set_ylabel('population', color=color)
pyplot.xticks(rotation=90)
ax1.plot(states, populationHospitalBedsdf["Population"], label ="population", color=color)
ax1.tick_params(axis='y', labelcolor=color)

color = 'tab:blue'
ax2 = ax1.twinx()
ax2.set_ylabel('NumPublicBeds_HMIS', color=color)

ax2.plot(states, populationHospitalBedsdf["NumPublicBeds_HMIS"].astype(int), label="NumPublicBeds_HMIS", color=color)
ax2.tick_params(axis='y', labelcolor=color)
pyplot.legend()


# ## State-wise numbers

# In[9]:


covidIndiaLastDayDataDf = pd.DataFrame(columns=covidIndiaDataDf.columns.values)

covidIndiaLastDayDataDf.insert(len(covidIndiaDataDf.columns), "dy_dt", [], True)
covidIndiaLastDayDataDf.insert(len(covidIndiaDataDf.columns), "d2y_dt2", [], True)
covidIndiaLastDayDataDf.insert(len(covidIndiaDataDf.columns), "days", [], True)


for state in states:
    stateDataDf = covidIndiaDataDf.loc[covidIndiaDataDf["State/UnionTerritory"] ==state]
    stateDataDf.sort_values('Date',ascending=False,inplace=True)
    if stateDataDf.shape[0] != 0:
        covidIndiaLastDayDataDf = covidIndiaLastDayDataDf.append(stateDataDf.iloc[0])
        dy_dt= np.diff(stateDataDf["Confirmed"].values.astype(int))
        d2y_dt2= np.diff(dy_dt)
        days = 0
        if len(stateDataDf.index) > 0:
            date = stateDataDf.index[-1]
            days = (stateDataDf.index[0] - stateDataDf.index[-1]).days
            #print(days)
        else:
            date=datetime.strptime("1/1/1970", '%d/%m/%y')
        if date == 0:
            date=datetime.strptime("1/1/1970", '%d/%m/%y')
        last_dy_dt = 0
        if dy_dt.shape[0] != 0:
            last_dy_dt = dy_dt[0]
        last_d2y_dt2 = 0
        if d2y_dt2.shape[0] != 0:
            last_d2y_dt2 = d2y_dt2[0]
        covidIndiaLastDayDataDf.iloc[-1,-1] = -1*last_dy_dt
        covidIndiaLastDayDataDf.iloc[-1, -2] = -1*last_d2y_dt2
        covidIndiaLastDayDataDf.iloc[-1, -3] = days
    else:
        covidIndiaLastDayDataDf = covidIndiaLastDayDataDf.append(pd.Series(), ignore_index=True)
        covidIndiaLastDayDataDf.iloc[-1, 1] = state
    

covidIndiaLastDayDataDf.fillna(0, inplace=True)


# In[18]:


import seaborn as sns

# Disable warnings 
import warnings
warnings.filterwarnings('ignore')

get_ipython().run_line_magic('matplotlib', 'inline')
sns.set()

f, ax = pyplot.subplots(figsize=(18, 20))
covidIndiaLastDayDataDf['Name of State / UT']=covidIndiaLastDayDataDf['State/UnionTerritory']
covidIndiaLastDayDataDf['Total cases']=covidIndiaLastDayDataDf['Confirmed']
covidIndiaLastDayDataDf['Cured/Discharged/Migrated']=covidIndiaLastDayDataDf['Cured']
data = covidIndiaLastDayDataDf[['Name of State / UT','Total cases','Cured/Discharged/Migrated','Deaths', 'dy_dt', 'd2y_dt2', 'days']]

data.sort_values('Total cases',ascending=False,inplace=True)
sns.set_color_codes("pastel")
sns.barplot(x="Total cases", y="Name of State / UT", data=data,
            label="Total", color="r", ci=None)

sns.set_color_codes("muted")
g =sns.barplot(x="Cured/Discharged/Migrated", y="Name of State / UT", data=data,
            label="Recovered", color="g", ci=None)


# Add a legend and informative axis label
ax.legend(ncol=2, loc="lower right", frameon=True)
ax.set(xlim=(0, 200), ylabel="",
       xlabel="Cases, (dy/dt,d2y/dt2,Days since first case, Total cases)")
sns.despine(left=True, bottom=True)


order = 0
for index, row in data.iterrows():
    val = str(int(row['dy_dt'])) + "," + str(int(row['d2y_dt2'])) + "," + str(int(row['days'])) + ","+str(row["Total cases"])
    if val != "0,0,0,0":
        g.text(row["Total cases"], order, val, color='black', ha="center", fontsize=9, horizontalalignment='left',  verticalalignment='center')
    order += 1
    


# ## Testing to positive - trend and ratio

# In[11]:


fig, ax1 = pyplot.subplots(figsize=(20,10))

color = 'tab:red'
ax1.set_ylabel('tested', color=color)
pyplot.xticks(rotation=90)
ax1.plot(icmrTestingDf["DateTime"], icmrTestingDf["TotalSamplesTested"], label ="TotalSamplesTested", color=color)
ax1.tick_params(axis='y', labelcolor=color)

color = 'tab:blue'
ax2 = ax1.twinx()
ax2.set_ylabel('TotalPositiveCases', color=color)

ax2.plot(icmrTestingDf["DateTime"], icmrTestingDf["TotalPositiveCases"], label="TotalPositiveCases", color=color)
ax2.tick_params(axis='y', labelcolor=color)
pyplot.legend()


# # Giving an Index to states based on their handling - where to focus?
# 
# Lower the better

# In[12]:


#Penalty for delay since first case
data["responseIndex"] = (0.001+data["days"])
#Penalty for rate of growth of cases
data["responseIndex"] = data["responseIndex"] + data["responseIndex"] * 1000*(0.001+data["dy_dt"])
#Penalty if the rate of rate itself is up
data["responseIndex"] = data["responseIndex"] + data["responseIndex"] * 1000*(0.001+data["d2y_dt2"])

data["responseIndex"] = data["responseIndex"] + data["responseIndex"] *100*(0.001+data["Total cases"])/(data["Total cases"].sum())

data.sort_values('responseIndex',ascending=False,inplace=True)
data.reset_index()
indexData = data[['Name of State / UT', 'responseIndex']]
indexData.drop(index=0, inplace=True)
display(indexData)


# # Analyze a particular State

# In[13]:


covidStateDataDf = covidIndiaDataDf.loc[covidIndiaDataDf["State/UnionTerritory"]==stateToAnalyze]


# In[14]:


get_ipython().run_line_magic('matplotlib', 'inline')
pyplot.figure(1)
pyplot.plot(covidStateDataDf["ConfirmedIndianNational"].values, label="ConfirmedIndianNational")
pyplot.legend()


# In[15]:


dy_dt= np.diff(covidStateDataDf["Confirmed"].values)
pyplot.figure(1)
pyplot.plot(dy_dt, label="dy/dt")
pyplot.legend()


# In[16]:


d2y_dt2= np.diff(dy_dt)
pyplot.figure(1)
pyplot.plot(d2y_dt2, label="d2y/dt2")
pyplot.legend()


# In[17]:




from matplotlib import pyplot
import numpy as np
#from mlxtend.plotting import ecdf
from scipy import stats
get_ipython().run_line_magic('matplotlib', 'inline')

provinceDf_group_by_date = provinceDf.groupby('Date').sum()
regionDf_group_by_date = regionDf.groupby('Date').sum()

total_positive_cases_timeseries = provinceDf_group_by_date['TotalPositiveCases']
total_removed_cases_timeseries = regionDf_group_by_date['Recovered']+regionDf_group_by_date['Deaths']

print(total_positive_cases_timeseries.values.flatten())
incremental_positive_cases_timeseries = np.diff(total_positive_cases_timeseries.values.flatten())
pyplot.figure(figsize=(15, 8))
pyplot.xticks(rotation=90)
ax = pyplot.axes()
ax_bis = ax.twinx()
ax.plot(total_positive_cases_timeseries, label='Total positive cases', color='blue')
ax_bis.plot(incremental_positive_cases_timeseries, label='Incremental positive cases', color= 'red')
ax.legend(loc=2)
ax_bis.legend(loc=1)   
pyplot.show()


date_ = '2020-03-28T17:00:00'
df_last_date = provinceDf[provinceDf['Date']==date_]
df_last_date = df_last_date.groupby('RegionName').sum()

# df_last_date = df_last_date.sortby('TotalPositiveCases')
df_timeseries = df_last_date['TotalPositiveCases']
df_timeseries = df_timeseries.sort_values(ascending=False)
pyplot.figure(figsize=(15, 8))
pyplot.xticks(rotation=90)
pyplot.plot(df_timeseries)
pyplot.show()


df_timeseries = df_timeseries/df_timeseries.sum()
print('Percentage of time series')
pyplot.show()

out_sum = np.cumsum(df_timeseries)
pyplot.figure(figsize=(15, 8))
pyplot.xticks(rotation=90)
pyplot.plot(out_sum)
pyplot.show()


len_reg=len(df_last_date)
x= np.arange(len_reg)
x=x+1
x = x/x.max()
# pyplot.scatter(0.2, 0.8, s=100, color='red')
pyplot.figure(figsize=(15, 8))
pyplot.axhline(y=0.8,  color='red')
# TODO : compute value of x for which y=0.8 and show
pyplot.plot(x, out_sum)
pyplot.show()

