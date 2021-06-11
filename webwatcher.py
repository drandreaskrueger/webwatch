#!/usr/bin/env python3
'''
Created on 11 Jun 2021

@author: Andreas Krueger

@requires: dependencies venv, see README.md
@start longrunner:

    source env/bin/activate
    nohup ./webwatcher.py >> nohup.out 2>&1 &
    ps aux | grep "webwatcher" | grep -v grep
    cat nohup.out
    
Then you can logout, as it will run in the background.
'''

import requests, hashlib, smtplib, time, sys
from bs4 import BeautifulSoup 
from pprint import pprint

from config_personal import mail, www, mailtext

pageFingerprintFile="fingerprint.sha256"

def get_URL(pageToWatch, searchOnPage, searchString):
    if not pageToWatch:
        print ("Get the target page URL by selecting the first occurrence of the given link text:")
        
        html_page = requests.get(searchOnPage).text
        soup = BeautifulSoup(html_page, features="html5lib")
        for link in soup.findAll('a'):
            href, linktext = link.get('href'), link.text
            if linktext==searchString:
                print ("SUCCESS:", href,linktext)
                pageToWatch = href
                break
            
        print ()
        
    return pageToWatch

def compare_page(pageToWatch, pageFingerprintFile=pageFingerprintFile):
    # pageToWatch=""
    
    if not pageToWatch:
        print("ERROR: No 'pageToWatch' URL. Check the 'searchOnPage' link page manually, possibly updating the searchString")
        # hmmm ... this is a serious error that could also begin to happen during runtime. Perhaps send this error as email too? Yes:
        return "ERROR: no 'pageToWatch' URL", "ERROR: check the script again"
    
    else:
        print ("Now this page will be studied for any changes:", pageToWatch)
        html_page = requests.get(pageToWatch).text
        length=len(html_page)
        newsha=hashlib.sha256(bytes(html_page, encoding='utf8')).hexdigest()
        print ("Loading page ... done.\nNew sha256sum=%s, Length=%d" % (newsha, length))
        
        try:
            with open(pageFingerprintFile, "r") as f:
                oldsha=f.read().strip()
                print ("Old sha256sum=%s" % oldsha)
        except FileNotFoundError:
            oldsha=""
            
        if newsha==oldsha:
            print ("Nothing changed.")
        else:
            print ("Page has changed somehow, updating fingerprint file...")
            with open(pageFingerprintFile, "w") as f:
                f.write(newsha)
        
        return newsha, oldsha
        
def send_alert_email(newsha, oldsha, pageToWatch, mail, www):

    params = {**www, **mail, "oldsha": oldsha, "newsha": newsha, "pageToWatch": pageToWatch}
    pprint(params)
    msg = mailtext.format(**params)
    print(msg)
    
    print ("Connecting to SMTP server")
    server = smtplib.SMTP_SSL(mail["server"], mail["port"], timeout=15)
    server.login(mail["login"], mail["password"])
    
    server.sendmail(mail["sender"], mail["recipient"], msg)
    print ('Done sending email.')
    server.quit()


def check_compare_emailPerhaps(pageToWatch, searchOnPage, searchString, pageFingerprintFile, mail):
    pageToWatch = get_URL(pageToWatch, searchOnPage, searchString)
    newsha, oldsha = compare_page(pageToWatch, pageFingerprintFile=pageFingerprintFile)
    print()
    if newsha==oldsha:
        print ("No change. Done. Exit.")
    else:
        print ("Sha256 changed, sending email:")
        send_alert_email(newsha, oldsha, pageToWatch, mail=mail, www=www)
    
        
if __name__ == '__main__':
    # send_alert_email("aaaa", "bbbb", pageToWatch="http://...", mail=mail, www=www); exit()
    
    while True:
        check_compare_emailPerhaps(www['pageToWatch'], www['searchOnPage'], www['searchForLinkText'], pageFingerprintFile, mail)
        print ("\nSleeping %.0f minutes now, then trying again." % (www['sleepSeconds']/60))
        sys.stdout.flush()
        time.sleep(www['sleepSeconds'])
        