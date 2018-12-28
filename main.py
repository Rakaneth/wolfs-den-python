import tcod
import math
import parsers
from utils import clamp
from screen import Screen, MainScreen
from entity import Entity


def main():
    SCREEN_W = 100
    SCREEN_H = 40
    LIMIT_FPS = 20

    font_file = 'Cheepicus_14x14.png'
    font_flags = tcod.FONT_TYPE_GRAYSCALE | tcod.FONT_LAYOUT_ASCII_INROW
    tcod.console_set_custom_font(font_file, font_flags)

    window_title = 'Wolf\'s Den 2: Python Edition'
    fullscreen = False
    root = tcod.console_init_root(SCREEN_W, SCREEN_H, window_title, fullscreen)
    tcod.sys_set_fps(LIMIT_FPS)

    Screen.register(MainScreen(root))
    Screen.setScreen('main')

    player = Entity()
    player.stats = dict(str=10, spd=10)
    print(player)

    creature_file = 'data/entity/creatures.dat'
    parsers.parse_creatures(creature_file)
    for _, temp in parsers.CREATURE_TEMPLATES.items():
        print(temp)

    while not tcod.console_is_window_closed():
        root.clear()
        Screen.cur_screen.render()
        root.put_char(player.x, player.y, player.glyph)
        tcod.console_flush()
        key = tcod.console_wait_for_keypress(tcod.KEY_PRESSED)
        cmd = Screen.cur_screen.handle_keys(key)
        val = cmd.execute(player)
        if val == -1:
            break


if __name__ == '__main__':
    main()
