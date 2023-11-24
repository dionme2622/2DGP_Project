from pico2d import load_image, get_time, load_font, clamp, draw_rectangle
import game_framework
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_UP, SDLK_DOWN, SDLK_PERIOD, SDLK_COMMA, SDLK_SLASH, \
    SDLK_SEMICOLON, SDLK_QUOTE

from tkinter import *

import game_world
import play_mode
from ball import Ball

root = Tk()
WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 당 30cm   100 pixel에 3m
RUN_SPEED_KMPH = 45.0  # 시속
RUN_SPEED_MPH = RUN_SPEED_KMPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPH / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4


def Semi_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SEMICOLON


def Quote_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_QUOTE


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP


def up_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP


def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN


def down_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN


def atk_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_COMMA


def def_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_PERIOD


def skill_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SLASH


def lets_idle(e):
    return e[0] == 'LETS_IDLE'


def lets_defense(e):
    return e[0] == 'LETS_DEFENSE'


def lets_skill(e):
    return e[0] == 'LETS_SKILL'


class Idle:

    @staticmethod
    def enter(ch, e):
        ch.frame = 0
        if def_down(e):
            if get_time() - ch.wait_time > 5.0:  # get_time() - ch.time() > 5
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if Semi_down(e):
            ch.angle += 5
        if Quote_down(e):
            ch.angle -= 5
        if ch.action == 2:
            ch.angle += 45
        elif ch.action == 3:
            ch.angle += 0
        elif ch.action == 4:
            ch.angle += 90
        elif ch.action == 5:
            ch.angle += 135

    @staticmethod
    def exit(ch, e):
        if atk_down(e):
            ch.shoot_ball()
        if ch.action == 2:
            ch.angle -= 45
        elif ch.action == 3:
            ch.angle -= 0
        elif ch.action == 4:
            ch.angle -= 90
        elif ch.action == 5:
            ch.angle -= 135
        pass

    @staticmethod
    def do(ch):
        pass

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class RunRight:
    @staticmethod
    def enter(ch, e):
        ch.action = 3
        if def_down(e):
            if get_time() - ch.wait_time > 2.0:  # get_time() - ch.time() > 5
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if Semi_down(e):
            ch.angle += 5
        if Quote_down(e):
            ch.angle -= 5

    @staticmethod
    def exit(ch, e):
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.x += RUN_SPEED_PPS * game_framework.frame_time
        if ch.state == 'alive':
            ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 270)
            ch.y = clamp(180, ch.y, 700)
        pass

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class RunRightUp:
    @staticmethod
    def enter(ch, e):
        ch.action = 3
        if def_down(e):
            if get_time() - ch.wait_time > 2.0:  # get_time() - ch.time() > 5
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if Semi_down(e):
            ch.angle += 5
        if Quote_down(e):
            ch.angle -= 5
        pass

    @staticmethod
    def exit(ch, e):
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.x += RUN_SPEED_PPS * game_framework.frame_time
        ch.y += RUN_SPEED_PPS * game_framework.frame_time
        if ch.state == 'alive':
            ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 270)
            ch.y = clamp(180, ch.y, 700)
        pass

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class RunRightDown:
    @staticmethod
    def enter(ch, e):
        ch.action = 3
        if def_down(e):
            if get_time() - ch.wait_time > 2.0:  # get_time() - ch.time() > 5
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if Semi_down(e):
            ch.angle += 5
        if Quote_down(e):
            ch.angle -= 5
        pass

    @staticmethod
    def exit(ch, e):
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.x += RUN_SPEED_PPS * game_framework.frame_time
        ch.y -= RUN_SPEED_PPS * game_framework.frame_time
        if ch.state == 'alive':
            ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 270)
            ch.y = clamp(180, ch.y, 700)
        pass

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class RunLeft:
    @staticmethod
    def enter(ch, e):
        ch.action = 4
        ch.angle += 90
        if def_down(e):
            if get_time() - ch.wait_time > 2.0:  # get_time() - ch.time() > 5
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if Semi_down(e):
            ch.angle += 5
        if Quote_down(e):
            ch.angle -= 5
        pass

    @staticmethod
    def exit(ch, e):
        ch.angle -= 90
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.x -= RUN_SPEED_PPS * game_framework.frame_time
        if ch.state == 'alive':
            ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 270)
            ch.y = clamp(180, ch.y, 700)
        pass

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class RunLeftUp:
    @staticmethod
    def enter(ch, e):
        ch.action = 4
        ch.angle += 90
        if def_down(e):
            if get_time() - ch.wait_time > 2.0:  # get_time() - ch.time() > 5
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if Semi_down(e):
            ch.angle += 5
        if Quote_down(e):
            ch.angle -= 5
        pass

    @staticmethod
    def exit(ch, e):
        ch.angle -= 90
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.x -= RUN_SPEED_PPS * game_framework.frame_time
        ch.y += RUN_SPEED_PPS * game_framework.frame_time
        if ch.state == 'alive':
            ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 270)
            ch.y = clamp(180, ch.y, 700)

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class RunLeftDown:
    @staticmethod
    def enter(ch, e):
        ch.action = 4
        ch.angle += 90
        if def_down(e):
            if get_time() - ch.wait_time > 2.0:  # get_time() - ch.time() > 5
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if Semi_down(e):
            ch.angle += 5
        if Quote_down(e):
            ch.angle -= 5
        pass

    @staticmethod
    def exit(ch, e):
        ch.angle -= 90
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.x -= RUN_SPEED_PPS * game_framework.frame_time
        ch.y -= RUN_SPEED_PPS * game_framework.frame_time
        if ch.state == 'alive':
            ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 270)
            ch.y = clamp(180, ch.y, 700)

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class RunUp:
    @staticmethod
    def enter(ch, e):
        ch.action = 2
        ch.angle += 45
        if def_down(e):
            if get_time() - ch.wait_time > 2.0:  # get_time() - ch.time() > 5
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if Semi_down(e):
            ch.angle += 5
        if Quote_down(e):
            ch.angle -= 5

    @staticmethod
    def exit(ch, e):
        ch.angle -= 45
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.y += RUN_SPEED_PPS * game_framework.frame_time
        if ch.state == 'alive':
            ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 270)
            ch.y = clamp(180, ch.y, 700)

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class RunDown:
    @staticmethod
    def enter(ch, e):
        ch.action = 5
        ch.angle += 135
        if def_down(e):
            if get_time() - ch.wait_time > 2.0:  # get_time() - ch.time() > 5
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if Semi_down(e):
            ch.angle += 5
        if Quote_down(e):
            ch.angle -= 5
        pass

    @staticmethod
    def exit(ch, e):
        ch.angle -= 135
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.y -= RUN_SPEED_PPS * game_framework.frame_time
        if ch.state == 'alive':
            ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 270)
            ch.y = clamp(180, ch.y, 700)

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class Attack:

    @staticmethod
    def enter(ch, e):
        ch.action = 1
        ch.frame = 0

    @staticmethod
    def exit(ch, e):
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if ch.frame >= 2:
            ch.state_machine.handle_event(('LETS_IDLE', 0))

    @staticmethod
    def draw(ch):
        if ch.frame < 1:
            ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)
        elif ch.frame >= 1:
            ch.image.clip_draw(int(ch.frame) * 32, ch.action * 52, 32, 52 - 14, ch.x, ch.y, 100, 100)


class Defense:
    @staticmethod
    def enter(ch, e):
        ch.action = 1
        ch.frame = 0

    @staticmethod
    def exit(ch, e):
        ch.wait_time = get_time()

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if ch.frame >= 2:
            ch.state_machine.handle_event(('LETS_IDLE', 0))

    @staticmethod
    def draw(ch):
        if ch.frame < 1:
            ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)
        elif ch.frame >= 1:
            ch.image.clip_draw(int(ch.frame) * 32, ch.action * 52, 32, 52 - 14, ch.x, ch.y, 100, 100)


class Damage:

    @staticmethod
    def enter(ch, e):
        ch.action = 0
        ch.frame = 0

    @staticmethod
    def exit(ch, e):
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if ch.frame >= 2:
            ch.state_machine.handle_event(('LETS_IDLE', 0))

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class StateMachine:
    def __init__(self, ch):
        self.ch = ch
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: RunRight, left_down: RunLeft, left_up: RunRight, right_up: RunLeft, up_down: RunUp,
                   down_down: RunDown, up_up: RunDown, down_up: RunUp, atk_down: Attack, def_down: Idle,
                   Semi_down: Idle,
                   Quote_down: Idle, lets_defense: Defense},
            RunRight: {right_up: Idle, left_down: Idle, up_down: RunRightUp, up_up: RunRightDown,
                       down_down: RunRightDown, down_up: RunRightUp, atk_down: Attack, def_down: RunRight,
                       Semi_down: RunRight,
                       Quote_down: RunRight, lets_defense: Defense},
            RunRightUp: {up_up: RunRight, right_up: RunUp, left_down: RunUp, down_down: RunRight, atk_down: Attack,
                         def_down: RunRightUp, Semi_down: RunRightUp, Quote_down: RunRightUp, lets_defense: Defense},
            RunUp: {up_up: Idle, left_down: RunLeftUp, down_down: Idle, right_down: RunRightUp,
                    left_up: RunRightUp, right_up: RunLeftUp, atk_down: Attack, def_down: RunUp, Semi_down: RunUp,
                    Quote_down: RunUp,
                    lets_defense: Defense},
            RunLeftUp: {right_down: RunUp, down_down: RunLeft, left_up: RunUp, up_up: RunLeft,
                        atk_down: Attack, def_down: RunLeftUp, Semi_down: RunLeftUp, Quote_down: RunLeftUp,
                        lets_defense: Defense},
            RunLeft: {left_up: Idle, up_down: RunLeftUp, right_down: Idle, down_down: RunLeftDown,
                      up_up: RunLeftDown, down_up: RunLeftUp, atk_down: Attack, def_down: RunLeft, Semi_down: RunLeft,
                      Quote_down: RunLeft, lets_defense: Defense},
            RunLeftDown: {left_up: RunDown, down_up: RunLeft, up_down: RunLeft, right_down: RunDown,
                          atk_down: Attack, def_down: RunLeftDown, Semi_down: RunLeftDown, Quote_down: RunLeftDown,
                          lets_defense: Defense},
            RunDown: {down_up: Idle, left_down: RunLeftDown, up_down: Idle, right_down: RunRightDown,
                      left_up: RunRightDown, right_up: RunLeftDown,
                      atk_down: Attack, def_down: RunDown, Semi_down: RunDown, Quote_down: RunDown,
                      lets_defense: Defense},
            RunRightDown: {right_up: RunDown, down_up: RunRight, left_down: RunDown, up_down: RunRight,
                           atk_down: Attack, def_down: RunRightDown, Semi_down: RunRightDown, Quote_down: RunRightDown,
                           lets_defense: Defense},
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


class Redteam:
    image = None

    def __init__(self, x, y, num):
        if Redteam.image == None:
            Redteam.image = load_image("./character/sands_red.png")
        self.x, self.y, self.num = x, y, num
        self.frame, self.action = 0, 0
        self.state = 'alive'
        self.angle = 0
        self.getball = False
        self.shoot = False
        self.wait_time = -2.0
        self.font = load_font('./object/ENCR10B.TTF', 30)
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def shoot_ball(self):
        if self.getball == True:
            self.getball = False
            play_mode.ball.shoot = True

    def get_bb(self):
        return self.x - 40, self.y - 50, self.x + 50, self.y + 50

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x, self.y + 70, f'{self.num}', (255, 255, 255))
        draw_rectangle(*self.get_bb())
        if float(self.wait_time) - float(get_time()) > -5.0:
            self.font.draw(WIDTH // 2 + 100, HEIGHT // 2 + 300, f'{float(self.wait_time) + 5 - float(get_time()):.1f}',
                           (0, 0, 0))
        else:
            self.font.draw(WIDTH // 2 + 100, HEIGHT // 2 + 300, f'ON', (0, 0, 0))

    def handle_collision(self, group, other):
        if group == 'Redteam:ball':
            if play_mode.ball.state == 'floor':  # 공이 바닥에 놓여있다면
                print("레드팀 공 주움")
                self.getball = True
                play_mode.ball.state = 'Redteam_get'
            elif play_mode.ball.state == 'Blueteam_get' and play_mode.ball.shoot == True:  # 공을 블루팀이 들고있었다면
                if self.state == 'alive':
                    self.state_machine.cur_state = Damage
                    play_mode.ball.x, play_mode.ball.y = self.x, self.y  # 맞은 플레이어 앞에 떨어진다
                    play_mode.ball.state = 'floor'
                    self.x, self.y, self.state = 200, 400, 'dead'
            elif play_mode.ball.state == 'Redteam_get' and play_mode.ball.shoot == True:  # 공을 같은 팀이 들고있었다면
                self.getball = True
                play_mode.ball.shoot = False
        pass
