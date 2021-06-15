# Guide to seleCrawl.py

### What this script does:  

  -Make queries to Twitter, conduct sentiment analysis, cross check lemma coincidence with WordArray.csv on a tweet per tweet basis, export data indexed by company ID.  
  
  -Ensure that every single tweet in scope is taken into account, in detriment of speed and memory.  
  
  -Ensure that no error returned by the intepreter interfieres with a correct functioning (avoid data leaks and corruption).  
  
  -Notify of errors using a Telegram bot and record them into errorLog.txt.  
  
  -Group its querying sessions in time brackets of one month, starting at one month before a funding.  
  
  -Store data generated on top of Twitter in data/ThesisDatabase.db  
  
  -Mark all obsevations susceptible of being dubious, for further inspection.
  
  
 ### What it does not do:  

  -Be informative about its inner workings.  
  
  -Run smoothlessly without errors.  
  
  -Guarantee its autonomy in front of persistent errors.  
  
  -Support remote troubleshooting through Telegram.  
  
  
  ### How it works:  
  
  
  -Once the setup is provided as Setup Commands for seleCrawl suggest, the script call takes this form:  
  
  
  python3 seleCrawl.py [number of months before a funding] [Telegram chat ID (optional)]  
  
  
  
  Also, recording the errors locally can be explicitly disallowed by setting the parameter debug = False.  
  
