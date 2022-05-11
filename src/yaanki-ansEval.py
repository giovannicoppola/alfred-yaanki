#!/usr/bin/env python3
### ALFRED-ANKILITE
#or yaanki
#### Monday, November 15, 2021, 11:41 AM

# script to show answer (back card) and handle evaluation

import time
import json
import os
from config import MYMODE
from yaankiFun import *

myAnswer=os.path.expanduser(os.getenv('myAnswer', ''))
myCardID=os.path.expanduser(os.getenv('myCardID', ''))
myNoteID=os.path.expanduser(os.getenv('myNoteID', ''))
dueIcon=os.path.expanduser(os.getenv('dueICON', ''))
col_creation=os.path.expanduser(os.getenv('col_creation', '')) # creation of the collection, timestamp

myTableValues = myScheduler() #fetching the 11 outcome-dependent table values for each possible answer (outcome)
if (myTableValues['again']['cards']['due'] != "not set yet"):
    DUE_AGAIN =  TS_CONV (myTableValues['again']['cards']['due'],'%H:%M')
else:
    DUE_AGAIN = "not set yet"

QUICK_LOOK = ""


if (myTableValues['easy']['cards']['due'] != "not set yet"):
    dueDaysE = int(col_creation) + (int(myTableValues['easy']['cards']['due'])*86400) #converting days in seconds
    DUE_EASY = time.strftime('%Y-%m-%d-%a', time.localtime(int(dueDaysE)))
else:
    DUE_EASY = "not set yet"


if ((myTableValues['good']['cards']['due'] != "not set yet") and (myTableValues['good']['cards']['due'] < 1000000000)):
    dueDays = int(col_creation) + (int(myTableValues['good']['cards']['due'])*86400) #converting days in seconds
    DUE_GOOD = time.strftime('%Y-%m-%d-%a', time.localtime(int(dueDays)))
elif ((myTableValues['good']['cards']['due'] != "not set yet") and (myTableValues['good']['cards']['due'] > 1000000000)):    
    DUE_GOOD =  TS_CONV (myTableValues['good']['cards']['due'],'%H:%M')
else:
    DUE_GOOD = "not set yet"

(myAnswer, QUICK_LOOK)=picHandler(myAnswer)
myAnswer = removeTags(myAnswer)

if MYMODE == "Standard":
    myAnswerBlockAgain = ""
    myAnswerBlockGood = ""
    myAnswerBlockEasy = ""
elif MYMODE == "Verbose":
    myAnswerBlockAgain = (
            "Factor: "
        + str(myTableValues['again']['revlog']['factor'])
        + " Type: "
        + str(myTableValues['again']['cards']['type'])
    )
    myAnswerBlockGood = (
            "Factor: "
            + str(myTableValues['good']['revlog']['factor'])
            +" Type: "
            + str(myTableValues['good']['cards']['type'])
    )
    myAnswerBlockEasy = (
            "Factor: "
            + str(myTableValues['easy']['revlog']['factor'])
            +" Type: "
            + str(myTableValues['easy']['cards']['type'])
    )


answer = {"items": [{"title": myAnswer,
    "subtitle": (
        "^🔴 (+"
        + str (abs(myTableValues['again']['revlog']['ivl']))
        + " " 
        + str(DUE_AGAIN) 
        + ") ⌥🟢 (+"
        + str(abs(myTableValues['good']['revlog']['ivl'])) 
        + ", "
        + str(DUE_GOOD)
        + ")  ⌘🍰 (+"
        + str(abs(myTableValues['easy']['cards']['ivl'])) 
        + ", "
        + str(DUE_EASY)
        + ")"
    ), 
    "quicklookurl": QUICK_LOOK,
    "arg": myAnswer,  #enter is the same as alt+enter
     "icon": {

            "path": "icons/"+dueIcon 
        },
    "variables": {
        "rev_ease": myTableValues['good']['revlog']['ease'],
            "rev_ivl": myTableValues['good']['revlog']['ivl'],
            "rev_type": myTableValues['good']['revlog']['type'],
            "rev_factor": myTableValues['good']['revlog']['factor'],
        
            "card_type": myTableValues['good']['cards']['type'],
            "card_queue": myTableValues['good']['cards']['queue'],
            "card_due": myTableValues['good']['cards']['due'],
            "card_ivl": myTableValues['good']['cards']['ivl'],
            "card_factor": myTableValues['good']['cards']['factor'],
            "card_laps": myTableValues['good']['cards']['laps'],
            "card_left": myTableValues['good']['cards']['left']
        },
    "mods": {
    "ctrl": {
        "valid": 'true',
        "arg": "1",
        "subtitle": (
            "🛑again, due: " 
            + str(DUE_AGAIN)
            + " (+"
            + str(abs(myTableValues['again']['revlog']['ivl']))
            + ") "
            + myAnswerBlockAgain
        ),
        "variables": {
        
            "rev_ease": myTableValues['again']['revlog']['ease'],
            "rev_ivl": myTableValues['again']['revlog']['ivl'],
            "rev_type": myTableValues['again']['revlog']['type'],
            "rev_factor": myTableValues['again']['revlog']['factor'],
        
            "card_type": myTableValues['again']['cards']['type'],
            "card_queue": myTableValues['again']['cards']['queue'],
            "card_due": myTableValues['again']['cards']['due'],
            "card_ivl": myTableValues['again']['cards']['ivl'],
            "card_factor": myTableValues['again']['cards']['factor'],
            "card_laps": myTableValues['again']['cards']['laps'],
            "card_left": myTableValues['again']['cards']['left']
        
        }
    
    },
    "alt": {
        "valid": 'true',
        "arg": "2",
        "subtitle": (
            "🟢good, due: " 
            + str(DUE_GOOD)
            +" (+"
            + str(abs(myTableValues['good']['revlog']['ivl'])) 
            + ") "
            + myAnswerBlockGood
        )
    },
    "cmd": {
        "valid": 'true',
        "subtitle": (
            "🍰piece of cake, due: " 
            + str(DUE_EASY) 
            +"(+"
            + str(abs(myTableValues['easy']['cards']['ivl'])) 
            + ") "
            + myAnswerBlockEasy
        ),
        "arg": "4", #used 1, 2, 4 for consistency with the rest of anki (skipped 2 Hard)
        "variables": {
        "rev_ease": myTableValues['easy']['revlog']['ease'],
            "rev_ivl": myTableValues['easy']['revlog']['ivl'],
            "rev_type": myTableValues['easy']['revlog']['type'],
            "rev_factor": myTableValues['easy']['revlog']['factor'],
        
            "card_type": myTableValues['easy']['cards']['type'],
            "card_queue": myTableValues['easy']['cards']['queue'],
            "card_due": myTableValues['easy']['cards']['due'],
            "card_ivl": myTableValues['easy']['cards']['ivl'],
            "card_factor": myTableValues['easy']['cards']['factor'],
            "card_laps": myTableValues['easy']['cards']['laps'],
            "card_left": myTableValues['easy']['cards']['left']
        }
    }
}

    }]}


print (json.dumps(answer))



