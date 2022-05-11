#!/usr/bin/env python3
# encoding: utf-8
#
#
# Saturday, February 5, 2022, 11:51 AM
# Partly cloudy ⛅️  🌡️+23°F (feels +12°F, 63%) 🌬️↘16mph 🌒



import os


AGAININTERVAL = int(os.path.expanduser(os.getenv('AGAININTERVAL', '0'))) #time to review (in secs if hard
GOODINTERVAL = int (os.path.expanduser(os.getenv('GOODINTERVAL', '0'))) #time to review (in secs) if good
EASYINTERVAL = int(os.path.expanduser(os.getenv('EASYINTERVAL', '0'))) #time to review (in days) if easy
GRAD_INTERVAL = int(os.path.expanduser(os.getenv('GRAD_INTERVAL', '0'))) #graduating interval (default:1)

# DEFAULT USER 1
ANKI_DATABASE = os.path.expanduser(os.path.expanduser(os.getenv('ANKI_DATABASE', ''))) #ANKI database
DEFAULT_DECK = os.path.expanduser(os.getenv('DEFAULT_DECKS')) 
DEF_CARD_TYPE = os.path.expanduser(os.getenv('DEFAULT_NEWCARD_TYPE')) 
DEFAULT_DECK_NEW = os.path.expanduser(os.path.expanduser(os.getenv('DEFAULT_DECK_NEW', ''))) #Deck  where new cards are added


INT_MODIFIER =float(os.path.expanduser(os.getenv('INT_MODIFIER', '0'))) # default int modifier (1)
ANKI_MEDIA_FOLDER = os.path.dirname (ANKI_DATABASE)+'/collection.media/'

DECK_LIST = [x.strip() for x in DEFAULT_DECK.split(',') if x]

MYMODE = "Standard"
#MYMODE = "Verbose"

