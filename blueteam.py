from pico2d import load_image, draw_rectangle, get_time, load_font

import game_framework
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_r, SDLK_d, SDLK_f, SDLK_g, SDLK_q, SDLK_w, SDLK_e, SDLK_a, SDLK_s
from tkinter import *

root = Tk()
WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 당 30cm   100 pixel에 3m
RUN_SPEED_KMPH = 15.0  # 시속
RUN_SPEED_MPH = RUN_SPEED_KMPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPH / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4


def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


def s_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s


def r_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_r


def r_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_r


def d_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d


def d_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d


def f_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_f


def f_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_f


def g_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_g


def g_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_g

def atk_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_q


def def_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_w


def lets_idle(e):
    return e[0] == 'LETS_IDLE'


def lets_defense(e):
    return e[0] == 'LETS_DEFENSE'




class Idle:

    @staticmethod
    def enter(ch, e):
        ch.dir_x = 0
        ch.frame = 0
        if ch.job == 'sands':
            ch.action = 1
        elif ch.job == 'gray':
            ch.action = 4
        if def_down(e):
            if get_time() - ch.wait_time > 5.0:   # get_time() - ch.time() > 5
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if a_down(e):
            ch.angle += 5
        if s_down(e):
            ch.angle -= 5
    @staticmethod
    def exit(ch, e):
        if atk_down(e):
            ch.shoot_ball()

        pass

    @staticmethod
    def do(ch):
        pass

    @staticmethod
    def draw(ch):
        if ch.job == 'sands':
            ch.image.clip_composite_draw(int(ch.frame) * 250, ch.action * 420, 250, 330, 0, 'h',
                                         ch.x, ch.y, 100, 150)
        elif ch.job == 'gray':
            ch.image.clip_composite_draw(int(ch.frame) * 95, ch.action * 130, 85, 120, 0, 'h',
                                         ch.x, ch.y, 100, 150)


class Run:

    @staticmethod
    def enter(ch, e):
        ch.frame = 0
        if ch.job == 'sands':
            ch.action = 1
        elif ch.job == 'gray':
            ch.action = 3

        if g_down(e):
            ch.dir_right = 1
            ch.dirX = 1
        elif d_down(e):
            ch.dir_left = 1
            ch.dirX = -1
        elif r_down(e):
            ch.dir_up = 1
            ch.dirY = 1
        elif f_down(e):
            ch.dir_down = 1
            ch.dirY = -1

        elif g_up(e):
            ch.dir_right = 0
            ch.dirX = 0

            if ch.dir_left == 1:
                ch.dirX = -1
            elif ch.dir_up == 1:
                ch.dirX, ch.dirY = 0, 1
            elif ch.dir_down == 1:
                ch.dirX, ch.dirY = 0, -1
        elif d_up(e):
            ch.dir_left = 0
            ch.dirX = 0
            if ch.dir_right == 1:
                ch.dirX = 1
            elif ch.dir_up == 1:
                ch.dirX, ch.dirY = 0, 1
            elif ch.dir_down == 1:
                ch.dirX, ch.dirY = 0, -1
        elif r_up(e):
            ch.dir_up = 0
            ch.dirY = 0
            if ch.dir_down == 1:
                ch.dirY = -1
            elif ch.dir_right == 1:
                ch.dirX, ch.dirY = 1, 0
            elif ch.dir_left == 1:
                ch.dirX, ch.dirY = -1, 0

        elif f_up(e):
            ch.dir_down = 0
            ch.dirY = 0
            if ch.dir_up == 1:
                ch.dirY = 1
            elif ch.dir_right == 1:
                ch.dirX, ch.dirY = 1, 0
            elif ch.dir_left == 1:
                ch.dirX, ch.dirY = -1, 0

        if ch.dir_left == 0 and ch.dir_right == 0 and ch.dir_up == 0 and ch.dir_down == 0:
            ch.state_machine.handle_event(('LETS_IDLE', 0))

        if def_down(e):
            if get_time() - ch.wait_time > 5.0:   # get_time() - ch.time() > 5
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))


        if a_down(e):
            ch.angle += 5
        if s_down(e):
            ch.angle -= 5
    @staticmethod
    def exit(ch, e):
        if atk_down(e):
            ch.shoot_ball()

    @staticmethod
    def do(ch):
        if ch.job == "sands":
            ch.frame = (ch.frame + ch.FRAMES_PER_ACTION * ch.ACTION_PER_TIME * game_framework.frame_time) % 4
        elif ch.job == "gray":
            ch.frame = (ch.frame + ch.FRAMES_PER_ACTION * ch.ACTION_PER_TIME * game_framework.frame_time) % 4
        if ch.x >= WIDTH // 2 - 20:
            ch.x = WIDTH // 2 - 20
        elif ch.x <= 0 + 230:
            ch.x = 0 + 230
        ch.x += ch.dirX * ch.RUN_SPEED_PPS * game_framework.frame_time
        if ch.y >= 800 - 20:
            ch.y = 800 - 20
        elif ch.y <= 100 - 20:
            ch.y = 100 - 20
        ch.y += ch.dirY * ch.RUN_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(ch):
        if ch.job == "sands":
            ch.image.clip_composite_draw(int(ch.frame) * 250, ch.action * 420, 250, 330, 0, 'h',
                                         ch.x, ch.y, 100, 150)
        elif ch.job == "gray":
            ch.image.clip_composite_draw(int(ch.frame) * 95, ch.action * 130, 85, 120, 0, 'h',
                                         ch.x, ch.y, 100, 150)


class Attack:

    @staticmethod
    def enter(ch, e):
        ch.dir_x = 0
        ch.frame = 0
        if ch.job == 'sands':
            ch.action = 2
        elif ch.job == 'gray':
            ch.action = 1

    @staticmethod
    def exit(ch, e):
        pass

    @staticmethod
    def do(ch):
        if ch.job == "sands":
            ch.frame = (ch.frame + ch.FRAMES_PER_ACTION * ch.ACTION_PER_TIME * game_framework.frame_time)
            if ch.frame >= 2:
                ch.state_machine.handle_event(('LETS_IDLE', 0))
        elif ch.job == "gray":
            ch.frame = (ch.frame + ch.FRAMES_PER_ACTION * ch.ACTION_PER_TIME * game_framework.frame_time)
            if ch.frame >= 4:
                ch.state_machine.handle_event(('LETS_IDLE', 0))

    @staticmethod
    def draw(ch):
        if ch.job == 'sands':
            ch.image.clip_composite_draw(int(ch.frame) * 250, 720, 250, 360, 0, 'h',
                                         ch.x, ch.y, 100, 150)
        elif ch.job == 'gray':
            ch.image.clip_composite_draw(int(ch.frame) * 85, ch.action * 130, 85, 120, 0, 'h',
                                         ch.x, ch.y, 100, 150)


class Defense:
    @staticmethod
    def enter(ch, e):
        ch.dir_x = 0
        ch.frame = 0
        if ch.job == 'sands':
            ch.action = 2
        elif ch.job == 'gray':
            ch.action = 1
        print("player1 defense!")

    @staticmethod
    def exit(ch, e):
        ch.wait_time = get_time()

    @staticmethod
    def do(ch):
        if ch.job == "sands":
            ch.frame = (ch.frame + ch.FRAMES_PER_ACTION * ch.ACTION_PER_TIME * game_framework.frame_time)
            if ch.frame >= 2:
                ch.state_machine.handle_event(('LETS_IDLE', 0))
        elif ch.job == "gray":
            ch.frame = (ch.frame + ch.FRAMES_PER_ACTION * ch.ACTION_PER_TIME * game_framework.frame_time)
            if ch.frame >= 2:
                ch.state_machine.handle_event(('LETS_IDLE', 0))

    @staticmethod
    def draw(ch):
        if ch.job == 'sands':
            ch.image.clip_composite_draw(int(ch.frame) * 250, 720, 250, 360, 0, 'h',
                                         ch.x, ch.y, 100, 150)
        elif ch.job == 'gray':
            ch.image.clip_composite_draw(int(ch.frame) * 85, 130, 85, 120, 0, 'h',
                                         ch.x, ch.y, 100, 150)

class Damage:

    @staticmethod
    def enter(ch, e):
        ch.dir_x = 0
        ch.frame = 0


    @staticmethod
    def exit(ch, e):
        pass

    @staticmethod
    def do(ch):
        if ch.job == "sands":
            ch.frame = (ch.frame + ch.FRAMES_PER_ACTION * ch.ACTION_PER_TIME * game_framework.frame_time)
            if ch.frame >= 2:
                ch.state_machine.handle_event(('LETS_IDLE', 0))
        elif ch.job == "gray":
            ch.frame = (ch.frame + ch.FRAMES_PER_ACTION * ch.ACTION_PER_TIME * game_framework.frame_time)
            if ch.frame >= 2:
                ch.state_machine.handle_event(('LETS_IDLE', 0))

    @staticmethod
    def draw(ch):
        if ch.job == "sands":
            ch.image.clip_composite_draw(int(ch.frame), 50, 250, 360, 0, 'h', ch.x, ch.y, 100, 150)
        elif ch.job == "gray":
            ch.image.clip_composite_draw(int(ch.frame) * 85, 270, 85, 110, 0, 'h',
                                         ch.x, ch.y, 100, 150)


class StateMachine:
    def __init__(self, ch):
        self.ch = ch
        self.cur_state = Idle
        self.transitions = {
            Idle: {g_down: Run, d_down: Run, g_up: Run, d_up: Run, r_down: Run, r_up: Run,
                   f_down: Run, f_up: Run, a_down: Idle, s_down: Idle, atk_down: Attack, def_down: Idle, skill_down: Idle, lets_defense: Defense},
            Run: {g_down: Run, d_down: Run, g_up: Run, d_up: Run, r_down: Run,
                  r_up: Run, f_down: Run, f_up: Run, a_down: Run, s_down: Run, lets_idle: Idle, atk_down: Attack, def_down: Idle, skill_down: Idle, lets_defense: Defense},
            Attack: {lets_idle: Idle},
            Defense: {lets_idle: Idle},
            Damage: {lets_idle: Idle},
        }

    def start(self):
        self.cur_state.enter(self.ch, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.ch)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.ch, e)
                self.cur_state = next_state
                self.cur_state.enter(self.ch, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.ch)


class Blueteam:
    image = None
    def __init__(self, ch):
        if Blueteam.image == None:
            Blueteam.image = load_image("./character/sands_blue.png")
        self.x, self.y = 250, 500
        self.frame, self.action = 0, 0
        self.dirX = ch.dirX
        self.dirY = ch.dirY
        self.angle = 0
        self.getball = True
        self.shoot = False
        self.dir_left, self.dir_right, self.dir_up, self.dir_down = ch.dir_left, ch.dir_right, ch.dir_up, ch.dir_down
        self.wait_time = -5.0
        self.font = load_font('./object/ENCR10B.TTF', 30)
        self.state_machine = StateMachine(self)
        self.state_machine.start()
    def shoot_ball(self):
        if self.getball == True:
            self.shoot = True
            #self.getball = False

    def get_bb(self):
        if self.job == 'sands':
            return self.x - 40, self.y - 60, self.x + 40, self.y + 50
        elif self.job == 'gray':
            return self.x - 30, self.y - 60, self.x + 50, self.y + 50
        else:
            return

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        if float(self.wait_time) - float(get_time()) > -5.0:
            self.font.draw(WIDTH // 2 - 100, HEIGHT // 2 + 300, f'{float(self.wait_time) + 5 - float(get_time()):.1f}', (0, 0, 0))
        else:
            self.font.draw(WIDTH // 2 - 100, HEIGHT // 2 + 300, f'ON', (0, 0, 0))
        #draw_rectangle(*self.get_bb())

    def handle_collision(self, group, other):
        # if group == 'player1:ball':
        #     # 공이 player1 에게 넘어감
        #     #self.getball = True
        #     # 만약 Defense 상태가 아니라면
        #     if self.state_machine.cur_state != Defense:
        #         # player1 쳬력 1칸 감소
        #         self.hp -= 1
        #         # 피격 animation 출력
        #         self.state_machine.cur_state = Damage
        #     if self.hp == 0:
        #         print("player1 사망")
        #     # player1 스킬 게이지 1칸 증가
        #     if self.mp < 3:
        #         self.mp += 1
        pass