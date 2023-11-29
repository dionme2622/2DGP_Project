import math
import random

from pico2d import load_image, get_time, load_font, clamp, draw_rectangle
import game_framework
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_UP, SDLK_DOWN, SDLK_PERIOD, SDLK_COMMA, SDLK_SLASH, \
    SDLK_SEMICOLON, SDLK_QUOTE

from tkinter import *

import game_world
import play_mode
import ball
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from function import *
from skill import Skill

root = Tk()
WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 당 30cm   100 pixel에 3m
RUN_SPEED_KMPH = 25.0  # 시속
RUN_SPEED_MPH = RUN_SPEED_KMPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPH / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

survivor = 5
def_cooltime = 4.0
skill_cool_time = 1.0
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

def return_run_state(ch):
    if ch.run_state == Idle:
        ch.state_machine.handle_event(('LETS_IDLE', 0))
    elif ch.run_state == RunRight:
        ch.state_machine.handle_event(('LETS_RIGHT', 0))
    elif ch.run_state == RunRightUp:
        ch.state_machine.handle_event(('LETS_RIGHT_UP', 0))
    elif ch.run_state == RunRightDown:
        ch.state_machine.handle_event(('LETS_RIGHT_DOWN', 0))
    elif ch.run_state == RunLeft:
        ch.state_machine.handle_event(('LETS_LEFT', 0))
    elif ch.run_state == RunLeftUp:
        ch.state_machine.handle_event(('LETS_LEFT_UP', 0))
    elif ch.run_state == RunLeftDown:
        ch.state_machine.handle_event(('LETS_LEFT_DOWN', 0))
    elif ch.run_state == RunUp:
        ch.state_machine.handle_event(('LETS_UP', 0))
    elif ch.run_state == RunDown:
        ch.state_machine.handle_event(('LETS_DOWN', 0))
PI = 3.141592
radian = 10
class Idle:

    @staticmethod
    def enter(ch, e):
        ch.frame = 0
        ch.run_state = Idle

        if def_down(e):
            if get_time() - ch.wait_time > def_cooltime:  # get_time() - ch.time() > 5
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if Semi_down(e):
            ch.angle -= radian
        if Quote_down(e):
            ch.angle += radian
        if ch.run == 2:
            ch.angle += 45
        elif ch.run == 3:
            ch.angle += 0
        elif ch.run == 4:
            ch.angle += 90
        elif ch.run == 5:
            ch.angle += 135
        print("Idle 입장")
        print(ch.angle)
    @staticmethod
    def exit(ch, e):
        if atk_down(e):
            ch.shoot_ball()
        if skill_down(e):
            if get_time() - Redteam.skill_wait_time > skill_cool_time:
                ch.use_skill()
        if ch.run == 2:
            ch.angle -= 45
        elif ch.run == 3:
            ch.angle -= 0
        elif ch.run == 4:
            ch.angle -= 90
        elif ch.run == 5:
            ch.angle -= 135
        print("Idle 해제")
        print(ch.angle)
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
        ch.action, ch.run = 3, 3
        ch.run_state = RunRight
        if def_down(e):
            if get_time() - ch.wait_time > def_cooltime:  # get_time() - ch.time() > 5
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if Semi_down(e):
            ch.angle -= radian
        if Quote_down(e):
            ch.angle += radian

    @staticmethod
    def exit(ch, e):
        if atk_down(e):
            ch.shoot_ball()
        if skill_down(e):
            if get_time() - Redteam.skill_wait_time > skill_cool_time:
                ch.use_skill()
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.x += RUN_SPEED_PPS * game_framework.frame_time
        if ch.state == 'alive':
            ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 270)
            ch.y = clamp(180, ch.y, 700)
        elif ch.state == 'dead':
            if ch.x > 180 and ch.x < 240 and ch.y >= 100 and ch.y <= 770:
                ch.x = clamp(200, ch.x, 220)
                ch.y = clamp(50, ch.y, 800)
            elif ch.x > 180 and ch.y >= 770:
                ch.x = clamp(200, ch.x, WIDTH // 2 - 20)
                ch.y = clamp(780, ch.y, 800)
            elif ch.x > 180 and ch.y <= 125:
                ch.x = clamp(200, ch.x, WIDTH // 2 - 20)
                ch.y = clamp(50, ch.y, 100)
            else:
                ch.x = clamp(200, ch.x, 220)
                ch.y = clamp(0, ch.y, 800)

        pass

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class RunRightUp:
    @staticmethod
    def enter(ch, e):
        ch.action, ch.run = 3, 3
        ch.run_state = RunRightUp
        if def_down(e):
            if get_time() - ch.wait_time > def_cooltime:  # get_time() - ch.time() > 5
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if Semi_down(e):
            ch.angle -= radian
        if Quote_down(e):
            ch.angle += radian
        pass

    @staticmethod
    def exit(ch, e):
        if atk_down(e):
            ch.shoot_ball()
        if skill_down(e):
            if get_time() - Redteam.skill_wait_time > skill_cool_time:
                ch.use_skill()
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.x += RUN_SPEED_PPS * game_framework.frame_time
        ch.y += RUN_SPEED_PPS * game_framework.frame_time
        if ch.state == 'alive':
            ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 270)
            ch.y = clamp(180, ch.y, 700)
        elif ch.state == 'dead':
            if ch.x > 180 and ch.x < 240 and ch.y >= 100 and ch.y <= 770:
                ch.x = clamp(200, ch.x, 220)
                ch.y = clamp(50, ch.y, 800)
            elif ch.x > 180 and ch.y >= 770:
                ch.x = clamp(200, ch.x, WIDTH // 2 - 20)
                ch.y = clamp(780, ch.y, 800)
            elif ch.x > 180 and ch.y <= 125:
                ch.x = clamp(200, ch.x, WIDTH // 2 - 20)
                ch.y = clamp(50, ch.y, 100)
            else:
                ch.x = clamp(200, ch.x, 220)
                ch.y = clamp(0, ch.y, 800)
        pass

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class RunRightDown:
    @staticmethod
    def enter(ch, e):
        ch.action, ch.run = 3, 3
        ch.run_state = RunRightDown
        if def_down(e):
            if get_time() - ch.wait_time > def_cooltime:  # get_time() - ch.time() > 5
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if Semi_down(e):
            ch.angle -= radian
        if Quote_down(e):
            ch.angle += radian
        pass

    @staticmethod
    def exit(ch, e):
        if atk_down(e):
            ch.shoot_ball()
        if skill_down(e):
            if get_time() - Redteam.skill_wait_time > skill_cool_time:
                ch.use_skill()
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.x += RUN_SPEED_PPS * game_framework.frame_time
        ch.y -= RUN_SPEED_PPS * game_framework.frame_time
        if ch.state == 'alive':
            ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 270)
            ch.y = clamp(180, ch.y, 700)
        elif ch.state == 'dead':
            if ch.x > 180 and ch.x < 240 and ch.y >= 100 and ch.y <= 770:
                ch.x = clamp(200, ch.x, 220)
                ch.y = clamp(50, ch.y, 800)
            elif ch.x > 180 and ch.y >= 770:
                ch.x = clamp(200, ch.x, WIDTH // 2 - 20)
                ch.y = clamp(780, ch.y, 800)
            elif ch.x > 180 and ch.y <= 125:
                ch.x = clamp(200, ch.x, WIDTH // 2 - 20)
                ch.y = clamp(50, ch.y, 100)
            else:
                ch.x = clamp(200, ch.x, 220)
                ch.y = clamp(0, ch.y, 800)
    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class RunLeft:
    @staticmethod
    def enter(ch, e):
        ch.action, ch.run = 4, 4
        ch.angle += 90
        print("Left enter")
        print(ch.angle)
        ch.run_state = RunLeft
        if def_down(e):
            if get_time() - ch.wait_time > def_cooltime:  # get_time() - ch.time() > 5
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if Semi_down(e):
            ch.angle -= radian
        if Quote_down(e):
            ch.angle += radian
        pass

    @staticmethod
    def exit(ch, e):
        ch.angle -= 90
        if atk_down(e):
            ch.shoot_ball()
        if skill_down(e):
            if get_time() - Redteam.skill_wait_time > skill_cool_time:
                ch.use_skill()
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.x -= RUN_SPEED_PPS * game_framework.frame_time
        if ch.state == 'alive':
            ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 270)
            ch.y = clamp(180, ch.y, 700)
        elif ch.state == 'dead':
            if ch.x > 180 and ch.x < 240 and ch.y >= 100 and ch.y <= 770:
                ch.x = clamp(200, ch.x, 220)
                ch.y = clamp(50, ch.y, 800)
            elif ch.x > 180 and ch.y >= 770:
                ch.x = clamp(200, ch.x, WIDTH // 2 - 20)
                ch.y = clamp(780, ch.y, 800)
            elif ch.x > 180 and ch.y <= 125:
                ch.x = clamp(200, ch.x, WIDTH // 2 - 20)
                ch.y = clamp(50, ch.y, 100)
            else:
                ch.x = clamp(200, ch.x, 220)
                ch.y = clamp(0, ch.y, 800)

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class RunLeftUp:
    @staticmethod
    def enter(ch, e):
        ch.action, ch.run = 4, 4
        ch.angle += 90
        ch.run_state = RunLeftUp
        if def_down(e):
            if get_time() - ch.wait_time > def_cooltime:  # get_time() - ch.time() > 5
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if Semi_down(e):
            ch.angle -= radian
        if Quote_down(e):
            ch.angle += radian
        pass

    @staticmethod
    def exit(ch, e):
        ch.angle -= 90
        if atk_down(e):
            ch.shoot_ball()
        if skill_down(e):
            if get_time() - Redteam.skill_wait_time > skill_cool_time:
                ch.use_skill()
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.x -= RUN_SPEED_PPS * game_framework.frame_time
        ch.y += RUN_SPEED_PPS * game_framework.frame_time
        if ch.state == 'alive':
            ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 270)
            ch.y = clamp(180, ch.y, 700)
        elif ch.state == 'dead':
            if ch.x > 180 and ch.x < 240 and ch.y >= 100 and ch.y <= 770:
                ch.x = clamp(200, ch.x, 220)
                ch.y = clamp(50, ch.y, 800)
            elif ch.x > 180 and ch.y >= 770:
                ch.x = clamp(200, ch.x, WIDTH // 2 - 20)
                ch.y = clamp(780, ch.y, 800)
            elif ch.x > 180 and ch.y <= 125:
                ch.x = clamp(200, ch.x, WIDTH // 2 - 20)
                ch.y = clamp(50, ch.y, 100)
            else:
                ch.x = clamp(200, ch.x, 220)
                ch.y = clamp(0, ch.y, 800)
    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class RunLeftDown:
    @staticmethod
    def enter(ch, e):
        ch.action, ch.run = 4, 4
        ch.angle += 90
        ch.run_state = RunLeftDown
        if def_down(e):
            if get_time() - ch.wait_time > def_cooltime:  # get_time() - ch.time() > 5
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if Semi_down(e):
            ch.angle -= radian
        if Quote_down(e):
            ch.angle += radian
        pass

    @staticmethod
    def exit(ch, e):
        ch.angle -= 90
        if atk_down(e):
            ch.shoot_ball()
        if skill_down(e):
            if get_time() - Redteam.skill_wait_time > skill_cool_time:
                ch.use_skill()
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.x -= RUN_SPEED_PPS * game_framework.frame_time
        ch.y -= RUN_SPEED_PPS * game_framework.frame_time
        if ch.state == 'alive':
            ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 270)
            ch.y = clamp(180, ch.y, 700)
        elif ch.state == 'dead':
            if ch.x > 180 and ch.x < 240 and ch.y >= 100 and ch.y <= 770:
                ch.x = clamp(200, ch.x, 220)
                ch.y = clamp(50, ch.y, 800)
            elif ch.x > 180 and ch.y >= 770:
                ch.x = clamp(200, ch.x, WIDTH // 2 - 20)
                ch.y = clamp(780, ch.y, 800)
            elif ch.x > 180 and ch.y <= 125:
                ch.x = clamp(200, ch.x, WIDTH // 2 - 20)
                ch.y = clamp(50, ch.y, 100)
            else:
                ch.x = clamp(200, ch.x, 220)
                ch.y = clamp(0, ch.y, 800)
    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class RunUp:
    @staticmethod
    def enter(ch, e):
        ch.action, ch.run = 2, 2
        ch.angle += 45
        ch.run_state = RunUp
        if def_down(e):
            if get_time() - ch.wait_time > def_cooltime:  # get_time() - ch.time() > 5
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if Semi_down(e):
            ch.angle -= radian
        if Quote_down(e):
            ch.angle += radian

    @staticmethod
    def exit(ch, e):
        ch.angle -= 45
        if atk_down(e):
            ch.shoot_ball()
        if skill_down(e):
            if get_time() - Redteam.skill_wait_time > skill_cool_time:
                ch.use_skill()
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.y += RUN_SPEED_PPS * game_framework.frame_time
        if ch.state == 'alive':
            ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 270)
            ch.y = clamp(180, ch.y, 700)
        elif ch.state == 'dead':
            if ch.x > 180 and ch.x < 240 and ch.y >= 100 and ch.y <= 770:
                ch.x = clamp(200, ch.x, 220)
                ch.y = clamp(50, ch.y, 800)
            elif ch.x > 180 and ch.y >= 770:
                ch.x = clamp(200, ch.x, WIDTH // 2 - 20)
                ch.y = clamp(780, ch.y, 800)
            elif ch.x > 180 and ch.y <= 125:
                ch.x = clamp(200, ch.x, WIDTH // 2 - 20)
                ch.y = clamp(50, ch.y, 100)
            else:
                ch.x = clamp(200, ch.x, 220)
                ch.y = clamp(0, ch.y, 800)
    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class RunDown:
    @staticmethod
    def enter(ch, e):
        ch.action, ch.run = 5, 5
        ch.angle += 135
        ch.run_state = RunDown
        if def_down(e):
            if get_time() - ch.wait_time > def_cooltime:  # get_time() - ch.time() > 5
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if Semi_down(e):
            ch.angle -= radian
        if Quote_down(e):
            ch.angle += radian
        pass

    @staticmethod
    def exit(ch, e):
        ch.angle -= 135
        if atk_down(e):
            ch.shoot_ball()
        if skill_down(e):
            if get_time() - Redteam.skill_wait_time > skill_cool_time:
                ch.use_skill()
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.y -= RUN_SPEED_PPS * game_framework.frame_time
        if ch.state == 'alive':
            ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 270)
            ch.y = clamp(180, ch.y, 700)
        elif ch.state == 'dead':
            if ch.x > 180 and ch.x < 240 and ch.y >= 100 and ch.y <= 780:
                ch.x = clamp(200, ch.x, 220)
                ch.y = clamp(50, ch.y, 800)
            elif ch.x > 180 and ch.y >= 770:
                ch.x = clamp(200, ch.x, WIDTH // 2 - 20)
                ch.y = clamp(780, ch.y, 800)
            elif ch.x > 180 and ch.y <= 125:
                ch.x = clamp(200, ch.x, WIDTH // 2 - 20)
                ch.y = clamp(50, ch.y, 100)
            else:
                ch.x = clamp(200, ch.x, 220)
                ch.y = clamp(0, ch.y, 800)

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
            return_run_state(ch)

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
        print("Defense 입장")
        print(ch.angle)

    @staticmethod
    def exit(ch, e):
        ch.wait_time = get_time()

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if ch.frame >= 2:
            return_run_state(ch)

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
            return_run_state(ch)

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
                   Quote_down: Idle, lets_defense: Defense, skill_down: Idle},
            RunRight: {right_up: Idle, left_down: Idle, up_down: RunRightUp, up_up: RunRightDown,
                       down_down: RunRightDown, down_up: RunRightUp, atk_down: Attack, def_down: RunRight,
                       Semi_down: RunRight,
                       Quote_down: RunRight, lets_defense: Defense, skill_down: RunRight},
            RunRightUp: {up_up: RunRight, right_up: RunUp, left_down: RunUp, down_down: RunRight, atk_down: Attack,
                         def_down: RunRightUp, Semi_down: RunRightUp, Quote_down: RunRightUp,
                         lets_defense: Defense, skill_down: RunRightUp},
            RunUp: {up_up: Idle, left_down: RunLeftUp, down_down: Idle, right_down: RunRightUp,
                    left_up: RunRightUp, right_up: RunLeftUp, atk_down: Attack, def_down: RunUp, Semi_down: RunUp,
                    Quote_down: RunUp, lets_defense: Defense, skill_down: RunUp},
            RunLeftUp: {right_down: RunUp, down_down: RunLeft, left_up: RunUp, up_up: RunLeft,
                        atk_down: Attack, def_down: RunLeftUp, Semi_down: RunLeftUp, Quote_down: RunLeftUp,
                        lets_defense: Defense, skill_down: RunLeftUp},
            RunLeft: {left_up: Idle, up_down: RunLeftUp, right_down: Idle, down_down: RunLeftDown,
                      up_up: RunLeftDown, down_up: RunLeftUp, atk_down: Attack, def_down: RunLeft, Semi_down: RunLeft,
                      Quote_down: RunLeft, lets_defense: Defense, skill_down: RunLeft},
            RunLeftDown: {left_up: RunDown, down_up: RunLeft, up_down: RunLeft, right_down: RunDown,
                          atk_down: Attack, def_down: RunLeftDown, Semi_down: RunLeftDown, Quote_down: RunLeftDown,
                          lets_defense: Defense, skill_down: RunLeftDown},
            RunDown: {down_up: Idle, left_down: RunLeftDown, up_down: Idle, right_down: RunRightDown,
                      left_up: RunRightDown, right_up: RunLeftDown,
                      atk_down: Attack, def_down: RunDown, Semi_down: RunDown, Quote_down: RunDown,
                      lets_defense: Defense, skill_down: RunDown},
            RunRightDown: {right_up: RunDown, down_up: RunRight, left_down: RunDown, up_down: RunRight,
                           atk_down: Attack, def_down: RunRightDown, Semi_down: RunRightDown, Quote_down: RunRightDown,
                           lets_defense: Defense, skill_down: RunRightDown},
            Attack: {lets_run_right: RunRight, lets_run_right_up: RunRightUp, lets_run_right_down: RunRightDown,
                     lets_run_left: RunLeft, lets_run_left_up: RunLeftUp, lets_run_left_down: RunLeftDown,
                     lets_run_up: RunUp, lets_run_down: RunDown, lets_idle: Idle
                     },
            Defense: {lets_run_right: RunRight, lets_run_right_up: RunRightUp, lets_run_right_down: RunRightDown,
                      lets_run_left: RunLeft, lets_run_left_up: RunLeftUp, lets_run_left_down: RunLeftDown,
                      lets_run_up: RunUp, lets_run_down: RunDown, lets_idle: Idle
                      },
            Damage: {lets_run_right: RunRight, lets_run_right_up: RunRightUp, lets_run_right_down: RunRightDown,
                     lets_run_left: RunLeft, lets_run_left_up: RunLeftUp, lets_run_left_down: RunLeftDown,
                     lets_run_up: RunUp, lets_run_down: RunDown, lets_idle: Idle
                     }
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
    skill_wait_time = -30.0
    def __init__(self, x, y, num):
        if Redteam.image == None:
            Redteam.image = load_image("./character/sands_red.png")
        self.x, self.y, self.num = x, y, num
        self.run = 0
        self.frame, self.action = 0, 0
        self.state = 'alive'
        self.run_state = Idle
        self.angle = 0
        self.getball = False
        self.shoot = False
        self.wait_time = -2.0
        self.font = load_font('./object/ENCR10B.TTF', 30)
        self.tx, self.ty = 0, 0
        self.dir = 0.0
        self.build_behavior_tree()
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def shoot_ball(self):
        if self.getball == True:
            self.getball = False
            play_mode.ball.shoot = True

    def use_skill(self):
        if self.getball == True:
            Redteam.skill_wait_time = get_time()
            skill = Skill(self.x, self.y, self.action)
            game_world.add_object(skill, 1)

    def get_bb(self):
        return self.x - 40, self.y - 50, self.x + 50, self.y + 50

    def update(self):
        self.state_machine.update()
        if play_mode.select[1] != self.num and self.getball != True:     # 선택되지 않았다면 AI가 조작한다
            self.bt.run()
            pass
    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x, self.y + 70, f'{self.num}', (255, 255, 255))
        draw_rectangle(*self.get_bb())
        if float(self.wait_time) - float(get_time()) > -30.0:
            self.font.draw(self.x, self.y + 120, f'{float(Redteam.skill_wait_time) + 30 - float(get_time()):.1f}', (255, 255, 255))
        else:
            self.font.draw(WIDTH // 2 + 100, HEIGHT // 2 + 300, f'ON', (0, 0, 0))

    def handle_collision(self, group, other):
        if group == 'Redteam:ball':
            # 공이 바닥에 놓여있다면
            if play_mode.ball.state == 'floor':
                ball_is_floor(self)
            # 공을 블루팀이 들고있었다면
            elif play_mode.ball.state == 'Blueteam_get' and play_mode.ball.shoot == True:
                ball_is_enemy(self)
            # 공을 같은 팀이 들고있었다면
            elif play_mode.ball.state == 'Redteam_get' and play_mode.ball.shoot == True:
                ball_is_team(self)
        pass
    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2


    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        self.speed = RUN_SPEED_PPS
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time

    def move_to(self, r=0.5):
        if math.cos(self.dir) < 0:
            self.action = 4
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        else:
            self.action = 3
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def set_random_location(self):
        self.tx, self.ty = random.randint(WIDTH // 2 + 70, WIDTH - 270), random.randint(180, 700)
        return BehaviorTree.SUCCESS

    def is_alive(self):
        if self.state == 'alive':
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def is_ball_nearby(self, distance):
        if self.distance_less_than(play_mode.boy.x, play_mode.boy.y, self.x, self.y, distance):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def move_to_boy(self, r=0.5):
        self.state = 'Walk'
        self.move_slightly_to(play_mode.boy.x, play_mode.boy.y)
        if self.distance_less_than(play_mode.boy.x, play_mode.boy.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING



    def flee(self):
        self.state = 'Walk'
        # 소년으로부터 멀어지는 방향
        self.dir = math.atan2(self.y - play_mode.boy.y, self.x - play_mode.boy.x)

        # 살짝 이동
        self.speed = RUN_SPEED_PPS
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time

        return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        a1 = Action("랜덤위치지정", self.set_random_location)
        a2 = Action("이동", self.move_to)
        root = SEQ_wander = Sequence("Wander", a1, a2)
        c1 = Condition("살아있는가?", self.is_alive)
        root = SEQ_wander = Sequence("살아있으면 배회", c1, SEQ_wander)

        self.bt = BehaviorTree(root)

def ball_is_team(ch):
    play_mode.ball.shoot = False
    ch.getball = True
    play_mode.ball.state = 'Redteam_get'
    pass

def ball_is_enemy(ch):
    global survivor
    if ch.state == 'alive':
        play_mode.ball.shoot = False
        if ch.state_machine.cur_state != Defense:   # 방어에 실패했다면
            play_mode.ball.x, play_mode.ball.y = ch.x - 80, ch.y  # 맞은 플레이어 앞에 떨어진다
            #ch.state_machine.cur_state = Damage
            ch.x, ch.y, ch.state = 200, 400, 'dead'
            survivor -= 1
            play_mode.ball.state = 'floor'
        else:                                       # 방어에 성공했다면
            play_mode.ball.x, play_mode.ball.y = ch.x - 80, ch.y
            play_mode.ball.state = 'floor'
    pass

def ball_is_floor(ch):
    ch.getball = True
    play_mode.ball.state = 'Redteam_get'
    pass
