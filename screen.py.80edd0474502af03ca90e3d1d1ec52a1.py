import tcod
import commands
import factory
from utils import DIRS, clamp
from world import WORLD


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

    @staticmethod
    def border(con, caption):
        con.print_frame(0, 0, con.width, con.height, caption, False)

    def __init__(self, name, root):
        self.name = name
        self.root = root

    def render(self):
        raise NotImplementedError

    def handle_keys(self, key: tcod.Key) -> commands.Command:
        raise NotImplementedError

    def exit(self):
        print(f'Exited {self.name} screen.')

    def enter(self):
        print(f'Entered {self.name} screen.')

    def blit(self, con, x, y):
        tcod.console_blit(con, 0, 0, con.width, con.height, self.root, x, y)

    def center_on_point(self, con, x, y, w, h, dx, dy):
        tcod.console_blit(con, x, y, w, h, self.root, dx, dy)


def new_game():
    mines = factory.rooms("mines", "Mines", 85, 85, tcod.dark_sepia,
                          tcod.darker_sepia, False)
    WORLD.add_map(mines)
    WORLD.set_cur_map("mines")
    player = factory.creature_from_template("wolf", 'mines')
    axe = factory.equip_from_template('axe', 'iron', 'mines')
    WORLD.make_player(player)
    WORLD.add_entity(axe)


class MainScreen(Screen):
    MAP_VIEW_W = 60
    MAP_VIEW_H = 30

    def __init__(self, root):
        Screen.__init__(self, 'main', root)
        MAP_W = 100
        MAP_H = 100

        MSG_W = 40
        MSG_H = 10
        SKILL_W = 20
        SKILL_H = 10
        INFO_W = 40
        INFO_H = 10
        STAT_W = 40
        STAT_H = 30
        self.map_con = tcod.console_new(MAP_W, MAP_H)
        self.msg_con = tcod.console_new(MSG_W, MSG_H)
        self.skill_con = tcod.console_new(SKILL_W, SKILL_H)
        self.info_con = tcod.console_new(INFO_W, INFO_H)
        self.stat_con = tcod.console_new(STAT_W, STAT_H)
        self.game_init = True

    def enter(self):
        Screen.enter(self)
        if self.game_init:
            new_game()
            self.game_init = False

    def render(self):
        self.render_map()
        self.render_msg()
        self.render_skill()
        self.render_info()
        self.render_stat()

    def cam(self, entity):
        m = WORLD.cur_map
        mw = m.width
        mh = m.height
        sw = MainScreen.MAP_VIEW_W
        sh = MainScreen.MAP_VIEW_H
        left = clamp(entity.x - sw // 2, 0, max(0, mw - sw))
        top = clamp(entity.y - sh // 2, 0, max(0, mh - sh))
        return (left, top)

    def render_map(self):
        cx, cy = self.cam(WORLD.player)
        m = WORLD.cur_map
        for wx, wy in [(x, y) for (x, y) in m if m.is_dirty(x, y)]:
            t = m.get_tile(wx, wy)
            map_color = m.floor_color if t.walk else m.wall_color
            visible = m.light or WORLD.player.can_see(wx, wy)
            explored = m.is_explored(wx, wy)
            if t.glyph and (visible or explored):
                if visible:
                    fg = t.fg or map_color
                    bg = t.bg or map_color
                elif explored:
                    fg = t.walk and tcod.dark_blue or tcod.darker_blue
                    bg = fg
                tcod.console_put_char_ex(self.map_con, wx, wy, t.glyph, fg, bg)
            if visible:
                things = WORLD.things_at(wx, wy)
                sorted(things, key=lambda t: t.layer)
                for thing in things:
                    tt = m.get_tile(thing.x, thing.y)
                    tbg = tt.bg or m.floor_color

                    tcod.console_put_char_ex(self.map_con, thing.x, thing.y,
                                             thing.glyph, thing.color, tbg)
            m.clean(wx, wy)

        self.center_on_point(self.map_con, cx, cy, MainScreen.MAP_VIEW_W,
                             MainScreen.MAP_VIEW_H, 0, 0)

    def render_msg(self):
        self.msg_con.clear()
        Screen.border(self.msg_con, 'Messages')
        self.blit(self.msg_con, 0, 30)

    def render_skill(self):
        self.skill_con.clear()
        Screen.border(self.skill_con, 'Skills')
        self.blit(self.skill_con, 40, 30)

    def render_info(self):
        self.info_con.clear()
        Screen.border(self.info_con, 'Info')
        self.blit(self.info_con, 60, 30)

    def render_stat(self):
        self.stat_con.clear()
        Screen.border(self.stat_con, 'Stats')
        self.blit(self.stat_con, 60, 0)

    def handle_keys(self, key: tcod.Key) -> commands.Command:
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
            return commands.MoveByCommand(*dirMoves)
        elif key.vk == tcod.KEY_ESCAPE:
            return commands.ExitCommand()
        else:
            return commands.WaitCommand()
