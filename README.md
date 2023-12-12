# Readme

## install requirements
* python >= 3.10
* tesseract >= 5.3 https://tesseract-ocr.github.io/tessdoc/Installation.html
* requirements.txt ```pip install -r requirements.txt```

## Let it run
```python main.txt```

## configuration
in ./ data folder ony the "required.json" should be edited

### class
set ur classname here:
* barbarian
* druid
* necromancer
* rogue
* sorcerer

### bis
Put required unique items or needed attributes here

Unique example:
```
"helm": {
    "unique": true,
    "name": "Godslayer Crown"
},
```
Attributes example:
```
"chest": {
    "min_match_count": 3, // this are the minimal count of matches for a success
    "attribut1": "Total Armor",
    "attribut2": "Damage Reduction from Distant Enemies",
    "attribut3": "Damage Reduction from Close Enemies",
    "attribut4": "Damage Reduction from Burning Enemies"
},
```
Aspects:
Add them to the array. 
```
"aspects": [
    "mage-lord-aspect",
    "aspect-of-disobedience",
    ...
]
```
For now only supported aspects are:
* storm-swell-aspect
* snowveiled-aspec
* conceited-aspect
* mage-lords-aspect
* aspect-of-disobedience
* aspect-of-control
* gravitational-aspect

check is attributes > aspect!

## TODO
- [ ] Load data from https://mobalytics.gg/
- [ ] Item Power needs >= required as part of requirement
- [ ] Wapon needs to be checkt the whole list for one hand or two hand and attributes
- [ ] Offhand needs to be checkt the whole list for attributes
- [x] TN-1 - Find also Aspects on legendaries
- [ ] O and OO in name is not nice to parse cause d4 font need a regex fix here
- [ ] squares should despawn after an amount of time
- [ ] squares should sourounded mouse possition (at the moment mous position is left top)
- [ ] support multiple languages (only englisch at the moment)
- [ ] tests
- [x] TN-2 - require.txt
- [ ] Adding all aspects
- [ ] Aspects only for required class
- [ ] Find items two-handed needs be checked before one hands!
- [ ] Process is not killed by pressing Q
- [ ] User interface for configuration



## Misc only for me for dev. Too lazy to put it somewhere else :P
* (CHECK) Wapon needs to be checkt the whole list for one hand or two hand and attributes // get from internal list
* offhand needs to be checkt the whole list for attributes // get from internal list
https://diablo4.wiki.fextralife.com/Weapons

Barbarian
Mainhand: 1 Handed Axe, 2 Handed Axe, 1 Handed Sword, 2 Handed Sword, 1 Handed Mace, 2 Handed Mace, Polearm, 
Offhand: 1 Handed Axe, 1 Handed Sword, 1 Handed Mace, 

Druid
Mainhand: 1 Handed Axe, 2 Handed Axe, 1 Handed Mace, 2 Handed Mace, Staff, 2 Handed Staff,
Offhand:

Necromancer
Mainhand: 1 Handed Sword, 2 Handed Sword, 1 Handed Scythe, 2 Handed Scythe, Staff, 2 Handed Staff,
Offhand: Wand, Shield, Focus

Rogue
Mainhand: 1 Handed Sword, Dagger, Bow, Crossbow, 
Offhand: 1 Handed Sword, Dagger,

Sorcerer
Mainhand: Dagger, Staff, 2 Handed Staff,
Offhand: Wand, Focus

2-Hand Mace
2-Hand Sword