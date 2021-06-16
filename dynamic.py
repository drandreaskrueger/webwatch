#!/usr/bin/env python3
'''
Created on 16 Jun 2021

@author: Andreas Krueger

@requires: dependencies venv, see README.md

@start longrunner:

    source env/bin/activate
    nohup ./dynamic.py >> nohup_dynamic.out 2>&1 &
    
    ps aux | grep "dynamic" | grep -v grep
    cat nohup_dynamic.out
    
Then you can logout, as it will run in the background.
'''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os, time, datetime, sys
# from pprint import pprint

from config_dynamic_personal import URL, SLEEPTIME, CLASS_SEARCH, ORDER, DATAFILE, REPEAT_AFTER

def chromedriver(URL, sleeptime=SLEEPTIME):
    print ("Selenium chromedriver ...", end=" ")
    # Instantiate options
    opts = Options()
    opts.binary_location = "/usr/bin/chromium" # which chromium # see README.md
    
    # unknown error: DevToolsActivePort file doesn't exist ... SOLVED:
    opts.add_argument("--disable-dev-shm-using") 
    opts.add_argument("--disable-extensions") 
    opts.add_argument("--disable-gpu") 
    opts.add_argument("--no-sandbox") #  Bypass OS security model
    
    # headless version needs no Xorg window manager
    opts.add_argument("--headless") 
    
    # Location of the webdriver - download from https://chromedriver.chromium.org/downloads
    chrome_driver = os.getcwd() + "/chromedriver" # see README.md
    
    # Instantiate a webdriver
    driver = webdriver.Chrome(options=opts, executable_path=chrome_driver)
    
    # Load the HTML page
    driver.get(URL)
    print("wait %d seconds until Javascript is actually finished ..." % sleeptime, end=" ")
    time.sleep(sleeptime)
    html_page=driver.page_source
    
    driver.quit()
    print ("killed browser. Analyzing webpage: ...")
    return html_page

def parse(html_page, find_classes):
    # Parse processed webpage with BeautifulSoup
    results={}
    soup = BeautifulSoup(html_page, features="html5lib")
    
    for observable, find_class in find_classes.items():
        hit = soup.find(class_=find_class) # finds the FIRST one only!
        # print (hit.text)
        results[observable] = hit.text.strip()
            
    return results
        
def store_csv_row(results, order, datafile):
    with open(datafile, "a") as f:
        f.write(("\t".join([results[name] for name in order])+"\n"))
        
        
def dynamic_page_scraper(url, find_classes, datafile, order):
    html_page=chromedriver(url)
    results = parse(html_page, find_classes)
    results["DateTime"] = ("%s" % datetime.datetime.now())[:19]
    print(results)
    store_csv_row(results, order=order, datafile=datafile)


if __name__ == '__main__': 
    while True:
        try:
            # raise Exception("Just testing")
            dynamic_page_scraper(URL, find_classes=CLASS_SEARCH, datafile=DATAFILE, order=ORDER)
        except Exception as e:
            print("ERROR: (%s) %s" % (type(e), e))
        print ("Now sleep %.0f minutes, then repeat ..." % (REPEAT_AFTER/60))
        sys.stdout.flush()
        time.sleep(REPEAT_AFTER)
        print ()
    
    
    