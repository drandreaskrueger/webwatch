'''
Created on 11 Jun 2021

@author: andreas
'''

mail={
    "server" :    "<your SMTP server>",
    "port":       465,
    "password" :  "<your password>",
    "login" :     "<your login name to your SMTP server>",
    "sender":     "<email address, might be the same as the 'login'>",
    "recipient":  "<email address that gets alerted>",
}

www={
    "searchOnPage": "http://parse-all-the-href-links-on-this-page/",
    "searchForLinkText" : "First link with this text gets selected",
    "pageToWatch" : "", # "http://alternatively-give-the-URL-to-watch-directly/or-leave-this-empty"
    "sleepSeconds" : 60*60*2 # until the page is checked again
}

mailtext="""To:{recipient}
From:{sender}
Subject: THE WEBPAGE HAS CHANGED !

ALERT: The page '{pageToWatch}' has changed!

old sha256: {oldsha}
new sha256: {newsha}

Perhaps you can book an appointment now?
"""
