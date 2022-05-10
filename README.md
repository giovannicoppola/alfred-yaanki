# yaanki <img src="images/icon.png" width="30"/>
### yet another alfred anki (workflow)


<a href="https://github.com/giovannicoppola/alfred-yaanki/releases/latest/">
<img alt="Downloads"
src="https://img.shields.io/github/downloads/giovannicoppola/alfred-yaanki/total?color=purple&label=Downloads"><br/>
</a>

![](alfred-yaanki.gif)


<!-- MarkdownTOC autolink="true" bracket="round" depth="3" autoanchor="true" -->

- [Motivation](#motivation)
- [Setting up](#setting-up)
- [Usage](#usage)
- [Limitations & Known Issues](#known-issues)
- [Acknowledgments](#acknowledgments)
- [Changelog](#changelog)
- [Feedback](#feedback)

<!-- /MarkdownTOC -->



<a name="motivation"></a>
# motivation ✅
1. **Search:** ability to quickly look up a card from any anki deck (searching both sides of cards), even if it is not scheduled for review. 
	- Once reviewed, I would like to record the outcome and get credit for review
2. **Create:** ability to quickly create cards from Alfred. 
3. **Study:** ability to review scheduled cards ('study') using Alfred. 

<a name="setting-up"></a>
# setting up ⚙️
1. 🚨BACK UP YOUR DECKS!🚨 yaanki is still being developed. you don't want to lose your precious cards. Howto [here](https://docs.ankiweb.net/backups.html)
2. set the user directory with Anki decks (if needed, default should work in most cases. Default: `~/Library/Application Support/Anki2/User 1/collection.anki2`)
3. optional settings (if you are not familiar with these parameters, you can find additiona information in the Anki documentation):
	- set `AGAININTERVAL` (default: 60 seconds). Interval after which a card marked `🔴again` becomes due
	- set `GOODINTERVAL` (default: 600 seconds). Interval after which a card marked `🟢good` becomes due
	- set `EASYINTERVAL` (default: 4 days). Interval after which a card marked `🍰easy` becomes due
	- set `EASE_FACTOR` (default: 2500)
	- set `EASY_BONUS` (default: 1.3)
	- set `GRAD_INTERVAL` (default: 1)
	- set `INT_MODIFIER` (default: 1)
- 

<a name="usage"></a>
# usage 📖
## creating new cards 📝
- you can create a new card by entering the corresponding keyword (default: `!a`) or hotkey, then entering (or pasting into Alfred) the text of front and back separated by `//`. `--b` will invert front and back. New cards will be added to the deck listed in the `DEFAULT_DECK_NEW` Alfred environment variable, or – if that is not set – the `Default` deck. 
- Universal Action: new cards can also be created by selecting text in any app, then launching Universal Actions and selecting 'Create New Anki Card with yaanki`. 

 
## looking up a card 🗃️

- ... yaanki will show the front of the card, the deck it is from. The Anki star color will indicate the due status. Hitting `Enter` will show the back of the card and the times (or days) it will be due based on the outcome you will indicate. 
- `ctrl-Enter` will show card details (date creation, number of reviews, due date etc)
- `option-Enter` will show the card front in large type
- 🖼️ denotes an image present in the card front or back. Hit `Shift` to show it as a preview item

## studying with yaanki 🗂️
- if no search text is entered, cards are presented ordered by due date (new cards first), so review all the ones that are overdue



<a name="known-issues"></a>
# limitations & known issues ⚠️
- only works with one-line text cards
- scheduling algorithm is reverse-engineered and simplified, although some default scheduling options can be set by the user. No 'fuzz factor' delays in review not taken into account etc. It works for my purposes, but I haven't tested all use cases. 
- limited to one deck (but can be switched, same as anki app)
- will not work while the anki app is open  
- only 3 ease level options (instead of the typical 4) when studying:
    - Hard (default: 60 sec - can be customized with `AGAININTERVAL`)
    - Good (default: 10 min - can be customized with `GOODINTERVAL`)
    - Piece of cake (default: 4 days - can be customized with `EASYINTERVAL`)
- hidden fields in cards (e.g. ID) are shown if they are present in the card template
- need to open the Anki app to sync changes on the Anki server
- sub-decks not tested
- currently all the fields beyond the first (front of the card) are joined in one (reverse). this can be changed  
- Most of the cards I use every day are one-liners. This will not work for cards with complex text, media etc. 


<a name="roadmap"></a>
# roadmap 🛣️
- option to search questions only (now it searches both questions and answers), could be by searching the field sfld as opposed to flds
- implement tags
- (Delete cards, Edit cards)
- creating cards with images through yannki
- add poll to this section
- add oneupdated
- add review time to card info


<a name="acknowledgments"></a>
# thank you 🙂
- vitor and deanishe, oneupdater
- drlulz for collecting some tools
- benjamin gray for simple query script
- @kerrickstaley for the gUId, modelID generating [function](https://github.com/kerrickstaley/genanki/blob/fc8148ab5cabeb16e8957ebb3e7d8ec48bed7cf5/genanki/util.py)
- Anki icon from [papyrus apps](https://icon-icons.com/icon/anki/93962)
- <a href="https://www.flaticon.com/free-icons/card" title="card icons">Card icons created by Victoruler - Flaticon</a>
- <a href="https://www.flaticon.com/free-icons/flash-cards" title="flash cards icons">Flash cards icons created by Freepik - Flaticon</a>
- <a href="https://www.flaticon.com/free-icons/tick" title="tick icons">Tick icons created by Freepik - Flaticon</a>


<a name="changelog"></a>
# Changelog 🧰

- 04-23-2022: version 0.1

<a name="feedback"></a>
# Feedback 🧐

Feedback welcome! If you notice a bug, or have ideas for new features, please feel free to get in touch either here, or on the [Alfred](https://www.alfredforum.com) forum. 


 
