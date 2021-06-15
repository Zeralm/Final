__version__ = "3.6.10"

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException
import time
import pandas as pd
import statistics
import numpy as np
import storage
import math
import datetime
StartDate = datetime.date(2016,1,3)
print(str(StartDate))
EndDate = datetime.date(2021,4,6)
driver = webdriver.Chrome("C:/Windows/chromedriver.exe")
driver.get("https://app.fundz.net/users/sign_in")
user = driver.find_element_by_xpath("/html/body/div/div/div/div/div/form/input[1]")
passw = driver.find_element_by_xpath("/html/body/div/div/div/div/div/form/input[2]")
user.send_keys("mtourkadze@gmail.com")
passw.send_keys("Simono123")
user.send_keys(Keys.ENTER)


def mainlooop(StartDate,EndDate):
    while StartDate < EndDate - datetime.timedelta(days = 2):
        driver.get("https://app.fundz.net/download_filings")
        loc = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div[2]/form/div[2]/div[2]/div[2]/div/div/div/button")
        loc.click()
        sel = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div[2]/form/div[2]/div[2]/div[2]/div/div/div/div/div/div[1]/span")
        sel.click()
        loc.click()
        NextDate = StartDate + datetime.timedelta(days = 2)
        former_field = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div[2]/form/div[2]/div[3]/input[1]")
        latter_field = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div[2]/form/div[2]/div[3]/input[2]")
    
        u1, u2 = StartDate.__format__("%d/%m/%Y"), NextDate.__format__("%d/%m/%Y")
        u1, u2 = u1.replace("-","/"), u2.replace("-","/")
    

        former_field.clear()
        former_field.send_keys(u1)
        latter_field.click()
        latter_field.clear()
        latter_field.send_keys(u2)
    
        loc.click()
        loc.click()
        search = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div[2]/form/div[2]/div[4]/input")
        try:
            search.click()
        except ElementClickInterceptedException:
            loc.click()
        try:
            WebDriverWait(driver,5).until(
                EC.presence_of_element_located((By.XPATH,"//h5[@class='fillings']/a"))
            )
        except TimeoutException:
            try:
                WebDriverWait(driver,5).until(
                    EC.presence_of_element_located((By.XPATH,"//*[@id='feed_entries_csv']/div[2]"))
                )
            except TimeoutException:
                return StartDate
        

        export = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div[2]/form/div[2]/div[4]/button")
        export.click()

        WebDriverWait(driver,5).until(
            EC.presence_of_element_located((By.XPATH,"//*[@id='modalFilingsSent']/div[1]"))
        )


    

        StartDate = NextDate
    return False

u = mainlooop(StartDate,EndDate)
while True:
    
    if u == False:
        break
    else:
        u = mainlooop(u,EndDate)