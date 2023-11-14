from pico2d import load_image, draw_rectangle, get_time, load_font

import game_framework
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_UP, SDLK_DOWN, SDLK_PERIOD, SDLK_COMMA, SDLK_SLASH

from tkinter import *

root = Tk()
WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()
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
        ch.dir_x = 0
        ch.frame = 0
        if ch.job == 'sands':
            ch.action = 1
        elif ch.job == 'gray':
            ch.action = 4

        if def_down(e):
            if get_time() - ch.wait_time > 5.0:   # get_time() - ch.time() > 5
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if skill_down(e):
            if ch.mp == 3:
                print("skill")
                ch.state_machine.handle_event(('LETS_SKILL', 0))
                ch.mp = 0
    @staticmethod
    def exit(ch, e):
        if atk_down(e):
            ch.shoot_ball()

    @staticmethod
    def do(ch):
        pass

    @staticmethod
    def draw(ch):
        if ch.job == 'sands':
            ch.image.clip_draw(int(ch.frame) * 250, ch.action * 420, 250, 330,
                                            ch.x, ch.y, 100, 150)
        elif ch.job == 'gray':
            ch.image.clip_draw(int(ch.frame) * 95, ch.action * 130, 85, 120, ch.x, ch.y, 100, 150)

class Run:

    @staticmethod
    def enter(ch, e):
        ch.frame = 0
        if ch.job == 'sands':
            ch.action = 1
        elif ch.job == 'gray':
            ch.action = 3

        if right_down(e):
            ch.dir_right = 1
            ch.dirX = 1
        elif left_down(e):
            ch.dir_left = 1
            ch.dirX = -1
        elif up_down(e):
            ch.dir_up = 1
            ch.dirY = 1
        elif down_down(e):
            ch.dir_down = 1
            ch.dirY = -1

        elif right_up(e):
            ch.dir_right = 0
            ch.dirX = 0

            if ch.dir_left == 1:
                ch.dirX = -1
            elif ch.dir_up == 1:
                ch.dirX, ch.dirY = 0, 1
            elif ch.dir_down == 1:
                ch.dirX, ch.dirY = 0, -1
        elif left_up(e):
            ch.dir_left = 0
            ch.dirX = 0
            if ch.dir_right == 1:
                ch.dirX = 1
            elif ch.dir_up == 1:
                ch.dirX, ch.dirY = 0, 1
            elif ch.dir_down == 1:
                ch.dirX, ch.dirY = 0, -1
        elif up_up(e):
            ch.dir_up = 0
            ch.dirY = 0
            if ch.dir_down == 1:
                ch.dirY = -1
            elif ch.dir_right == 1:
                ch.dirX, ch.dirY = 1, 0
            elif ch.dir_left == 1:
                ch.dirX, ch.dirY = -1, 0

        elif down_up(e):
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

        if skill_down(e):
            if ch.mp == 3:
                print("skill")
                ch.state_machine.handle_event(('LETS_SKILL', 0))
                ch.mp = 0
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

        if ch.x <= WIDTH // 2 + 40: ch.x = WIDTH // 2 + 40
        elif ch.x >= WIDTH - 230: ch.x = WIDTH - 230
        ch.x += ch.dirX * ch.RUN_SPEED_PPS * game_framework.frame_time
        if ch.y >= 800 - 20:
            ch.y = 800 - 20
        elif ch.y <= 100 - 20:
            ch.y = 100 - 20
        ch.y += ch.dirY * ch.RUN_SPEED_PPS * game_framework.frame_time
    @staticmethod
    def draw(ch):
        if ch.job == 'sands':
            ch.image.clip_draw(int(ch.frame) * 250, ch.action * 420, 250, 330,
                               ch.x, ch.y, 100, 150)
        elif ch.job == "gray":
            ch.image.clip_draw(int(ch.frame) * 95, ch.action * 130, 85, 120, ch.x, ch.y, 100, 150)

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
            ch.image.clip_draw(int(ch.frame) * 250, 720, 250, 360,
                                                ch.x, ch.y, 100, 150)
        elif ch.job == 'gray':
            ch.image.clip_draw(int(ch.frame) * 85, ch.action * 130, 85, 120,
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
            ch.image.clip_draw(int(ch.frame) * 250, 720, 250, 360,
                                                ch.x, ch.y, 100, 150)
        elif ch.job == 'gray':
            ch.image.clip_draw(int(ch.frame) * 85, ch.action * 130, 85, 120,
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
            ch.image.clip_draw(int(ch.frame), 50, 250, 360, ch.x, ch.y, 100, 150)
        elif ch.job == "gray":
            ch.image.clip_draw(int(ch.frame) * 85, 270, 85, 110, ch.x, ch.y, 100, 150)


class Skill:

    @staticmethod
    def enter(ch, e):
        pass

    @staticmethod
    def exit(ch, e):
        pass

    @staticmethod
    def do(ch):
        pass

    @staticmethod
    def draw(ch):
        pass

class StateMachine:
    def __init__(self, ch):
        self.ch = ch
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, up_down: Run, up_up: Run,
                   down_down: Run, down_up: Run, atk_down: Attack, def_down: Idle, skill_down: Idle, lets_defense: Defense, lets_skill: Skill},
            Run: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, up_down: Run,
                  up_up: Run, down_down: Run, down_up: Run, lets_idle: Idle, atk_down: Attack, def_down: Idle, skill_down: Idle,
                  lets_defense: Defense, lets_skill: Skill},
            Attack: {lets_idle: Idle},
            Defense: {lets_idle: Idle},
            Damage: {lets_idle: Idle},
            Skill: {lets_idle: Idle}
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

class Player2:
    def __init__(self, ch):
        self.x, self.y = WIDTH - 250, 500
        self.hp, self.mp, self.speed, self.attack_speed = ch.hp, ch.mp, ch.speed, ch.attack_speed
        self.frame = ch.frame
        self.action = ch.action  # 오른쪽 IDLE
        self.dirX = ch.dirX
        self.dirY = ch.dirY
        self.image = ch.image
        self.job = ch.job
        self.font = load_font('./object/ENCR10B.TTF', 30)
        self.wait_time = -5.0
        self.getball = False
        self.FRAMES_PER_ACTION = ch.FRAMES_PER_ACTION
        self.ACTION_PER_TIME = ch.ACTION_PER_TIME
        self.RUN_SPEED_PPS = ch.RUN_SPEED_PPS
        self.dir_left, self.dir_right, self.dir_up, self.dir_down = ch.dir_left, ch.dir_right, ch.dir_up, ch.dir_down
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def shoot_ball(self):
        if self.getball == True:
            print("player2 공 발사")
            self.getball = False

    def get_bb(self):
        if self.job == 'sands':
            return self.x - 30, self.y - 60, self.x + 50, self.y + 50
        elif self.job == 'gray':
            return self.x - 50, self.y - 60, self.x + 30, self.y + 50
        else:
            return

    def update(self):
        self.state_machine.update()
    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())
        if float(self.wait_time) - float(get_time()) > -5.0:
            self.font.draw(WIDTH // 2 + 100, HEIGHT // 2 + 300, f'{float(self.wait_time) + 5 - float(get_time()):.1f}', (0, 0, 0))
        else:
            self.font.draw(WIDTH // 2 + 100, HEIGHT // 2 + 300, f'ON', (0, 0, 0))
        self.font.draw(WIDTH // 2 + 400, HEIGHT // 2 + 300, f'HP:{self.hp}', (0, 0, 0))
        self.font.draw(WIDTH // 2 + 500, HEIGHT // 2 + 300, f'MP:{self.mp}', (0, 0, 0))
    def handle_collision(self, group, other):
        if group == 'player2:ball':
            # 공이 player2 에게 넘어감
            self.getball = True
            # 만약 Defense 상태가 아니라면
            if self.state_machine.cur_state != Defense:
                # player2 쳬력 1칸 감소
                self.hp -= 1
                # 피격 animation 출력.
                self.state_machine.cur_state = Damage
            if self.hp == 0:
                print("player1 사망")
            # player2 스킬 게이지 1칸 증가
            if self.mp < 3:
                self.mp += 1