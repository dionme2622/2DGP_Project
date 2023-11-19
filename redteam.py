from pico2d import load_image, draw_rectangle, get_time, load_font, clamp

import game_framework
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_UP, SDLK_DOWN, SDLK_PERIOD, SDLK_COMMA, SDLK_SLASH, \
    SDLK_SEMICOLON, SDLK_QUOTE

from tkinter import *

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
            if get_time() - ch.wait_time > 5.0:   # get_time() - ch.time() > 5
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if Semi_down(e):
            ch.angle += 5
        if Quote_down(e):
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
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class RunRight:
    @staticmethod
    def enter(ch, e):
        ch.action = 3
        pass

    @staticmethod
    def exit(ch, e):
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.x += RUN_SPEED_PPS * game_framework.frame_time
        ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 270)
        ch.y = clamp(180, ch.y, 700)
        pass

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29 ,ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class RunRightUp:
    @staticmethod
    def enter(ch, e):
        ch.action = 3
        pass

    @staticmethod
    def exit(ch, e):
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.x += RUN_SPEED_PPS * game_framework.frame_time
        ch.y += RUN_SPEED_PPS * game_framework.frame_time
        ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 270)
        ch.y = clamp(180, ch.y, 700)
        pass

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29 ,ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)

class RunRightDown:
    @staticmethod
    def enter(ch, e):
        ch.action = 3
        pass

    @staticmethod
    def exit(ch, e):
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.x += RUN_SPEED_PPS * game_framework.frame_time
        ch.y -= RUN_SPEED_PPS * game_framework.frame_time
        ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 270)
        ch.y = clamp(180, ch.y, 700)
        pass

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29 ,ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)




class RunLeft:
    @staticmethod
    def enter(ch, e):
        ch.action = 4
        pass

    @staticmethod
    def exit(ch, e):
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.x -= RUN_SPEED_PPS * game_framework.frame_time
        ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 270)
        ch.y = clamp(180, ch.y, 700)
        pass

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29 ,ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class RunLeftUp:
    @staticmethod
    def enter(ch, e):
        ch.action = 4
        pass

    @staticmethod
    def exit(ch, e):
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.x -= RUN_SPEED_PPS * game_framework.frame_time
        ch.y += RUN_SPEED_PPS * game_framework.frame_time
        ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 270)
        ch.y = clamp(180, ch.y, 700)

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29 ,ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class RunLeftDown:
    @staticmethod
    def enter(ch, e):
        ch.action = 4
        pass

    @staticmethod
    def exit(ch, e):
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.x -= RUN_SPEED_PPS * game_framework.frame_time
        ch.y -= RUN_SPEED_PPS * game_framework.frame_time
        ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 270)
        ch.y = clamp(180, ch.y, 700)

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29 ,ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)




class RunUp:
    @staticmethod
    def enter(ch, e):
        ch.action = 2


    @staticmethod
    def exit(ch, e):
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.y += RUN_SPEED_PPS * game_framework.frame_time
        ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 270)
        ch.y = clamp(180, ch.y, 700)

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29 ,ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class RunDown:
    @staticmethod
    def enter(ch, e):
        ch.action = 5
        pass

    @staticmethod
    def exit(ch, e):
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.y -= RUN_SPEED_PPS * game_framework.frame_time
        ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 270)
        ch.y = clamp(180, ch.y, 700)

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29 ,ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)

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




class StateMachine:
    def __init__(self, ch):
        self.ch = ch
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: RunRight, left_down: RunLeft, left_up: RunRight, right_up: RunLeft, up_down: RunUp,
                   down_down: RunDown, up_up: RunDown, down_up: RunUp},
            RunRight: {right_up: Idle, left_down: Idle, up_down: RunRightUp, up_up: RunRightDown,
                       down_down: RunRightDown, down_up: RunRightUp},
            RunRightUp: {up_up: RunRight, right_up: RunUp, left_down: RunUp, down_down: RunRight},
            RunUp: {up_up: Idle, left_down: RunLeftUp, down_down: Idle, right_down: RunRightUp,
                    left_up: RunRightUp, right_up: RunLeftUp},
            RunLeftUp: {right_down: RunUp, down_down: RunLeft, left_up: RunUp, up_up: RunLeft},
            RunLeft: {left_up: Idle, up_down: RunLeftUp, right_down: Idle, down_down: RunLeftDown,
                      up_up: RunLeftDown, down_up: RunLeftUp},
            RunLeftDown: {left_up: RunDown, down_up: RunLeft, up_down: RunLeft, right_down: RunDown},
            RunDown: {down_up: Idle, left_down: RunLeftDown, up_down: Idle, right_down: RunRightDown,
                      left_up: RunRightDown, right_up: RunLeftDown},
            RunRightDown: {right_up: RunDown, down_up: RunRight, left_down: RunDown, up_down: RunRight},
            Attack: {lets_idle: Idle},
            Defense: {lets_idle: Idle},
            Damage: {lets_idle: Idle}
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
    def __init__(self):
        if Redteam.image == None:
            Redteam.image = load_image("./character/sands_red.png")
        self.x, self.y = WIDTH - 300, 480
        self.frame, self.action = 0, 0
        self.angle = 0
        self.getball = True
        self.shoot = False
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
        #draw_rectangle(*self.get_bb())
        if float(self.wait_time) - float(get_time()) > -5.0:
            self.font.draw(WIDTH // 2 + 100, HEIGHT // 2 + 300, f'{float(self.wait_time) + 5 - float(get_time()):.1f}', (0, 0, 0))
        else:
            self.font.draw(WIDTH // 2 + 100, HEIGHT // 2 + 300, f'ON', (0, 0, 0))
    def handle_collision(self, group, other):
        if group == 'player2:ball':
            # 공이 player2 에게 넘어감
            #self.getball = True
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