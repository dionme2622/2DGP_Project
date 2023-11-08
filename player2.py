from pico2d import load_image

import game_framework
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_UP, SDLK_DOWN

from sands import FRAMES_PER_ACTION, ACTION_PER_TIME, RUN_SPEED_PPS


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


def lets_idle(e):
    return e[0] == 'LETS_IDLE'





class Idle:

    @staticmethod
    def enter(character, e):
        character.dir_x = 0
        character.frame = 0
        character.action = 1
        pass

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        pass

    @staticmethod
    def draw(character):
        character.image.clip_composite_draw(int(character.frame) * 250, character.action * 420, 250, 330, 0, 'h',
                                            character.x, character.y, 100, 150)


class Run:

    @staticmethod
    def enter(character, e):
        if right_down(e):
            character.dir_right = 1
            character.dirX, character.action = 1, 1
        elif left_down(e):
            character.dir_left = 1
            character.dirX, character.action = -1, 1
        elif up_down(e):
            character.dir_up = 1
            character.dirY, character.action = 1, 1
        elif down_down(e):
            character.dir_down = 1
            character.dirY, character.action = -1, 1

        elif right_up(e):
            character.dir_right = 0
            character.dirX = 0

            if character.dir_left == 1:
                character.dirX, character.action = -1, 1
            elif character.dir_up == 1:
                character.dirX, character.dirY, character.action = 0, 1, 1
            elif character.dir_down == 1:
                character.dirX, character.dirY, character.action = 0, -1, 1
        elif left_up(e):
            character.dir_left = 0
            character.dirX = 0
            if character.dir_right == 1:
                character.dirX, character.action = 1, 1
            elif character.dir_up == 1:
                character.dirX, character.dirY, character.action = 0, 1, 1
            elif character.dir_down == 1:
                character.dirX, character.dirY, character.action = 0, -1, 1
        elif up_up(e):
            character.dir_up = 0
            character.dirY = 0
            if character.dir_down == 1:
                character.dirY, character.action = -1, 1
            elif character.dir_right == 1:
                character.dirX, character.dirY, character.action = 1, 0, 1
            elif character.dir_left == 1:
                character.dirX, character.dirY, character.action = -1, 0, 1

        elif down_up(e):
            character.dir_down = 0
            character.dirY = 0
            if character.dir_up == 1:
                character.dirY, character.action = 1, 1
            elif character.dir_right == 1:
                character.dirX, character.dirY, character.action = 1, 0, 1
            elif character.dir_left == 1:
                character.dirX, character.dirY, character.action = -1, 0, 1

        if character.dir_left == 0 and character.dir_right == 0 and character.dir_up == 0 and character.dir_down == 0:
            character.state_machine.handle_event(('LETS_IDLE', 0))

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        character.frame = (character.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        if character.x >= 620: character.x = 620
        elif character.x <= 50: character.x = 50
        character.x += character.dirX * RUN_SPEED_PPS * game_framework.frame_time
        if character.y >= 800: character.y = 800
        elif character.y <= 80: character.y = 80
        character.y += character.dirY * RUN_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(character):
        character.image.clip_composite_draw(int(character.frame) * 250, character.action * 420, 250, 330, 0, 'h',
                                            character.x, character.y, 100, 150)


class StateMachine:
    def __init__(self, character):
        self.character = character
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, up_down: Run, up_up: Run,
                   down_down: Run, down_up: Run},
            Run: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, up_down: Run,
                  up_up: Run, down_down: Run, down_up: Run, lets_idle: Idle}
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

class Player2:
    def __init__(self, ch):
        self.x, self.y = 1200, 500
        self.hp, self.mp, self.speed, self.attack_speed = ch.hp, ch.mp, ch.speed, ch.attack_speed
        self.frame = ch.frame
        self.action = ch.action  # 오른쪽 IDLE
        self.dirX = ch.dirX
        self.dirY = ch.dirY
        self.face_dir = 1  # 오른쪽 방향 얼굴을 향하고 있음
        self.image = ch.image
        self.dir_left, self.dir_right, self.dir_up, self.dir_down = ch.dir_left, ch.dir_right, ch.dir_up, ch.dir_down
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()
    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()


# class Pinkbean:
#     def __init__(self):
#         self.x, self.y = 800, 500
#         self.frame = 0
#         self.action = 3  # 오른쪽 IDLE
#         self.dir_x = 0
#         self.dir_y = 0
#         self.face_dir = 1  # 오른쪽 방향 얼굴을 향하고 있음
#         self.image = load_image('sands.png')
#         self.state_machine = StateMachine(self)
#         self.state_machine.start()
#
#     def update(self):
#         self.state_machine.update()
#
#     def handle_event(self, event):
#         self.state_machine.handle_event(('INPUT', event))
#
#     def draw(self):
#         self.state_machine.draw()
#
# class Gray:
#     def __init__(self):
#         self.x, self.y = 800, 500
#         self.frame = 0
#         self.action = 3  # 오른쪽 IDLE
#         self.dir_x = 0
#         self.dir_y = 0
#         self.face_dir = 1  # 오른쪽 방향 얼굴을 향하고 있음
#         self.image = load_image('sands.png')
#         self.state_machine = StateMachine(self)
#         self.state_machine.start()
#
#     def update(self):
#         self.state_machine.update()
#
#     def handle_event(self, event):
#         self.state_machine.handle_event(('INPUT', event))
#
#     def draw(self):
#         self.state_machine.draw()