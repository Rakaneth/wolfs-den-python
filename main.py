import tcod
import math

def clamp(val, low, high):
  if val < low:
    return low
  elif val > high:
    return high
  else:
    return val

def between(val, low, high):
  return clamp(val, low, high) == val


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

  DIRS = {
    'N': (0, -1),
    'NE': (1, -1),
    'E': (1, 0),
    'SE': (1, 1),
    'S': (0, 1),
    'SW': (-1, 1),
    'W': (-1, 0),
    'NW': (-1, 1),
    'NONE': (0, 0)
  }

  moves = {
    tcod.KEY_KP8: DIRS['N'],
    tcod.KEY_KP9: DIRS['NE'],
    tcod.KEY_KP6: DIRS['E'],
    tcod.KEY_KP3: DIRS['SE'],
    tcod.KEY_KP2: DIRS['S'],
    tcod.KEY_KP1: DIRS['SW'],
    tcod.KEY_KP4: DIRS['W'],
    tcod.KEY_KP7: DIRS['NW'],
    tcod.KEY_KP5: DIRS['NONE']
  }

  while not tcod.console_is_window_closed():
    root.clear()
    root.put_char(px, py, ord('@'))
    tcod.console_flush()
    key = tcod.console_wait_for_keypress(tcod.KEY_PRESSED)
    dirMove = moves.get(key.vk)
    
    if key and dirMove:
      dx, dy = dirMove
      px = clamp(px + dx, 0, SCREEN_W - 1)
      py = clamp(py + dy, 0, SCREEN_H - 1)
    elif key.vk != tcod.KEY_NONE:
      print(f"Unknown key pressed: {key.text}")

if __name__ == "__main__":
    main()