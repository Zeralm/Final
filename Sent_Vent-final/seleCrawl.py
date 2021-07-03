__version__ = "3.6.10" #Works in higher versions as tested. Theoretically in older versions too
"""
Be sure to download nltk necessary packages. Nltk errors will show you the way
"""

import chromedriver_binary
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')
nltk.download("averaged_perceptron_tagger")
nltk.download("wordnet")
nltk.download('punkt',download_dir='/home/mtourkadze/nltk_data')
nltk.download('stopwords')
import nltk.data
import nltk.tokenize
import nltk.corpus
import nltk.stem.wordnet
import itertools
import time
import pandas as pd
import numpy as np
import storage
import math
import datetime
import os
import requests
import sys
#Need to press automatically the button sth went wrong. Also, how to notify if internet gone?
#pd.set_option('display.max_rows', None)
Gathered = pd.Series()


staleMarker = 0


class trinity_condition(object):
    """
    Defines a waiting condition returnin True when either one of two elements is found: All tweets or a no results page
    """

    def __init__(self):
            pass
    def __call__(self,driver):
        if not EC.presence_of_element_located((By.XPATH, "//article//div[@lang]//*")) or not EC.presence_of_element_located((By.XPATH, "//article//a[@dir='auto']")):
            return False
        elif not EC.presence_of_element_located((By.XPATH, "//div[@data-testid='emptyState']")):
            return False
        else:
            return True

def aggregate_str_content(array_of_elements):
    """
    Takes an array of DOM elements with text and merges their text content
    """

    u = ""
    for h in array_of_elements:
        u+=h.text
    return u

def extract(driver, iteration = 0):
    """
    Collects all tweets visibile by the driver, one by one. Innefficient and ineffective, needs some tweaking
    """
    #Add wait condition based on presence of all tweets
    linkos = set()
    if iteration % 4 == 0 and iteration != 0: print("Interruption in the collecting process. The browser window must remain still!")
    
    try:
        divs = driver.find_elements_by_xpath("/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div")
    
        [linkos.add((aggregate_str_content(div.find_elements_by_xpath("./div/div/article/div/div/div/div[2]/div[2]/div[2]/div[1]/div/*")),div.find_element_by_xpath("./div/div/article/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/a").get_attribute("href"), div.find_element_by_xpath("./div/div/article/div/div/div/div[2]/div[2]/div[2]/div[3]/div[2]/div/div/div[2]/span/span").text, div.find_element_by_xpath("./div/div/article/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/a/time").get_attribute("datetime"))) if len(div.find_elements_by_xpath("./div/div/article/div/div/div/div[2]/div[2]/div[2]/div[3]/div[2]/div/div/div[2]/span/span")) != 0 else linkos.add((aggregate_str_content(div.find_elements_by_xpath("./div/div/article/div/div/div/div[2]/div[2]/div[2]/div[1]/div/*")),div.find_element_by_xpath("./div/div/article/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/a").get_attribute("href"), 0, div.find_element_by_xpath("./div/div/article/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/a/time").get_attribute("datetime"))) if len(div.find_elements_by_xpath("./div/div/article/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/a")) != 0 else linkos.add(("Tweets not found",None,None,None)) for div in divs]
        
        
        if iteration >= 4: print("Collecting process resumed.")
        
    except StaleElementReferenceException:
        print('window moved')
        global staleMarker
        staleMarker+=1
        if iteration <= 20:
                linkos = linkos.union(extract(driver, iteration + 1))
        else:
                print("The collecting process accumulated too many interruptions. The DOM cannot be read. Exiting program")
                driver.quit()
                #Save progress and notify of stop
    return linkos

"""

Main

"""

def search_fromCSV(Data,holy_array, bookmark = 0):
    

    print("Initializing crawler")
    WINDOW_SIZE = "1920,1080"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument('--no-sandbox')
    
    driver = webdriver.Chrome(chrome_options=chrome_options)
    #driver.get("http://www.twitter.com/login")
    #print(driver.title)
    
    try:
        for l in range(bookmark,len(Data)):
            #Here we loop the automated query cycle
            term = Data["Company"].iloc[l]
            foundation = datetime.datetime.strptime(Data["FundDate"].iloc[l],"%Y-%m-%d").date() - datetime.timedelta(17+30*(month_before_funding-1))
            bracket = foundation - datetime.timedelta(30)

            bracko  =   bracket.strftime("%Y-%m-%d")


            #Replacing special characters that will be in query
            if "&" in term:
                term = term.replace("&","%26")
            if "#" in term:
                term = term.replace("#","%23")
            if "\\" in term:
                term = term.replace("\\","/")
            driver.get( 
                'https://twitter.com/search?q=\"' + 
                term+'\"' + '%20until%3A{}%20since%3A{}'.format(foundation,bracko) +'&src=typed_query&f=live'
                )

            #There must be a second between queries, at least.
        
            try:
                WebDriverWait(driver, 2.5).until(
                    trinity_condition()
                )
            #What's this, makes no sense, it just continues??
            except TimeoutException:
                #Add case when no internet
                driver.quit()
                return False
                #Tie to database to mark a problem

            try:
                ak = time.perf_counter()
                print("dumbo")
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH,"//div[@data-testid='emptyState']"))
                )
                u = driver.find_element_by_xpath("//div[@data-testid='emptyState']")
                print("dumbini")
                um = pd.Series(Data["tweets"])
                um[l] = 0
                Data["tweets"] = um
                links = {("EMPTY_RESULT",Data["Company"].iloc[l],None,None,None,bracket)}
                print("imperator")
                print("ID: {}".format(Data["ID"].iloc[l]))
                print(links)
                
            except TimeoutException:
                #Put except
                                   
                links=set()
                u = True
                
                #This will need tweaking too
                count_scrap = time.perf_counter()
                while u == True:           
                    #Reference /html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[x]/div/div/article
                    time.sleep(0.2)
                    if math.trunc(driver.execute_script("return document.body.scrollHeight;") - driver.execute_script("return document.documentElement.scrollTop;") - driver.execute_script("return window.innerHeight;")) == 0:
                        try:
                            WebDriverWait(driver, 1.5).until(
                                EC.presence_of_element_located((By.XPATH,"//div[@role='progressbar']"))
                                )
                            #Add here what happens when it loads eternally
                        except TimeoutException:
                            u = False
                        try:
                            WebDriverWait(driver, 5).until_not(
                                EC.presence_of_element_located((By.XPATH,"//div[@role='progressbar']"))
                                )
                        except TimeoutException:
                            um = pd.Series(Data["tweets"])
                            um[l] = 0
                            Data["tweets"] = um
                            u = False
                    links = links.union(extract(driver))
                    #u=False or break??
                    # Why is this even here? Relocate to extract 
                    if 1756 + driver.execute_script("return document.documentElement.scrollTop;") >= driver.execute_script("return document.body.scrollHeight;"):
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    else:
                        driver.execute_script("window.scrollTo(0, document.documentElement.scrollTop + 1756*2);")
                    
                    try: 
                        
                        u = driver.find_element_by_xpath("/html/body/div/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div/div[2]/div/span/span")
                        driver.quit()
                        return False
                    except:
                        print("{} links found, word: {} (ID: {}) in {} seconds".format(len(links),term,Data["ID"].iloc[l],time.perf_counter()-count_scrap))
                    
                    
                   

            print(links)
            uk = time.perf_counter()
            print("Search of {} items takes {} seconds".format(len(links),uk-ak))


            lengths = pd.Series(Data["tweets"])
            lengths[l] = len(links)
            Data["tweets"] = lengths
            print(Data[["Company","tweets"]])

            acceptable = [t>14 for t in Data["tweets"]]
            ouaga = acceptable.count(True)
            if l +1 - bookmark== 0: perc = 0
            else: perc = ouaga*100/(l+1- bookmark)
            print("Valid companies: {} out of {}. ({}%), with an average amount of Tweets of {}".format(ouaga, l+1-bookmark, perc, np.mean(Data["tweets"].iloc[acceptable])))
            #[Gathered.add((z[0], Data["Company"].iloc[l], z[3], z[2], z[1])) for z in links]
            #print((z[0], Data["Company"].iloc[l], z[3], z[2], z[1]) for z in links)
                
            #Don't connect to database if no tweets gathered

            
            stops = nltk.corpus.stopwords.words("english")
            def clean(tokens,stops):
                tokens = pd.Series(x for x in tokens if not x in stops)

                l = nltk.wordnet.WordNetLemmatizer()
                lemmatized = []

                for word, tag in nltk.pos_tag(tokens):
                    if tag.startswith('NN'):
                        pos = 'n'
                    elif tag.startswith('VB'):
                        pos = 'v'
                    else:
                        pos = 'a'
                    lemmatized.append(l.lemmatize(word, pos))
                return pd.Series(lemmatized)
            
            def select(lista, holy_array):
                if (list(lista.values) == list(clean(nltk.tokenize.word_tokenize("TweetsNotFound", "english"),stops).values) or list(lista.values) == list(clean(nltk.tokenize.word_tokenize("EMPTY_RESULT", "english"),stops).values)):
                    return [j for j in lista]
                else:
                    return [j for j in lista if j in holy_array.values]
                    
            
            storage.add_tweets([(str(" ".join(select(clean(nltk.tokenize.word_tokenize(z[0]),stops),holy_array))),fiki.polarity_scores(z[0])["compound"],fiki.polarity_scores(z[0])["pos"],fiki.polarity_scores(z[0])["neg"],fiki.polarity_scores(z[0])["neu"], Data["Company"].iloc[l], z[3], z[2], z[1],bracket) for z in links])
            reportime = (datetime.timedelta(hours=2) + datetime.datetime.now()).strftime("%H:%M:%S-%Y/%m/%d")
            k = open("data/errorLog.txt", "a")
            k.write("Checkpoint saved {} at time {} at company {} and company ID {} with {} tweets".format(bracko, reportime, Data["Company"].iloc[l], Data["ID"].iloc[l], len(links) ) + os.linesep)
            k.close()
        return True

    finally:
        pass
        print("Final Dataset")
        print(Data[["Company","tweets"]])
        driver.quit()

def apply_CSV():
        
        result = False
        try:
            Data = pd.DataFrame(storage.extract_fundings())
            Data.columns = ["ID","Company","Sector","Filing","State","Location","Raised","Offered","FundDate"]
            Data["tweets"] = 0
            holy_array = pd.read_csv("data/WordArray.csv")["Words"]
            
            #Additional instructions on what to fetch
        finally:
            print("Instructions uploaded")
            pointer = storage.extract_last_company()
        
            if pointer == None:
                u = 0
                
            elif Data["Company"].str.contains(pointer[0],regex = False).any():
                
                foundo = datetime.datetime.strptime(pointer[2],"%Y-%m-%d").date()
                bracketo = foundo + datetime.timedelta(17+30*month_before_funding)
                brackoto  =   bracketo.strftime("%Y-%m-%d")
                
                #print(brackoto,Data["FundDate"].iloc[0])
                kala = Data["Company"] == pointer[0]
                #print(Data.loc[kala,"ID"].loc[brackoto == Data["FundDate"]])
                try:
                    u = int(Data.loc[kala,"ID"].loc[brackoto == Data["FundDate"]])
                    print(u)
                except TypeError:
                    u = int(Data.loc[kala,"ID"].loc[brackoto == Data["FundDate"]].iloc[0])

                reportime = (datetime.timedelta(hours=2) + datetime.datetime.now()).strftime("%H:%M:%S-%Y/%m/%d")
                k = open("data/errorLog.txt", "a")
                k.write("Checkpoint RECOVERED {} at time {} at company {} and company ID {}".format(brackoto, reportime, pointer[0], u) + os.linesep)
                k.close()

                print("Checkpoint {} {}".format(pointer,u))
            else: 
                u = 0
                
            
            if u != 0:
                u = Data.index[Data.loc[:,"ID"] == u].to_list()[0]
            
            if len(Data["Company"]) != u:
                result = search_fromCSV(Data,holy_array,u+1)
                    #None: inconclusive, interrupted #True: Completed
        
                print("Extraction completed")
                
            #Instruction for next csv
            else:
                print("You are opening a finished dataset")
                
                
            #Instruction for next csv



if __name__ == "__main__":
    """
    Script parameters: 
        month_before_funding: time on which the crawling is focussed. Expressed on number of months before the funding. 
            Should be greater than 0
        chat_id: The id of your chat with the Telegram bot @seleCrawl_bot
    """
    
    debug = True 
    while True:
        try:
            fiki = SentimentIntensityAnalyzer()
            global month_before_funding
            month_before_funding = int(sys.argv[1])
            apply_CSV()
            
        except Exception as exc:
            if debug == True:
                reportime = (datetime.timedelta(hours=2) + datetime.datetime.now()).strftime("%H:%M:%S-%Y/%m/%d")
                k = open("data/errorLog.txt", "a")
                message = "Error {} at time {} at company and tweet nummber {}".format(exc, reportime, storage.extract_last_company())+ os.linesep
                k.write(message)
                k.close()
                if sys.argv[2] != "": 
                    requests.post('https://api.telegram.org/bot{}/sendMessage'.format(sys.argv[2]),data={'chat_id': sys.argv[3], 'text': "t = -{}: ".format(month_before_funding) + message})
            else:
                pass
        
