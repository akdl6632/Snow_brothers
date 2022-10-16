from pico2d import *

MAP_WIDTH, MAP_HEIGHT = 256, 223
MAP_SIZE = 5

class Map:
    def __init__(self):
        self.image = load_image('stage1.png')
        self.frame = 2250

    # 필드 내 모든적을 잡으면 y값을 증가 시켜서 다음 맵 출력
    def draw(self):
        self.image.clip_draw(1, 18, 256, 223, MAP_WIDTH * MAP_SIZE // 2, MAP_HEIGHT * MAP_SIZE // 2, MAP_WIDTH * MAP_SIZE, MAP_HEIGHT * MAP_SIZE)


class Nick:
    def __init__(self):
        self.x,self.y = 0, 100
        self.frame = 0
        self.image = load_image('Nick.png')


    def update(self):
        self.frame = (self.frame + 1) % 3
        self.x += 1


    def draw(self):
        self.image.clip_draw(21 + (self.frame * 17), 236, 15, 25, self.x, self.y, 15 * 2.5, 25 * 2.5)


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


nick = None
map = None
running = True

def enter():
    global nick, map, running
    nick = Nick()
    map = Map()
    running = True

def exit():
    global nick, map
    del nick
    del map

def update():
    nick.update()

def draw():
    clear_canvas()
    map.draw()
    nick.draw()
    update_canvas()


open_canvas(MAP_WIDTH * MAP_SIZE, MAP_HEIGHT * MAP_SIZE)

enter()
# game main loop code
while running:
    handle_events()
    update()
    draw()
    delay(0.1)
exit()

# finalization code
close_canvas()
