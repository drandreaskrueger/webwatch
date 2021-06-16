'''
Created on 16 Jun 2021

@author: andreas
'''

URL="https://..." # page with Javascript
SLEEPTIME=7       # how long does the Javascript need to finish, plus some extra time, just to be sure

# have a look at how the code uses this in the super simple dynamic.parse() = it can easily be extended, 
#   or modified to find e.g. EVERY occurence not only the first: soup.find_all() instead of soup.find() 
CLASS_SEARCH={"Number"      : "<unique class of this 'number' element, will find first occurrence>",
              "Weather"     : "<unique class of this 'weather' element, will find first occurrence>",
              }

ORDER=["DateTime", "Number", "Weather"] # order for the columns in the (tab-separated) CSV
DATAFILE="output.csv"

REPEAT_AFTER=60*60 # seconds until next readout