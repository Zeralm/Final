# Final

This document describes all resources in the repository branch.  

## Sent_Vent-final  

The code in the Sent_Vent-final folder contains all self-authory code that is strictly necessary in order to reproduce the dataset used for this project.  

Here is a list of its contents:  

  seleCrawl.py - An ethical tool that accesses Twitter and analyzes user-generated content in situ as explicitly allowed in Twitter's Terms of Use under the denomination of crawling, complying with the necessary specifications.  
  
  storage.py - A module used for facilitating the access to the thematic database.  
  
  "Array creator.ipynb" - A jupyter notebook that processes 18.000 recent tweets extracted from the Twitter API to tokenize and lemmatize them and finally summarize an array of the most used words.  
  
  data/WordArray.csv - The array outputed by the afforementioned jupyter file.  
  
  fundownload.py - Script that downloads basic information, including legal names, from a database of Startups called Fundz, as recommended by the propietary website.  
  
  mergecsv.py - Script that merges all CSVs downloaded by fundownload.py  
  
  ThesisDatabase.db - Sqlite3 database that stores data at the company level and is ready for tweet data to be inserted in it, mainly through seleCrawl.py.  
  
  errorLog.txt - File that contains script outputs from seleCrawl.py. Updates can be disallowed by setting debug = False in seleCrawl.py
