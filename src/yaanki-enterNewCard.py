#!/usr/bin/env python3
### ALFRED-ANKILITE
#or yaanki
#### Thursday, November 11, 2021, 8:05 PM
### a script to accept and parse a new card



import json
import sys
import re
from yaankiFun import * 



from config import DEF_CARD_TYPE, DEFAULT_DECK_NEW

myModID = checkCardType(DEF_CARD_TYPE)
myDeckID = checkDefaultDeck(DEFAULT_DECK_NEW)


MYTEXT= sys.argv[1]
MYFRONT=MYTEXT
MYBACK=""
result = {"items": []}

if MYTEXT == '':
    result['items'].append({
        "title": "Enter a new card",
            'subtitle': "enter front and back separated by //, --b to invert",
            'valid': True,
            
            "icon": {
                "path": 'icons/Warning.png'
            }
            
    })

    
    

else:

    if len (MYTEXT.split("//"))>1:
        if re.search ('--b',MYTEXT):
            MYTEXT = MYTEXT.replace('--b','')
            MYFRONT = MYTEXT.split("//")[1].strip()
            MYBACK = MYTEXT.split("//")[0].strip()
        else:
            MYFRONT = MYTEXT.split("//")[0].strip()
            MYBACK = MYTEXT.split("//")[1].strip()


    result["items"].extend([{
        "title": "▶️ "+ MYFRONT,
        "subtitle": "enter front and back separated by //, --b to invert",
        "arg": MYFRONT+"\x1f"+MYBACK,
            "variables": {
                "myMODID": myModID,
                "myDECKID": myDeckID
                
            },
        
        "icon": {"path": "icons/frontCard.png"}
        },{
        "title": MYBACK + " ◀️",
        "subtitle": "↩️ to save, ⇧↩️ save both sides",
        "arg": MYFRONT + "\x1f" + MYBACK,
        "variables": {
                "myModID": myModID,
                
            },
        
        "icon": {"path": "icons/backCard.png"}
        }])




print (json.dumps(result))






