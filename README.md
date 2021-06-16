# webwatch
Sends an email if WWW page content has changed. Quickstart:

    source env/bin/activate
    nohup ./webwatcher.py >> nohup.out 2>&1 &

Steps:

1. preparations (see below)
2. it visits a page "searchOnPage" with many links, selecting the first link with a specific link text "searchForLinkText"
3. then it downloads that "pageToWatch" HTML body, hashes it with sha256sum, compares the hash to last time
4. if the hash has changed, it sends an email
5. goto 2.


## preparations
### dependencies
```
python3 -m venv env
source env/bin/activate
pip install --upgrade pip
pip install requests BeautifulSoup4 html5lib
```

### SMTP server
fill in webpage search and SMTP parameters in the `config_personal.py` that you copy from the `config.py` template.

### testing 
For a clean situation, just remove the `fingerprint.sha256` file. Try this until you get it working:

    source env/bin/activate
    ./webwatcher.py
    
at "sleeping ..." press CTRL-C to exit. Now you are good to go for the nohup longrunner above.

## known problems
### SMTP
If the smtpserver connection times out, your machine might be firewalled, try this manually

    telnet smtpserver 465

until you get a connection like this

    Trying  smtpserver ...
    Connected to smtpserver.
    Escape character is ...
    
Some cloudproviders also have such a policy: "SMTP ports blocked for security reasons. To enable them ... click ... enable SMTP ports."

Once that telnet command works, you'll manage. Typos in login name, or password, ... the usual.


# webwatch_dynamic
If parts of the webpage are generated, or dynamically loaded (JavaScript), then we must use a browser; the module `selenium` provides for that. Here used with `chromium` (*).

## quickstart

    source env/bin/activate
    nohup ./dynamic.py >> nohup_dynamic.out 2>&1 &
    
### watch status

    ps aux | grep "dynamic" | grep -v grep
    cat nohup_dynamic.out output.csv
    
the first also shows you the PID for `kill PID`.

## preparations
Even if it is a headless console only machine, (e.g.) chromium must be installed:

    sudo apt install chromium unzip wget
    /usr/bin/chromium --version
    
    # get chromedriver = see https://chromedriver.chromium.org/downloads for perfect version
    wget https://chromedriver.storage.googleapis.com/90.0.4430.24/chromedriver_linux64.zip
    unzip chromedriver_linux64.zip 

    source env/bin/activate
    pip install selenium
    
    ./dynamic.py
    
Then google the error messages, until you get it working (i.e. you see "Now sleep __ minutes, then repeat ...").

## You
For debugging a remote situation, perhaps it helps to switch OFF the `opts.add_argument("--headless")` option, and instead connect via `ssh -Y yourmachine` to your VPS, so that the X window (of the remote controlled chromium) shows up locally. 

### (*) good first issue
Selenium would probably also work with Firefox, after minor tweaks? Feel free to post a pull request if you succeed; perhaps extend the `config_dynamic_personal.py` imports for that variation. Thanks.
