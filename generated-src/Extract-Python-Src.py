#!/usr/bin/env python
# coding: utf-8

# In[1]:


import nbformat
from nbconvert import PythonExporter

from os import listdir
from os.path import isfile, join, splitext

def convertNotebook(notebookPath, modulePath):

  with open(notebookPath) as fh:
    nb = nbformat.reads(fh.read(), nbformat.NO_CONVERT)

  exporter = PythonExporter()
  source, meta = exporter.from_notebook_node(nb)

  with open(modulePath, 'w+') as fh:
    fh.writelines(source)


# In[2]:


baseDir = "."
generatedSrcDir = join(baseDir, "generated-src")
for f in listdir(baseDir):
        if isfile(join(baseDir, f)):
            splitFileName = splitext(f)
            print(splitFileName)
            if len(splitFileName) == 2 and splitFileName[1] == ".ipynb":
                convertNotebook(join(baseDir, f),join(generatedSrcDir, splitFileName[0]+".py"))


# In[ ]:




