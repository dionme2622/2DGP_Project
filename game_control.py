from pico2d import *
import game_world


# Game object class here


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False




def create_world():
    global running
    global background

    game_world.add_object(background, 0)
    running = True

# 게임 월드 객체들을 모두 다 업데이트
def update_world():
    game_world.update()


# 게임 월드의 객체들을 몽땅 그리기
def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()


open_canvas()
create_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
# finalization code
close_canvas()
