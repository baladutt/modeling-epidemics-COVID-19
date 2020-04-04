#!/usr/bin/env python
# coding: utf-8

# In[1]:


#https://www.kaggle.com/sudalairajkumar/covid19-in-india/download


# In[2]:


get_ipython().system(' cd COVID-19')
get_ipython().system('git pull')
get_ipython().system('cd ..')


# In[3]:


import sys
get_ipython().system('{sys.executable} -m pip install kaggle')


# In[ ]:


from kaggle.api.kaggle_api_extended import KaggleApi

#Download kaggle API token
# homepage www.kaggle.com -> Your Account -> Create New API token
# move it to ~/.kaggle/kaggle.json

#kaggle datasets download -d sudalairajkumar/covid19-in-india

api = KaggleApi()
#print("before", api.competitions_list())
api.authenticate()
print("after", api.competitions_list())
print("datasets", api.dataset_list())


import os

print(os.listdir('./')) # This will print the content of current directory
os.remove('covid19-in-india.zip') # This will remove file 

files = api.dataset_download_files("sudalairajkumar/covid19-in-india/data")
#files = api.competition_download_files("sudalairajkumar/covid19-in-india/data")

get_ipython().system('cd covid19-in-india && unzip -oqu ../covid19-in-india.zip && cd ..')

import os

print(os.listdir('./')) # This will print the content of current directory
#os.remove('covid19-in-india.zip') # This will remove file 


# In[ ]:


get_ipython().run_line_magic('run', './Load-Data.ipynb')


# In[ ]:


get_ipython().run_line_magic('run', './Basic-Reproduction-Number.ipynb')


# In[ ]:


get_ipython().run_line_magic('run', './SEIR-with-Social-Distancing.ipynb')
get_ipython().run_line_magic('run', './Visualize-Analyze-Current-State.ipynb')
get_ipython().run_line_magic('run', './Extract-Python-Src.ipynb')


# In[ ]:




