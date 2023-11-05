from pico2d import load_image
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT

import game_framework

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

PIXEL_PER_METER = (20.0 / 0.6)      # 10 pixel 당 30cm   100 pixel에 3m
RUN_SPEED_KMPH = 20.0       # 시속
RUN_SPEED_MPH = RUN_SPEED_KMPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPH / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER
# Bird Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4


class Idle:

    @staticmethod
    def enter(character, e):
        character.dir_x = 0
        character.frame = 0
        pass

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        pass

    @staticmethod
    def draw(character):
        character.image.clip_composite_draw(int(character.frame) * 250, 420, 250, 330, 0, 'h', character.x, character.y, 100, 150)
class Run:

    @staticmethod
    def enter(character, e):
        character.dir_x = 0
        character.frame = 0
        pass

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        character.frame = (character.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

    @staticmethod
    def draw(character):
        character.image.clip_composite_draw(int(character.frame) * 250, 420, 250, 330, 0, 'h', character.x, character.y, 100, 150)
class StateMachine:
    def __init__(self, character):
        self.character = character
        self.cur_state = Idle
        self.transitions = {

        }
    def start(self):
        self.cur_state.enter(self.character, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.character)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.character, e)
                self.cur_state = next_state
                self.cur_state.enter(self.character, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.character)



class Sands:

    def __init__(self):
        self.x, self.y = 400, 400
        self.frame = 0
        self.dir_x = 0
        self.dir_y = 0
        self.face_dir = 1  # 오른쪽 방향 얼굴을 향하고 있음
        self.image = load_image('sands.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
