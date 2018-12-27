import tcod
import math
from utils import clamp
from screen import Screen, MainScreen


def main():
    SCREEN_W = 100
    SCREEN_H = 40
    LIMIT_FPS = 20
    px = 0
    py = 0

    font_file = 'Cheepicus_14x14.png'
    font_flags = tcod.FONT_TYPE_GRAYSCALE | tcod.FONT_LAYOUT_ASCII_INROW
    tcod.console_set_custom_font(font_file, font_flags)

    window_title = "Wolf's Den 2: Python Edition"
    fullscreen = False
    root = tcod.console_init_root(SCREEN_W, SCREEN_H, window_title, fullscreen)
    tcod.sys_set_fps(LIMIT_FPS)

    Screen.register(MainScreen(root))
    Screen.setScreen('main')

    while not tcod.console_is_window_closed():
        root.clear()
        root.put_char(px, py, ord('@'))
        tcod.console_flush()
        key = tcod.console_wait_for_keypress(tcod.KEY_PRESSED)
        cmd = Screen.cur_screen.handle_keys(key)
        cmdType = cmd['type']
        if cmdType == 'move-by':
            dx, dy = cmd['by']
            px = clamp(px + dx, 0, SCREEN_W - 1)
            py = clamp(py + dy, 0, SCREEN_H - 1)
        elif cmdType == 'wait':
            pass
        elif cmdType == 'exit':
            break
        elif key.vk != tcod.KEY_NONE:
            print(f"Unknown key pressed: {key.text}")
        else:
            pass


if __name__ == "__main__":
    main()
