#!/usr/bin/env python3
### yaanki
## creating a new card 
## Thursday, November 4, 2021, 8:39 AM

import sqlite3
import time
import sys
import hashlib
import os

from config import ANKI_DATABASE
from yaankiFun import * 

db = sqlite3.connect(ANKI_DATABASE)
cursor = db.cursor()
myTimeStamp = round(time.time() * 1000)

def guid_for(*values):
    ### function to generate the global id from the link below. 
    #https://github.com/kerrickstaley/genanki/blob/fc8148ab5cabeb16e8957ebb3e7d8ec48bed7cf5/genanki/util.py
    #the function takes all the values, but only the first 2 are passed in this package

    #'By default, the GUID is a hash of all the field values. This may not be desirable if, for example, you add a new field with additional info that doesn't change the identity of the note. 
    #You can create a custom GUID implementation to hash only the fields that identify the note:'

    BASE91_TABLE = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
  't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
  'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4',
  '5', '6', '7', '8', '9', '!', '#', '$', '%', '&', '(', ')', '*', '+', ',', '-', '.', '/', ':',
  ';', '<', '=', '>', '?', '@', '[', ']', '^', '_', '`', '{', '|', '}', '~']

    hash_str = '__'.join(str(val) for val in values)

    # get the first 8 bytes of the SHA256 of hash_str as an int
    m = hashlib.sha256()
    m.update(hash_str.encode('utf-8'))
    hash_bytes = m.digest()[:8]
    hash_int = 0
    for b in hash_bytes:
        hash_int <<= 8
        hash_int += b

  # convert to the weird base91 format that Anki uses
    rv_reversed = []
    while hash_int > 0:
        rv_reversed.append(BASE91_TABLE[hash_int % len(BASE91_TABLE)])
        hash_int //= len(BASE91_TABLE)

    return ''.join(reversed(rv_reversed))



myModID = os.getenv('myMODID')
myDeckID = os.getenv('myDECKID')


myTags = ''

myString = sys.argv[1]
myHash = guid_for(myTimeStamp,myString)

myQuestion = myString.split("\x1f")[0]


### adding a new record to 'notes'
count = cursor.execute (""" INSERT INTO "notes"
  VALUES(
    ?,  -- unique ID (myTimeStamp)
    ?,  -- unique ID (myHash)
    ?,  -- note model ID 
    ?,  -- modification timestamp, epoch seconds (timestamp/1000)
    -1, -- update sequence number: for finding diffs when syncing.
    ?,  -- space-separated string of tags. (myTags)
    ?,  -- the values of the fields in this note. separated by 0x1f (31) character. (myString)
    ?,  -- sort field: used for quick sorting and duplicate check. The sort field is an integer so that when users are sorting on a field that contains only numbers, they are sorted in numeric instead of lexical order. Text is stored in this integer field.
    '',  -- field checksum used for duplicate check.
    0,  -- flags, unused
    '') -- data, unused
    """,(myTimeStamp,myHash,myModID,round((myTimeStamp/1000),0),myTags,myString,myQuestion))


### adding a new record to 'cards'
count = cursor.execute (""" INSERT INTO "cards"
  VALUES(
    ?, -- cardID (timestamp)
    ?, -- note ID (also my timestamp for now)
    ?, -- did (deck ID)
    0, -- ord
    0, -- mod
    -1, -- usn
    0,  -- type
    0,  -- queue
    0, -- due
    1, -- ivl
    0, -- factor
    0, -- reps
    0, -- lapses
    0, -- left
    0, -- odue
    0, -- odid
    0, -- flags
    '' --data
    )
    """,(myTimeStamp,myTimeStamp,myDeckID))

db.commit()

## note: will need to add to the tags table as well if I implement tags

