import tcod
from utils import DIRS


class Screen:
    screens = {}
    cur_screen = None

    @classmethod
    def register(cls, *screens):
        for screen in screens:
            cls.screens[screen.name] = screen

    @classmethod
    def setScreen(cls, screenName):
        if cls.cur_screen is not None:
            cls.cur_screen.exit()
        cls.cur_screen = cls.screens[screenName]
        cls.cur_screen.enter()

    def __init__(self, name, root):
        self.name = name
        self.root = root

    def render(self):
        raise NotImplementedError

    def handle_keys(self, key):
        raise NotImplementedError

    def exit(self):
        print(f"Exited {self.name} screen.")

    def enter(self):
        print(f"Entered {self.name} screen.")


class MainScreen(Screen):
    def __init__(self, root):
        Screen.__init__(self, 'main', root)
        MAP_W = 60
        MAP_H = 30
        MSG_W = 40
        MSG_H = 10
        SKILL_W = 30
        SKILL_H = 10
        INFO_W = 30
        INFO_H = 10
        STAT_W = 40
        STAT_H = 30
        self.map_con = tcod.console_new(MAP_W, MAP_H)
        self.msg_con = tcod.console_new(MSG_W, MSG_H)
        self.skill_con = tcod.console_new(SKILL_W, SKILL_H)
        self.info_con = tcod.console_new(INFO_W, INFO_H)
        self.stat_con = tcod.console_new(STAT_W, STAT_H)

    def render(self):
        self.render_map()
        self.render_msg()
        self.render_skill()
        self.render_info()
        self.render_stat()

    def render_map(self):
        self.map_con.clear()
        self.map_con.print_frame(0, 0, 0, 0, "Map")
        tcod.console_blit(self.map_con, 0, 0, self.map_con.width,
                          self.map_con.height, self.root, 0, 0)

    def render_msg(self):
        self.msg_con.clear()
        self.msg_con.print_frame(0, 0, 0, 0, "Messages")
        tcod.console_blit(self.msg_con, 0, 0, self.msg_con.width,
                          self.msg_con.height, self.root, 0, 30)

    def render_skill(self):
        self.skill_con.clear()
        self.skill_con.print_frame(0, 0, 0, 0, "Skills")
        tcod.console_blit(self.skill_con, 0, 0, self.skill_con.width,
                          self.skill_con.height, self.root, 40, 30)

    def render_info(self):
        self.info_con.clear()
        self.info_con.print_frame(0, 0, 0, 0, "Info")
        tcod.console_blit(self.info_con, 0, 0, self.skill_con.width,
                          self.skill_con.height, self.root, 70, 30)

    def render_stat(self):
        self.stat_con.clear()
        self.stat_con.print_frame(0, 0, 0, 0, "Stats")
        tcod.console_blit(self.stat_con, 0, 0, self.stat_con.width,
                          self.stat_con.height, self.root, 60, 0)

    def handle_keys(self, key):
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

        dirMoves = moves.get(key.vk)
        if dirMoves:
            return {'type': 'move-by', 'objID': 'player', 'by': dirMoves}
        elif key.vk == tcod.KEY_ESCAPE:
            return {'type': 'exit'}
        else:
            return {'type': 'wait', 'objID': 'player'}
