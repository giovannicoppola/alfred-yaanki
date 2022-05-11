#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### ALFRED-YAANKI OPS (updating tables after card review)
from __future__ import print_function
from yaankiFun import * 
import time
myTimeStamp = round(time.time() * 1000) #trying to capture the timestamp as close as possible to 'return' being pressed at the previous step


import sqlite3
import os
from config import ANKI_DATABASE, DEFAULT_DECK


CARDID=os.path.expanduser(os.getenv('myCardID', ''))
START_TS = os.path.expanduser(os.getenv('myStartTS', ''))
MYREPS = os.path.expanduser(os.getenv('last_reps', '')) #current reps
LAST_IVL = os.path.expanduser(os.getenv('last_ivl', ''))
DECK_ID = os.path.expanduser(os.getenv('deck_id', ''))

# 11 outcome-dependent variables
REV_EASE = os.path.expanduser(os.getenv('rev_ease', ''))
REV_IVL = os.path.expanduser(os.getenv('rev_ivl', ''))
REV_TYPE = os.path.expanduser(os.getenv('rev_type', ''))
REV_FACTOR = os.path.expanduser(os.getenv('rev_factor', ''))

CARD_TYPE = os.path.expanduser(os.getenv('card_type', '')) 
CARD_QUEUE = os.path.expanduser(os.getenv('card_queue', '')) 
CARD_DUE = os.path.expanduser(os.getenv('card_due', '')) 
CARD_IVL = os.path.expanduser(os.getenv('card_ivl', '')) 
CARD_FACTOR = os.path.expanduser(os.getenv('card_factor', '')) 
CARD_LAPS = os.path.expanduser(os.getenv('card_laps', '')) 
CARD_LEFT = os.path.expanduser(os.getenv('card_left', '')) 
            


myReviewTime = myTimeStamp - int(START_TS) # how many milliseconds your review took, up to 60,000 (60s)
if (myReviewTime>60000):
    myReviewTime = 60000

mySecTS = int(myTimeStamp/1000) # mod timestamp in seconds

db = sqlite3.connect(ANKI_DATABASE)
cursor = db.cursor()

## Overview: need to change three tables: 1) revlog, 2) cards, 3) decks

# 1 ## REVLOG TABLE
    # revlog table has 9 fields, 5 independent of outcome, 4 dependent
    #for revlog table (independent of outcome, n=5)
rev_id = myTimeStamp
rev_cid = CARDID
rev_usn = -1
rev_lastivl =  LAST_IVL
rev_time = myReviewTime



# 2 ## CARDS TABLE
    # cards table changes at review 9 fields, 2 independent of outcome, 7 dependent
cards_mod = mySecTS #(same as the ID of the revlog record, but in secs, not msecs)
card_reps = int(MYREPS) + 1 # one other option is to actually count reps in the revlog table, but I think the akni algorithm doesn't do that (reps count remains if you delete the revlog records)


# 3 ## DECKS table
decks_mtime = mySecTS    # changes one field only, last review epoch, outcome-independent




#### UPDATING THREE TABLES (REVLOG, CARDS, DECKS)
try:
# 1 REVLOG TABLE ### INSERTING REVIEW INFORMATION IN THE DATABASE (REVLOG table)
    cursor.execute(""" INSERT INTO "revlog" (id, cid, usn, ease, ivl, lastIvl, factor, time, type)
        VALUES(
            ?,           -- unique review ID (timestamp)
            ?,           -- card id
            ?,           -- usn: to send on next synchronization
            ?,           -- review:  1(hard), 3(ok), 4(easy)
            ?,           -- interval (i.e. as in the card table) negative = second (10 minutes)
            ?,           -- last interval (i.e. the last value of ivl. Note that this value is not necessarily equal to the actual interval between this review and the preceding review)
            ?,           -- factor 
            ?,           -- how many milliseconds your review took, up to 60000 (60s)
            ?            -- 0=learn, 1=review, 2=relearn, 3=cram
        )""",(rev_id,rev_cid,rev_usn, REV_EASE,REV_IVL,rev_lastivl, REV_FACTOR, rev_time,REV_TYPE,))


# 2. CARDS TABLE ### UPDATING THE CARDS TABLE
    cursor.execute("""UPDATE cards SET 

        mod = ?,   -- most recent revlog timestamp in sec
        type = ?,  -- 0=new, 1=learning, 2=review, 3=relearning
        queue = ?,  -- 1=learning
        due =?,    -- due date/time in sec
        ivl =?,
        factor =?,
        reps = ?,  -- number of reviews from the `revlog` table
        lapses =?,
        left =?
        WHERE id = ?""", (cards_mod,CARD_TYPE, CARD_QUEUE, CARD_DUE,CARD_IVL,CARD_FACTOR,card_reps, CARD_LAPS,CARD_LEFT, CARDID,))

# 3. DECKS TABLE ### UPDATING THE DECKS TABLE
    cursor.execute("""UPDATE decks SET 
        mtime_secs = ?  --  ID of the most recent `revlog` entry/1000 (in secs, not msecs)
        where id = ?
         """,(decks_mtime, DECK_ID,))



    db.commit()



except sqlite3.OperationalError as err:
    raise err

finally:
    cursor.close()
    db.close()



