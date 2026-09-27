#!/usr/bin/env python3
### yaanki
## creating a new card 
## Thursday, November 4, 2021, 8:39 AM

import sqlite3
import time
import sys
import hashlib
import os
import html

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



myModID = int(os.getenv('myMODID'))
myDeckID = int(os.getenv('myDECKID'))
bothSides = os.getenv('bothSides') == '1'  # ⇧↩️: also save the reversed card (back -> front)

myTags = ''

myString = sys.argv[1] if len(sys.argv) > 1 else ''
myFront, _, myBack = myString.partition("\x1f")

NOTETYPE = noteTypeInfo(db, myModID)


def nextID(table):
    """Anki ids are ms timestamps; take now, or one past the newest id if that is later."""
    (maxID,) = cursor.execute(f'SELECT max(id) FROM {table}').fetchone()
    return max(myTimeStamp, (maxID or 0) + 1)


def stripHTML(myText):
    return html.unescape(removeTags(myText)).strip()


def addNote(front, back):
    # the note must have exactly as many fields as its note type, otherwise Anki crashes
    # opening it (IndexError in notes.items) and 'Check Database' flags it
    fields = ([front, back] + [''] * NOTETYPE["nfields"])[:max(NOTETYPE["nfields"], 1)]
    noteID = nextID('notes')
    myFlds = "\x1f".join(fields)
    sortField = stripHTML(fields[min(NOTETYPE["sortf"], len(fields) - 1)])
    checksum = int(hashlib.sha1(stripHTML(fields[0]).encode('utf-8')).hexdigest()[:8], 16)

    ### adding a new record to 'notes'
    cursor.execute(""" INSERT INTO "notes"
      VALUES(
        ?,  -- unique ID (timestamp)
        ?,  -- globally unique ID (hash)
        ?,  -- note model ID
        ?,  -- modification timestamp, epoch seconds
        -1, -- update sequence number: for finding diffs when syncing.
        ?,  -- space-separated string of tags. (myTags)
        ?,  -- the values of the fields in this note. separated by 0x1f (31) character.
        ?,  -- sort field: used for quick sorting and duplicate check.
        ?,  -- field checksum used for duplicate check: first 8 hex digits of sha1(first field)
        0,  -- flags, unused
        '') -- data, unused
        """, (noteID, guid_for(noteID, myFlds), myModID, int(noteID / 1000), myTags, myFlds, sortField, checksum))

    ### adding a record to 'cards' for each template that this note generates
    # (e.g. 'Basic (and reversed card)' gets both directions, as when adding in Anki)
    for cardOrd in cardOrds(NOTETYPE, fields):
        cursor.execute(""" INSERT INTO "cards"
          VALUES(
            ?, -- cardID (timestamp)
            ?, -- note ID
            ?, -- did (deck ID)
            ?, -- ord (template)
            ?, -- mod
            -1, -- usn
            0,  -- type
            0,  -- queue
            0, -- due
            0, -- ivl
            0, -- factor
            0, -- reps
            0, -- lapses
            0, -- left
            0, -- odue
            0, -- odid
            0, -- flags
            '' --data
            )
            """, (nextID('cards'), noteID, myDeckID, cardOrd, int(noteID / 1000)))


addNote(myFront, myBack)
if bothSides and myBack:
    addNote(myBack, myFront)

# bump the collection modification time so that the next Anki sync picks up the new cards
cursor.execute('UPDATE col SET mod = ?', (round(time.time() * 1000),))

db.commit()

## note: will need to add to the tags table as well if I implement tags
