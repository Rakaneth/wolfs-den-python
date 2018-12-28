# Wolf's Den, Python #

A Python implementation of my roguelike concept Wolf's Den, used as a starter project for learning new langauges.

Lots of code lifted from [here](https://github.com/TStand90/roguelike_tutorial_revised)

# DONE #

* Moving @
* Screen scaffolding
* Command interface
* Main Screen UI
* Creature File Parser

# ISSUES #

## 2018-12-28 ##

* python-tcod appears to have a bug in line 2524 of libtcodpy.py. Updating `_parser_listener.end_struct` to `_parser_listener.end_struct` seems to fix the issue. A bug issue has been raised.