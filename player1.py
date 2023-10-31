from pico2d import load_image

import sands
class Idle:

    @staticmethod
    def enter(character, e):
        character.action = 3
        character.dir_x = 0
        character.frame = 0
        pass

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        character.frame = (character.frame + 1) % 4

    @staticmethod
    def draw(character):
        character.image.clip_composite_draw(character.frame * 250, 420, 250, 330, 0, 'h', character.x, character.y, 100, 150)
        # move += 10
        # Character.clip_draw(frame * 250, 420, 250, 330, x - 150 - move, y - 200, 100, 150)  # 이동 모션
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
        self.x, self.y = 400, 500
        self.frame = 0
        self.action = 3  # 오른쪽 IDLE
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