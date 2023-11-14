from pico2d import *
WIDTH, HEIGHT = 1280, 1024
open_canvas(WIDTH, HEIGHT)

# Character = load_image("Barnard Gray.png")
# Background = load_image("GROUND.png")
arrow = load_image("./object/Arrow.png")
running = True
frame = 0
move = 0
radian = 0
angle = 0.0
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
    frame = (frame + 1) % 4
    move += 10
    #radian += 1
    r = 3
    radian += r
    print(radian)
    angle = float(radian) * 2 * 3.14 / 180
    arrow.clip_composite_draw(0, 0, 300, 160, angle, ' ', 540, 540, 300, 160)
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
