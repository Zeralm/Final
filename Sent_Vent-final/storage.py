import sqlite3
from sqlite3 import Error
import datetime
import pandas as pd

"""

cursorObj.execute("INSERT INTO Tweets VALUES(1, 'generic tweet', 'Tesla', '29-3-2009', 'twitter.com', 23, 52)")
    con.commit()

cursorObj.execute("SELECT id, content, link FROM Tweets")
info = cursorObj.fetchall()
"""

        
def standard_connect():
    
    con = sqlite3.connect('data/ThesisDatabase.db')
    #print("Connection is established with data/ThesisDatabase.db")
    
    cursorObj = con.cursor()    
    return con, cursorObj
    
def abort(con):
    #Ahemm you should be able to do this with decorators u dumb
    con.close()
    #print("Connection terminated with data/ThesisDatabase.db")

def create_table_tweets():
    con, cursorObj = standard_connect()
    #You can change date type object to Datetime
    cursorObj.execute("CREATE TABLE tweets(id integer PRIMARY KEY AUTOINCREMENT, words TEXT, sentiment FLOAT,positive FLOAT,negative FLOAT,neutral FLOAT,company TEXT, date TEXT, link TEXT, retweets TEXT, foundation DATE, UNIQUE(words, sentiment,company,date,link,retweets,foundation) );") #Only unique tweets allowed
    con.commit()
    abort(con)

def create_table_companies():
    con, cursorObj = standard_connect()
    #You can change date type object to Datetime
    cursorObj.execute("CREATE TABLE companies(id integer PRIMARY KEY AUTOINCREMENT, company TEXT, industry TEXT, filing TEXT, state TEXT, city TEXT, money TEXT, offered TEXT, published DATE, UNIQUE(company,filing,state,city,money,offered,published));") #Only unique tweets allowed
    con.commit()
    abort(con)

def add_tweets(info): #[content, company, date, link, retweets]
    con, cursorObj = standard_connect()
    cursorObj.executemany("INSERT OR IGNORE INTO tweets(words, sentiment, positive, negative, neutral, company, date, link, retweets, foundation) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", info)
    con.commit()
    abort(con)

def add_fundings(info):
    con, cursorObj = standard_connect()
    try:
        cursorObj.executemany("INSERT OR IGNORE INTO companies(company, filing, industry, state, city, money, offered, published) VALUES(?, ?, ?, ?, ?, ?, ?, ?) ", info)
    except sqlite3.IntegrityError:
        print("Repeated funding")
    con.commit()
    abort(con)


def extract_last_company(): #[content, company, date, link, retweets]
    con, cursorObj = standard_connect()
    cursorObj.execute("SELECT company, id, foundation FROM tweets WHERE id = (SELECT MAX(id) FROM tweets)")
    data = cursorObj.fetchall()
    print(data)
    abort(con)
    if len(data) != 0:
        print("Checkpoint recovered: {}".format(data[0][0]))
        return data[0]
    else:
        print("No checkpoint returned because there's no checkpoint")
        return None
    
def extract_tweets(company = None,down = None, up = None):
    if company == None and down == None and up == None: raise TypeError('Expected arguments')
    
    con, cursorObj = standard_connect()
    
    if company == None and down != None and up != None:

        cursorObj.execute("SELECT * FROM tweets WHERE id > ? AND id < ?", [down,up])
        data = cursorObj.fetchall()
        abort(con)
        print("Tweets in range [{} < id < {}] recovered".format(down,up))

    elif company != None and down == None and up == None:

        cursorObj.execute("SELECT * FROM tweets WHERE company = ?", [company])
        data = cursorObj.fetchall()
        abort(con)
        print("Tweets mentioning {} recovered".format(company))
    
    else:
        return None
    return data

def extract_fundings():
    con, cursObj = standard_connect()

    cursObj.execute("SELECT * FROM companies")
    data = cursObj.fetchall()
    abort(con)
    print("{} fundings recovered".format(len(data)))
    return data


"""

add_tweet(["Generic tweet!","Enormocorp","29-3-2006","twitter.com",2])
print(extract_last_company())
"""
#print(len(extract_tweets("HYGIEIA INC")))
#add_tweets([["Generic tweet!","Grivy","29-3-2006","twitter.com",2,"sc"]])
 
#create_table_tweets()

#add_fundings([["e","t","e","k","e","e","e",datetime.date(2010,1,1)]])
"""
con, cursObject = standard_connect()
cursObject.execute("DROP TABLE companies")
abort(con)
create_table_companies()
"""
"""
con, cursObject = standard_connect()
cursObject.execute("DROP TABLE tweets")
abort(con)
create_table_tweets()
"""

#print(extract_last_company())
#print(len(extract_tweets(company = "KaloBios Pharmaceuticals Inc")))

#u = pd.DataFrame(extract_fundings())

#pd.set_option("display.max_rows", None, "display.max_columns", None)
#print(u)
#print(ua.iloc[29130:29142])

#k = pd.DataFrame(extract_fundings())

#print(len(set(k[1])))
