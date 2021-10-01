# Final

Ethical tools for crawling through Twitter's user-generated content mentioning financial information on Startups, classifying it and analyzing it. Designed for asyncronous use through several GNU/Linux servers. It can process millions of Tweets in a few days.


This document describes all resources in the repository branch.  

## Sent_Vent-final  

The code in the Sent_Vent-final folder contains all self-authory code that is strictly necessary in order to reproduce the dataset used for this project and needs to be collected using a script.  

Here is a list of its contents:  

  seleCrawl.py - An ethical tool that accesses Twitter and analyzes user-generated content in situ as explicitly allowed in Twitter's Terms of Use under the denomination of crawling, complying with the necessary specifications. [More details here][1].
  
  storage.py - A module used for facilitating the access to the local thematic database ThesisDatabase.db.  
  
  "Array creator.ipynb" - A jupyter notebook that processes 18.000 recent tweets extracted from the Twitter API to tokenize and lemmatize them and finally summarize them in an array of the most used words.  
 
  ### Tools for obtaining Company Data 
 
  fundownload.py - Script that downloads basic information, including legal names, from a database of Startups called Fundz, as recommended by the propietary website.  
  
  mergecsv.py - Script that merges all CSVs downloaded by fundownload.py , and outputs them into either a csv or the local database
  
  ### Data folder (src)
   
  data/WordArray.csv - The array outputed by the afforementioned jupyter file.  
  
  data/ThesisDatabase.db - Sqlite database that stores data at the company level. It has been set up for storing tweet data, mainly coming from seleCrawl.py.  
  
  data/errorLog.txt - File that contains script outputs from seleCrawl.py. Updates can be disallowed by setting debug = False in seleCrawl.py


[1]: https://github.com/Zeralm/Final/blob/main/Sent_Vent-final/Guide%20to%20seleCrawl.py%20.md
