# yaanki <img src="images/icon.png" width="30"/>
### yet another alfred anki (workflow)


<a href="https://github.com/giovannicoppola/alfred-yaanki/releases/latest/">
<img alt="Downloads"
src="https://img.shields.io/github/downloads/giovannicoppola/alfred-yaanki/total?color=purple&label=Downloads"><br/>
</a>

![](images/alfred-yaanki.gif)


<!-- MarkdownTOC autolink="true" bracket="round" depth="3" autoanchor="true" -->

- [Motivation](#motivation)
- [Setting up](#setting-up)
- [Usage](#usage)
- [Limitations & Known Issues](#known-issues)
- [Acknowledgments](#acknowledgments)
- [Changelog](#changelog)
- [Feedback](#feedback)

<!-- /MarkdownTOC -->



<h1 id="motivation">motivation ✅</h1>

1. **Search:** ability to quickly look up a card from any anki deck (searching both sides of cards), even if it is not scheduled for review. 
	- Once reviewed, I would like to record the outcome and get credit for review.
2. **Create:** ability to quickly create cards from Alfred. 
3. **Study:** ability to review scheduled cards ('study') using Alfred. 


<h1 id="setting-up">setting up⚙️</h1>

1. 🚨BACK UP YOUR DECKS!🚨 yaanki is still being developed. you don't want to lose your precious cards. Howto [here](https://docs.ankiweb.net/backups.html)
2. Open the 'Configure Workflow' window in paperpAlfred preferences
3. set the user directory with Anki decks (if needed, the default: `~/Library/Application Support/Anki2/User 1/collection.anki2` should work in most cases).
4. optional settings (if you are not familiar with these parameters, you can leave the defaults or find additional information in the Anki documentation):
	- set `AGAININTERVAL` (default: 60 seconds). Interval after which a card marked `🔴again` becomes due
	- set `GOODINTERVAL` (default: 600 seconds). Interval after which a card marked `🟢good` becomes due
	- set `EASYINTERVAL` (default: 4 days). Interval after which a card marked `🍰easy` becomes due
	- set `EASE_FACTOR` (default: 2500)
	- set `EASY_BONUS` (default: 1.3)
	- set `GRAD_INTERVAL` (default: 1)
	- set `INT_MODIFIER` (default: 1)


<h1 id="usage">usage 📖</h1>

## creating new cards 📝
- you can create a new card by entering the corresponding keyword (default: `!a`) or hotkey, then entering (or pasting into Alfred) the text of front and back separated by `//`. `--b` will invert front and back. New cards will be added to the deck listed in the `DEFAULT_DECK_NEW` Alfred environment variable, or – if that is not set – the `Default` deck. 
- Universal Action: new cards can also be created by selecting text in any app, then launching Universal Actions and selecting 'Create New Anki Card with yaanki`. 

 
## looking up a card 📇

- launch yaanki by entering the corresponding keyword (default: `!s`) or hotkey and search for a card by typing in Alfred. yaanki will show the front of the card, and the deck it is from. The Anki star color will indicate the due status. Hitting `Enter` will show the back of the card and the times (or days) it will be due based on the outcome you will indicate. 
- `ctrl-Enter` will show card details (date creation, number of reviews, due date etc)
- `option-Enter` will show the card front in large type
- 🖼️ denotes an image present in the card front or back. Hit `Shift` to show it in preview 

## studying with yaanki 🗂️ 
- you can set the decks from which cards are presented by entering `yaanki:decks` in Alfred, or setting a hotkey. Shift-Enter will add or remove a deck from the list. THe deck list can also be edited in Alfred's workflow variables. 
- launch yaanki with keyword or hotkey. if no search text is entered, cards are presented ordered by due date (new cards first), so review all the ones that are overdue


<h1 id="known-issues">limitations & known issues ⚠️</h1>

- only works with one-line text cards
- scheduling algorithm is reverse-engineered and simplified, although some default scheduling options can be set by the user. No 'fuzz factor' delays in review not taken into account etc. It works for my purposes, but I haven't tested all use cases. 
- limited to one user profile (but can be switched in setting, as in the anki app)
- will not work while the anki app is open  
- only 3 ease level options (instead of the typical 4) when studying:
    - Hard (default: 60 sec - can be customized with `AGAININTERVAL`)
    - Good (default: 10 min - can be customized with `GOODINTERVAL`)
    - Piece of cake (default: 4 days - can be customized with `EASYINTERVAL`)
- hidden fields in cards (e.g. ID) are shown if they are present in the card template
- need to open the Anki app to sync changes on the Anki server (AnkiWeb)
- sub-decks not tested
- occasional warnings from the Anki app to 'fix the database', probably in relation to AnkiWeb
- currently all the fields beyond the first (front of the card) are joined in one (reverse). this can be changed  
- Most of the cards I use every day are one-liners. This will not work for cards with complex text, media etc. 


<h1 id="roadmap">roadmap 🛣️</h1>

- option to search questions only (currently searching both questions and answers)
- implement tags
- delete cards, edit cards
- creating cards with images through yannki



<h1 id="acknowledgments">thank you 🙂</h1>

- @kerrickstaley for the gUId, modelID generating [function](https://github.com/kerrickstaley/genanki/blob/fc8148ab5cabeb16e8957ebb3e7d8ec48bed7cf5/genanki/util.py)
- Anki icon from [papyrus apps](https://icon-icons.com/icon/anki/93962)
- <a href="https://www.flaticon.com/free-icons/card" title="card icons">Card icons created by Victoruler - Flaticon</a>
- <a href="https://www.flaticon.com/free-icons/flash-cards" title="flash cards icons">Flash cards icons created by Freepik - Flaticon</a>
- <a href="https://www.flaticon.com/free-icons/tick" title="tick icons">Tick icons created by Freepik - Flaticon</a>
- [Vítor Galvão](https://github.com/vitorgalvao) for [OneUpdater](https://github.com/vitorgalvao/alfred-workflows/tree/master/OneUpdater) and terrific help on the Alfred forum.
- [Dean Jackson](https://github.com/deanishe) for help on the Alfred forum and for sharing scripts used as inspiration for this workflow. 
- The [Alfred forum](https://www.alfredforum.com) community.



<h1 id="changelog">changelog 🧰</h1>

- 12-04-2022: version 0.2 (Alfred 5)
- 05-11-2022: version 0.1

<h1 id="feedback">feedback 🧐</h1>

Feedback welcome! If you notice a bug, or have ideas for new features, please feel free to get in touch either here, or on the [Alfred](https://www.alfredforum.com) forum. 


 
