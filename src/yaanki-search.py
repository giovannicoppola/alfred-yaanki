#!/usr/bin/env python3

### ALFRED-ANKILITE
#or yaanki
#### Sunday, October 31, 2021 🎃
### the nth attempt at getting anki to work with alfred. 
## initial version of this script (with the sqlite search code) from Benjamin Gray, 2013
## merged with the card info script, created on Tuesday, November 16, 2021, 8:44 AM
## merged with 
### YAANKI-STUDY
#### Wednesday, January 19, 2022, 6:25 AM
### returning cards to study



# refer to the roam page for table annotation and database structure


import sqlite3
import string
import time
import json
import sys
from datetime import datetime
import re
import os

from config import ANKI_DATABASE, AGAININTERVAL, DECK_LIST, MYMODE
from yaankiFun import *

### INITIALIZING
MYINPUT = sys.argv[1]
MYQUERY = "%" + MYINPUT + "%"
result  = {"items": []}
QUICK_LOOK = ""

db = sqlite3.connect(ANKI_DATABASE)
cursor = db.cursor()




### Getting the list of decks from the database
MY_DECKS = {}
mysql_string = 'SELECT id,name FROM decks'
db.row_factory = sqlite3.Row
wwq = db.execute(mysql_string).fetchall()
for wwqq in wwq:
    MY_DECKS.update ({wwqq['name']: wwqq['id']}) #converting a table to a dictionary    
    

if len(DECK_LIST): #if there is at least one entry in the DEFAULT_DECKS variable
    MY_DECKS={k: MY_DECKS.get(k, None) for k in DECK_LIST} #subset of decks set by the user
    MY_DECKS = list(MY_DECKS.values()) #fetching deck IDs
    
else:
    MY_DECKS = list(MY_DECKS.values()) #no deck list set -> all



sqlite_string = f"""SELECT notes.flds, notes.id, decks.name,cards.id,cards.type,cards.due,cards.lapses, cards.reps, col.crt, cards.mod,cards.ivl,cards.queue,decks.id, cards.ord
    FROM notes,col 
    INNER JOIN (select DISTINCT nid,did,id,due,lapses,reps,type,mod,ivl,queue,ord from cards) cards ON cards.nid = notes.id 
    INNER JOIN decks ON decks.id = cards.did 
    WHERE cards.queue IN (0,1,2,3) AND notes.flds LIKE ? AND decks.id in  ({','.join(['?']*len(MY_DECKS))})
    ORDER BY cards.queue, cards.due"""

try:
    cursor.execute(sqlite_string,[MYQUERY]+MY_DECKS)
    rs = cursor.fetchall()

except sqlite3.OperationalError as err:
    result= {"items": [{
    "title": "Error: " + str(err),
    "subtitle": "Database error! Perhaps the Anki app is open?" + " – Close Anki and retry",
    "arg": ";;",
    "icon": {

            "path": "icons/Warning.png"
        }
    }]}
    print (json.dumps(result))
    raise err


myTimeStamp = round(time.time() * 1000)
myResLen = str(len (rs))
countR=1
    
for r in rs:
    string = r[0]  #string including front and back separated by \x1f
    noteID = r[1]   # note ID
    deckName = r[2] #deck name
    cardID = r[3] #cardID
    lapses = r[6] # number of lapses
    reps = r[7] #number of reps
    col_creation = r[8] #collection creation date
    ivl = r[10] #last interval from cards
    queue = r[11] #last queue from cards 
    deck_id = r[12] #Deck ID 
    c_order = r[13] #Deck ID 
    type = r[4] #last type from cards 
    myLastRev = time.strftime('%Y-%m-%d, %H:%M', time.localtime(int(r[9]))) #last review

    if r[4] in (1,3): # is the card being learned? # REPLACE this with formatting based on number type
        dueDate = time.strftime('%Y-%m-%d-%a, %H:%M', time.localtime(int(r[5]))) # if yes, uses the card due (integer sec timestamp)
        dueTS = int(r[5])
    else:
        dueTS = int(r[8]) + (int(r[5])*86400) #if not, converting days in seconds and adding to the deck creation date
        dueDate = time.strftime('%Y-%m-%d-%a', time.localtime(int(dueTS)))
    
    if reps == 0: #if there is no reps it is new
        dueDate = "New"
        myLastRev = "-"
        last_ease = 0
        last_ivl = 0
        last_lastIvl = -AGAININTERVAL
        last_rev_factor = 0
        lastDueBlock = "New Card"
    else: #fetching the most recent revlog value if there are reps
        revl = cursor.execute("""SELECT ease, ivl,lastivl, factor
        FROM revlog
        WHERE cid = ?
        ORDER BY id DESC""",(cardID,))
        revl = cursor.fetchone()
        last_ease = revl[0]
        last_ivl = revl[1]
        last_lastIvl = revl[2]
        last_rev_factor = revl[3]
        lastDueBlock = (" last: " 
            + myLastRev 
            + " due: " 
            + dueDate 
            + " – reps:" 
            + str(reps) 
            + " laps:" 
            + str(lapses)
            )
    
    string = string.replace("&nbsp;", "") # cleaning up HTML, might need to add more 
    fields = string.split("\x1f")
    
    if c_order == 0:    
        question = fields[0]
        answer = "-".join(fields[1:])
    else:
        answer = fields[0]
        question = "-".join(fields[1:])
    
    # setting the star/due icon
    if (dueTS < (myTimeStamp/1000)) or dueDate == "New" : #if due time is before now, or it is a new card
        dueIcon = 'star_red.png' # 🔴
    elif dueTS - (myTimeStamp/1000) < 86400: #due within 1 day
        dueIcon = 'star_yellow.png' #🟡
    else: #due in > 1d
        dueIcon = 'star_green.png' # 🟢

    # compiling the subtitle 
    if MYMODE == "Verbose":
        mySubtitle = (deckName 
            + " type:" 
            + str(type) 
            + " last: " 
            + myLastRev 
            + " ("
            + str(last_ease) 
            + ") factor: " 
            + str(last_rev_factor) 
            + " due: " 
            + dueDate 
            + " – reps:" 
            + str(reps) 
            + " laps:" 
            + str(lapses)
        )
    elif MYMODE == "Standard": 
        mySubtitle = (deckName 
            + " –"
            + lastDueBlock
        )
    (question,QUICK_LOOK) = picHandler(question)
    question = removeTags(question)
    

### COMPILING CARD INFO STRING
    NoteCreation = time.strftime('%Y-%m-%d, %H:%M', time.localtime(int(noteID)/1000))

    CardInfoString = (
        "Created on: "
        + NoteCreation 
        + "\nReviews: "
        + str(reps) 
        + "\nLast Reviewed: "
        + str(myLastRev) 
        + " (" 
        + str(myPrevEase) 
        + ")" 
        + "\nDue: "
        + str(dueDate) 
        + "\nLapses: "
        + str(lapses) 
        + "\nNote ID: "
        + str(noteID) 
        + "\nCard ID: "+ str(cardID)
    )


#### COMPILING OUTPUT    
    result["items"].append({
    "title": question,
    "subtitle": str(countR) + "/" + myResLen + "–" + mySubtitle, 
    "quicklookurl": QUICK_LOOK,
    "arg": question,
    "icon": {

            "path": "icons/" + dueIcon 
        },
    "variables": {
        "dueTS": dueTS,
        "dueDATE": dueDate,
        "myCardID": cardID,
        "myNoteID": noteID,
        "myStartTS": myTimeStamp,
        "myAnswer": answer,
        "last_reps": int(reps),
        "col_creation": col_creation,
        "last_ease": last_ease,
        "last_ivl": last_ivl,
        "last_lastIvl": last_lastIvl,
        "last_queue":   queue,
        "last_type":   type,
        "last_lapses":  lapses,
        "last_factor":   last_rev_factor,
        "deck_id":   deck_id,
        "dueICON":   dueIcon,

    },
    "mods": {
    "control": {
        "valid": 'true',
        "arg": CardInfoString,
        "subtitle": "Show card info"
    }
    
    
  
}

    })
    countR += 1

if rs:
    print (json.dumps(result))
      



if MYQUERY and not rs:
    resultErr= {"items": [{
        "title": "No matches",
        "subtitle": "Try a different query",
        "arg": "",
        "icon": {
            "path": "icons/Warning.png"
            }
        
            }]}
    print (json.dumps(resultErr))
