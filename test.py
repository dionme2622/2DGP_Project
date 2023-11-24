from pico2d import *
#WIDTH, HEIGHT = 1280, 1024

from tkinter import *

root = Tk()
WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()
open_canvas(WIDTH, HEIGHT)

character = load_image("./character/sands_blue.png")
# Background = load_image("GROUND.png")
arrow = load_image("./object/Arrow.png")
ball = load_image("./object/ball.png")
running = True
frame = 0
move = 0
radian = 0
angle = 0.0

arr = [1, 2, 3, 4, 5]
def handle_events():
    global running, mx, my, num, arrive
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False

# 주인공은 start[num]지점에서 end[num+1]까지 이동
# 주인공이 start지점에서 end지점까지 도달하면 start[num] = end[num+1]
# start.append(end[num])
# 주인공이 start 점에서 end 지점까지 도달하면 arrive += 1

def draw_character(x, y):
    global frame
    global move
    global radian
    global character
    global ball
    frame = (frame + 1) % 2
    move += 10
    action = 1
    radian += 1
    r = 3
    radian += r
    angle = float(radian) * 2 * 3.14 / 180
    arrow.clip_composite_draw(0, 0, 100, 100, angle, ' ', 540, 540, 100, 100)
    #블루 샌즈
    if action == 1:
        if frame == 0:
            character.clip_draw(frame * 29, action * 52, 29, 52 - 14, 250, 500, 100, 100)
        elif frame == 1:
            character.clip_draw(frame * 32, action * 52, 32, 52 - 14, 250, 500, 100, 100)
    else :character.clip_draw(frame * 29 ,action * 52, 29, 52 - 14, 250, 500, 100, 100)     # 피격 시

    ball.clip_draw(0, 0, 40, 40, 200, 200)
    # 샌즈
    # Character.clip_draw(frame * 250, 420, 250, 330, x - 150 - move, y - 200, 100, 150)     # 이동 모션
    #
    # Character.clip_draw(frame * 250, 0, 250, 360, x - 150, y + 200, 100, 150)       # 피격 시
    #
    # if frame == 0:
    #     Character.clip_draw(0, 720, 250, 360, x, y, 100, 150)  # 공격 시
    # else:
    #     Character.clip_draw(250, 720, 300, 360, x, y, 100, 150)


    # 그레이
    # Character.clip_composite_draw(frame * 95, 3 * 130, 85, 120, 0, 'h',       # 이동 모션
    #                              400, 400, 100, 150)

    # Character.clip_composite_draw(frame * 85, 1 * 130, 85, 120, 0, 'h',       # 공격 모션
    #                              400, 400, 100, 150)
while running:
    clear_canvas()
#    Background.draw(WIDTH // 2, HEIGHT // 2)
    draw_character(540, 540)
    update_canvas()
    handle_events()
    delay(0.1)
    hide_cursor()

close_canvas()
