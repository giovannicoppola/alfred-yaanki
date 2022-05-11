#!/usr/bin/env python3
# -*- coding: utf-8 -*-
### Getting the list of decks from the database to choose the predefined decks for search and study
## Saturday, April 30, 2022, 9:24 PM

import sqlite3
import sys
import json
from config import ANKI_DATABASE, DEFAULT_DECK
from yaankiFun import log

### INITIALIZING
MYINPUT= sys.argv[1]
MYQUERY= "%" + MYINPUT + "%"
result = {"items": []}

db = sqlite3.connect(ANKI_DATABASE)
cursor = db.cursor()

DECK_LIST = [x.strip() for x in DEFAULT_DECK.split(',') if x]


try:
    cursor.execute("""SELECT name, id, mtime_secs
    FROM decks
    WHERE name LIKE ? ORDER BY mtime_secs DESC;
    """,(MYQUERY,))
    
    rs = cursor.fetchall()

except sqlite3.OperationalError as err:
    result= {"items": [{
    "title": "Error: " + str(err),
    "subtitle": "Some error",
    "arg": "",
    "icon": {

            "path": "icons/Warning.png"
        }
    }]}
    print (json.dumps(result))
    raise err


if (rs):
    myResLen = str(len (rs))
    countR=1
    
    for r in rs:
        myIcon = ''
        title = r[0]  
        
        subtitle = DEFAULT_DECK
        
        if not DECK_LIST:
            myIcon = 'icons/check-mark.png'
            actionString = "No preferred decks, Shift-Enter to add this only to the list"
            DEFAULT_DECK_new = title
        else:
            if title in DECK_LIST:
                myIcon = 'icons/check-mark.png'
                actionString = "Shift-Enter to remove this deck from the default list"
                DEFAULT_DECK_new = DEFAULT_DECK.replace(title,'')
                DEFAULT_DECK_new = DEFAULT_DECK_new.rstrip(", ")
                DEFAULT_DECK_new = DEFAULT_DECK_new.lstrip(", ")
            else:
                myIcon = ''
                actionString = "Shift-Enter to add this deck to the default list"
                DEFAULT_DECK_new = DEFAULT_DECK + "," + title

    #### COMPILING OUTPUT    
        result["items"].append({
        "title": title,
        "subtitle": str(countR)+"/"+myResLen + "–" +actionString + " " + subtitle,
        "arg": DEFAULT_DECK,
        "mods": {
            "shift": {
                "subtitle": "new DEFAULT_DECK if ↩️: " + DEFAULT_DECK_new,
                "arg": DEFAULT_DECK_new
            }
        },
        "icon": {
            "path": myIcon
            }
        
        
               

        })
        countR += 1  

    print (json.dumps(result))


if MYINPUT and not rs:
    resultErr= {"items": [{
        "title": "No matches",
        "subtitle": "Try a different query",
        "arg": "",
        "icon": {
            "path": "icons/Warning.png"
            }
        
            }]}
    print (json.dumps(resultErr))
    
