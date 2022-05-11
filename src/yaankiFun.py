#!/usr/bin/env python3
# encoding: utf-8
#
#
# Saturday, February 5, 2022, 11:51 AM
# Partly cloudy ⛅️  🌡️+23°F (feels +12°F, 63%) 🌬️↘16mph 🌒

"""YAANKI functions"""

import time
import sys
import re
import os
import sqlite3
import json
from config import AGAININTERVAL, GOODINTERVAL, EASYINTERVAL, GRAD_INTERVAL, INT_MODIFIER, \
ANKI_MEDIA_FOLDER, DEF_CARD_TYPE, ANKI_DATABASE, DEFAULT_DECK
myNow = int(time.time())

myType=int(os.path.expanduser(os.getenv('last_type', '0'))) #type of current card
myFactor=int(os.path.expanduser(os.getenv('last_factor', '0'))) #previous factor of current card
prevIvl=int(os.path.expanduser(os.getenv('last_ivl', '0'))) #previous interval of current card
myPrevEase=int(os.path.expanduser(os.getenv('last_ease', '0'))) #previous ease of current card
EASY_BONUS =float(os.path.expanduser(os.getenv('EASY_BONUS', '0'))) # default ease factor
myLapses=int(os.path.expanduser(os.getenv('last_lapses', '0'))) #current lapses
# for some reason thes variables are not passed as integers, even if defined as such


myQueue=os.path.expanduser(os.getenv('last_queue', '0')) # queue of current card
col_creation=os.path.expanduser(os.getenv('col_creation', '')) # creation of the collection, timestamp

DEFAULT_FACTOR=int(os.path.expanduser(os.getenv('EASE_FACTOR', ''))) # default ease factor (need for introduction in graduation cards)



def TS_CONV (ts,format_string):
    dueDate = time.strftime(format_string, time.localtime(int(ts)))
    return dueDate

def DAYSfromCRT ():
    myDays = int((myNow-int(col_creation))/86400)
    return myDays


def log(s, *args):
    if args:
        s = s % args
    print(s, file=sys.stderr)


def checkCardType(DEF_CARD_TYPE):
    db = sqlite3.connect(ANKI_DATABASE)
    
    ### Getting the list of card types from the database
    # trying to fetch a single item throws a 'no such collation sequence: unicase' error
    NOTETYPES = {}
    mysql_string = 'SELECT id,name FROM notetypes'
    db.row_factory = sqlite3.Row
    wwq = db.execute(mysql_string).fetchall()
    for wwqq in wwq:
        NOTETYPES.update ({wwqq['name']: wwqq['id']}) #converting a table to a dictionary    

    

    if DEF_CARD_TYPE not in NOTETYPES.keys():
        
    
        log ("ID does not exist")

        errorMess = {"items": [
            {"title": "this card type does not exist: "+DEF_CARD_TYPE,
                'subtitle': "please check the spelling in the workflow settings",
                'valid': True,
                
                "icon": {
                    "path": 'icons/Warning.png'
                }
                
        }]}

        print (json.dumps(errorMess))
        sys.exit()
    return NOTETYPES[DEF_CARD_TYPE]


def checkDefaultDeck(DefDeck):
    db = sqlite3.connect(ANKI_DATABASE)
    

    ### Getting the list of decks from the database
    MY_DECKS = {}
    mysql_string = 'SELECT id,name FROM decks'
    db.row_factory = sqlite3.Row
    wwq = db.execute(mysql_string).fetchall()
    for wwqq in wwq:
        MY_DECKS.update ({wwqq['name']: wwqq['id']}) #converting a table to a dictionary    

  

    if DefDeck not in MY_DECKS.keys():
        
    
        log ("ID does not exist")

        errorMess = {"items": [
            {"title": "this deck does not exist: "+DefDeck,
                'subtitle': "please check the spelling in the workflow settings",
                'valid': True,
                
                "icon": {
                    "path": 'icons/Warning.png'
                }
                
        }]}

        print (json.dumps(errorMess))
        sys.exit()
    return MY_DECKS[DefDeck]




    

"""
Order of 11 elements:
"revlog": # 4 revlog fields, upper row
            "ease"
            "ivl"
            "type" TYPE-REVLOG: 0=learn, 1=review, 2=relearn, 3=cram, (4=force due?)
            "factor"
"cards": # 7 card fields, bottom row
            "type" TYPE-CARDS: 0=new, 1=learning, 2=review, 3=relearning 
            "queue" 0=new, 1=learning, 2=review (as for type) 3=in learning, next rev in at least a day after the previous review, 4=preview
            "due"
            "ivl"
            "factor"
            "laps"
            "left"

LEFT is an integer of the form a*1000+b, with: 1)  b the number of reps left till graduation; 2) a the number of reps left today
Set to 0, not sure when it is needed (and not a priority)
"""

#SCHEDULEAGAIN, a function returning a list of 11 outcome-dependent values if the user selects AGAIN
def scheduleAgain ():
    
    if myType in [0,1]: #new or learning card
        DUE_AGAIN = (myNow + AGAININTERVAL)
        myArray = [1,-AGAININTERVAL,0,0,
        1,1,DUE_AGAIN,1,0,myLapses,0]
        
    elif (myType == 2):       ## if you fail a review card, go to relearning, with due at goodinterval, 
        DUE_AGAIN = myNow + GOODINTERVAL
        reduced_factor = myFactor -200 #not sure where this is from, according to this it is just removing 200 (20 percent points) (https://readbroca.com/anki/ease-hell/#:~:text=The%20Ease%20Factor%20is%20the,Anki%20thinks%20that%20card%20is.)
        myArray= [1,-GOODINTERVAL,1,reduced_factor,   # revlog-type 1, reviewing, and reduced factor
        3,1,DUE_AGAIN,1,reduced_factor,(myLapses+1),0] #card type goes to #3 (relearning)
    elif (myType == 3):       ## if you fail a relearning card, revlog type goes from 1 (review) to 2 (relearn), apparently ease factor and ease interval stay the same. 
        DUE_AGAIN = myNow + GOODINTERVAL
#        reduced_factor = int(myFactor) -200 #apparently this doesn't change, double check that
        myArray= [1,-GOODINTERVAL,2,myFactor,   # revlog-type 2, relearning, and factor *stays the same*
        1,1,DUE_AGAIN,1,myFactor,myLapses,0] #card-type: relearning (not additional lapses)
    else: # is there a type 4? Doesn't seem so, all scenarios should be covered 
        myArray = [999,999,0,9999,
        0,0,"not set yet",1,999,myLapses,"not set yet"]
    return myArray

#SCHEDULEGOOD, a function returning a list of 11 outcome-dependent values if the user selects GOOD
def scheduleGood ():
      
    if (myType == 0): #new card
        DUE_GOOD = (myNow + GOODINTERVAL)
        myArray= [3,-GOODINTERVAL,0,0,
        1,1,DUE_GOOD,1,0,myLapses,0]
    elif ((myType == 1) and (myPrevEase==1)): #learning card, previously 'again': step 1
        DUE_GOOD = (myNow + GOODINTERVAL)
        myArray= [3,-GOODINTERVAL,0,0,
        1,1,DUE_GOOD,1,0,myLapses,0]
    elif ((myType == 1) and (myPrevEase==3)): #previously good -> graduating (step 2), to be reviewed the next day
        DUE_GOOD = DAYSfromCRT()+ GRAD_INTERVAL #(default =1)
        myArray= [3,1,0,DEFAULT_FACTOR,
        2,2,DUE_GOOD,GRAD_INTERVAL,DEFAULT_FACTOR,myLapses,0]
    elif (myType == 2): #review card -> good
        #log (prevIvl)
        if prevIvl == 1:
            myRawIvl = EASYINTERVAL
            myRawFactor = 1000 #if just graduated, take the easy interval, without factor. not sure this is correct, double check
        else:
            myRawIvl = prevIvl
            myRawFactor = myFactor
        myIVL = round(myRawIvl*(myRawFactor/1000)*INT_MODIFIER) 
        DUE_GOOD = DAYSfromCRT() + myIVL
        myArray= [3,myIVL,1,myFactor,
        2,2,DUE_GOOD,myIVL,myFactor,myLapses,0]
    elif (myType == 3):  
        DUE_GOOD = (myNow + GOODINTERVAL)
        myArray= [3,-GOODINTERVAL,2,0,
        1,1,DUE_GOOD,1,0,myLapses,0]
    else:
        myArray= [999,999,999,999,
        0,0,"not set yet",1,999,myLapses,"not set yet"]
    return myArray

#SCHEDULEEASY, a function returning a list of 11 outcome-dependent values if the user selects EASY
def scheduleEasy ():

    if myType in [0,1]: #new or learning card
        myIVL = EASYINTERVAL # in Anki there is a fuzz element which changes this slightly
        if myFactor == 0: #if the cart is being learned and factor is not set, use the default
            newFactor = DEFAULT_FACTOR #otherwise use the last factor (I believe the anki algorithm changes that a little)
        else:
            newFactor = myFactor
        DUE_EASY = DAYSfromCRT()+ myIVL
        myArray = [4,myIVL,0,DEFAULT_FACTOR,
        2,2,DUE_EASY,myIVL,newFactor,myLapses,0]
    
    elif (myType == 2): #review card -> easy (too easy!): 1) adds bonus and 2) increases factor +15
        if prevIvl == 1:
            myRawIvl = EASYINTERVAL #if just graduated, take the easy interval. not sure this is correct, double check
            myRawBonus = 1
            
        else:
            myRawIvl = prevIvl
            myRawBonus = EASY_BONUS
        myIVL = round(myRawIvl*(myFactor/1000)*myRawBonus*INT_MODIFIER) # not sure it is 1 or GRAD interval, and when to add it
        increased_factor = myFactor +150 #currently it is just adding 150, will revisit later
        DUE_EASY = DAYSfromCRT()+ myIVL
        myArray= [4,myIVL,1,increased_factor,
        2,2,DUE_EASY,myIVL,increased_factor,myLapses,0]
    elif (myType == 3):
        myIVL = EASYINTERVAL # in Anki there is a fuzz element which changes this slightly
        if myFactor == 0: #if the cart is being learned and factor is not set, use the default
            newFactor = DEFAULT_FACTOR #otherwise use the last factor (I believe the anki algorithm changes that a little)
        else:
            newFactor = myFactor
        DUE_EASY = DAYSfromCRT()+ myIVL
        myArray = [4,myIVL,0,DEFAULT_FACTOR,
        1,2,DUE_EASY,myIVL,newFactor,myLapses,0]
    else:
         myArray = [999,999,0,9999,
        0,0,"not set yet",1,999,myLapses,"not set yet"]
    return myArray

##### MYSCHEDULER, a function to collect and combine table values to schedule card review
# this function will return for each of the oucomes the 11 outcome-dependent values:
# 4 for revlog
# 7 for cards
# Total: 33 variables

def myScheduler (): 
    againVals= scheduleAgain()
    goodVals= scheduleGood()
    easyVals= scheduleEasy()

    MY_OUTPUT = {
    "again": {
        "revlog": {  # 4 revlog fields
            "ease": againVals[0],
            "ivl": againVals[1],
            "type": againVals[2],
            "factor": againVals[3]},
        "cards": {  # 7 card fields
            "type": againVals[4],
            "queue": againVals[5],
            "due": againVals[6],
            "ivl": againVals[7],
            "factor": againVals[8],
            "laps": againVals[9],
            "left": againVals[10]}
    },
    "good": {
        "revlog": {  # 4 revlog fields
            "ease": goodVals[0],
            "ivl": goodVals[1],
            "type": goodVals[2],
            "factor": goodVals[3]},
        "cards": {  # 7 card fields
            "type": goodVals[4],
            "queue": goodVals[5],
            "due": goodVals[6],
            "ivl": goodVals[7],
            "factor": goodVals[8],
            "laps": goodVals[9],
            "left": goodVals[10]}

    },
    "easy": {
        "revlog": {  # 4 revlog fields
           "ease": easyVals[0],
            "ivl": easyVals[1],
            "type": easyVals[2],
            "factor": easyVals[3]},
        "cards": {  # 7 card fields
            "type": easyVals[4],
            "queue": easyVals[5],
            "due": easyVals[6],
            "ivl": easyVals[7],
            "factor": easyVals[8],
            "laps": easyVals[9],
            "left": easyVals[10]}
        }
    }


    return (MY_OUTPUT)
    


def removeTags(myText):
    TAG_RE = re.compile(r'<[^>]+?>').sub('',myText) #eliminating HTML tags
    return TAG_RE

def picHandler(myText):
    QUICK_LOOK_STRING = "" 
    
    if '<img' in myText:   
        try:
            pic_string = re.search(r'<img[^<>]+src=["\']([^"\'<>]+\.(?:gif|png|svg|jpe?g))["\']', myText).group(1)
            myText= re.sub (r"(<img.*?>)"," 🖼️ ",myText)
            QUICK_LOOK_STRING= ANKI_MEDIA_FOLDER+pic_string
            #log (pic_string)
        except AttributeError:
            found = '' # apply your error handling
    return (myText,QUICK_LOOK_STRING)


# https://stackoverflow.com/questions/62192316/python-regex-to-extract-content-of-src-of-an-html-tag
# To break this down a little:

# re.findall() return a list of strings
# <img we are looking to start in an image tag
# [^<>]+ 1 or more chars that don't open/close the html tag
# there might not be a src="" tag in the current <img>
# ["\'] the HTML could use either type of quote
# [^"\'<>]+ keep reading 1+ chars whilst the string and the tag are not closed
# \. literal dots need to be escaped, else they mean the "match anything" special char
# (?:gif|png|jpe?g) a range of possible file extensions, but don't create a capture bracket for them (which would return these in your array)
# ([^"\'<>]+\.(?:gif|png|jpe?g)) this is the capture bracket for what will actually get returned for each match
# ["\'] search for the closing quote to end the capture bracket
# re.I make the regex case insensitive
