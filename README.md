# Wolf's Den, Python #

A Python implementation of my roguelike concept Wolf's Den, used as a starter project for learning new languages.

Lots of code lifted from [here](https://github.com/TStand90/roguelike_tutorial_revised)

# DONE #

* Moving @
* Screen scaffolding
* Command interface
* Main Screen UI
* Libtcod-style file parsers (not really necessary in Python, but I have the files from my C++ port already)

# ISSUES #

## 2018-12-28 ##

* python-tcod appears to have a bug in line 2524 of libtcodpy.py. Updating `_parser_listener.end_struct` to `_parser_listener.new_struct` seems to fix the issue. A bug issue has been raised. (Fixed 12-29)

## 2019-1-4 ##

I have decided to throw in the towel with libtcod. I would rather be implementing my game's systems than re-implementing basic dungeon generation. The one thing I really like about libtcod is the custom parser; most modern languages, though - even compiled ones - can now handle a modern file format such as json or (my preference) yaml. Feel free to fork/modify as you see fit, but this repo is officially abandoned.