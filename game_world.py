# 게임 월드 모듈

# 게임 월드 표현
objects = [[] for _ in range(4)]         # 게임 월드는 리스트로 표현

# 게임 월드에 객체 담기
def add_object(o, depth = 0):
    objects[depth].append(o)      # 지정된 깊이의 레이어에 객체 추가


def add_objects(ol, depth = 0):
    objects[depth] += ol


# 게임 월드 객체들을 모두 다 업데이트
def update():
    for layer in objects:
        for o in layer:
            o.update()


# 게임 월드의 객체들을 몽땅 그리기
def render():
    for layer in objects:
        for o in layer:
            o.draw()

# 객체 삭제
def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)
            return
    raise ValueError('왜 존재하지도 않는 걸 지우라구????')


def clear():
    for layer in objects:
        layer.clear()