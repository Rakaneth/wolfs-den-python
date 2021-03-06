﻿import tcod
import math
import parsers
import factory

from utils import clamp
from screen import Screen, MainScreen
from entity import Entity
from world import WORLD


def main():
    SCREEN_W = 100
    SCREEN_H = 40

    font_file = 'Cheepicus_14x14.png'
    font_flags = tcod.FONT_TYPE_GRAYSCALE | tcod.FONT_LAYOUT_ASCII_INROW
    tcod.console_set_custom_font(font_file, font_flags)

    window_title = 'Wolf\'s Den 2: Python Edition'
    fullscreen = False
    root = tcod.console_init_root(SCREEN_W, SCREEN_H, window_title, fullscreen)

    creature_file = 'data/entity/creatures.dat'
    equip_file = 'data/entity/equip.dat'
    item_file = 'data/entity/items.dat'
    mat_file = 'data/entity/materials.dat'
    map_file = 'data/maps.dat'
    parsers.parse_creatures(creature_file)
    parsers.parse_materials(mat_file)
    parsers.parse_equip(equip_file)
    parsers.parse_items(item_file)
    parsers.parse_maps(map_file)

    Screen.register(MainScreen(root))
    Screen.setScreen('main')

    while not tcod.console_is_window_closed():
        root.clear()
        Screen.cur_screen.render()
        tcod.console_flush()
        key = tcod.console_wait_for_keypress(tcod.KEY_PRESSED)
        cmd = Screen.cur_screen.handle_keys(key)
        val = cmd.execute(WORLD.player)
        if val == -1:
            break


if __name__ == '__main__':
    main()
