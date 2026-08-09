#!/usr/bin/env python3
# encoding: utf-8
#
#
# Saturday, February 5, 2022, 11:51 AM
# Partly cloudy ⛅️  🌡️+23°F (feels +12°F, 63%) 🌬️↘16mph 🌒



import os


def _int_env(name, default=0):
    """Parse an integer config/runtime var. Alfred always sets the variable but
    leaves it '' when the config field is empty, so guard blank/invalid -> default."""
    try:
        return int(os.getenv(name, ''))
    except (TypeError, ValueError):
        return default


def _float_env(name, default=0.0):
    try:
        return float(os.getenv(name, ''))
    except (TypeError, ValueError):
        return default


AGAININTERVAL = _int_env('AGAININTERVAL')  # time to review (in secs) if again/hard
GOODINTERVAL = _int_env('GOODINTERVAL')    # time to review (in secs) if good
EASYINTERVAL = _int_env('EASYINTERVAL')    # time to review (in days) if easy
GRAD_INTERVAL = _int_env('GRAD_INTERVAL')  # graduating interval (default: 1)

# DEFAULT USER 1
ANKI_DATABASE = os.path.expanduser(os.getenv('ANKI_DATABASE', ''))  # ANKI database (a path)
DEFAULT_DECK = os.getenv('DEFAULT_DECKS', '')          # comma-separated deck names
DEF_CARD_TYPE = os.getenv('DEFAULT_NEWCARD_TYPE', '')  # note-type name
DEFAULT_DECK_NEW = os.getenv('DEFAULT_DECK_NEW', '')   # deck where new cards are added


INT_MODIFIER = _float_env('INT_MODIFIER')  # default interval modifier (1)
ANKI_MEDIA_FOLDER = os.path.dirname(ANKI_DATABASE) + '/collection.media/'

DECK_LIST = [x.strip() for x in DEFAULT_DECK.split(',') if x.strip()]

MYMODE = "Standard"
#MYMODE = "Verbose"

