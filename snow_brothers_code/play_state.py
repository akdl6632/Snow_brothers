from pico2d import *
import game_framework
import logo_state
import title_state

MAP_WIDTH, MAP_HEIGHT = 256, 223
MAP_SIZE = 5

x = 0

class Map:
    def __init__(self):
        self.image = load_image('stage1.png')
        self.frame = 2250

    # 필드 내 모든적을 잡으면 y값을 증가 시켜서 다음 맵 출력
    def draw(self):
        self.image.clip_draw(1, 18, 256, 223, MAP_WIDTH * MAP_SIZE // 2, MAP_HEIGHT * MAP_SIZE // 2, MAP_WIDTH * MAP_SIZE, MAP_HEIGHT * MAP_SIZE)


class Nick:
    def __init__(self):
        self.x, self.y = 0, 100
        self.frame = 0
        self.dir, self.face_dir = 0, 1
        self.jump = 0
        self.attack = 0
        self.image = load_image('Nick.png')
        self.item = None


    def update(self):
        self.frame = (self.frame + 1) % 3
        self.x += self.dir * 1
        self.x = clamp(0, self.x, MAP_WIDTH * MAP_SIZE)
        # self.y += self.dir * 1

    def draw(self):
        if self.dir == -1:
            self.image.clip_draw(21 + (self.frame * 17), 236, 16, 26, self.x, self.y, 16 * 2.5, 26 * 2.5)  # 왼쪽 이동
        elif self.dir == 1:
            self.image.clip_draw(279 - (self.frame * 17), 236, 16, 26, self.x, self.y, 16 * 2.5, 26 * 2.5)  # 오른쪽 이동
        else:
            # self.image.clip_draw IDLE
            if self.face_dir == 1:
                self.image.clip_draw(299, 236, 16, 26, self.x, self.y, 16 * 2.5, 26 * 2.5)
            else:
                self.image.clip_draw(1, 236, 16, 26, self.x, self.y, 16 * 2.5, 26 * 2.5)

        # if self.jump == 1:
        #     self.image.clip_draw(75 + (self.frame * 17), 236, 46, 26, self.x, self.y, 16 * 2.5, 26 * 2.5)


def handle_events():
    # global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            match event.key:
                case pico2d.SDLK_ESCAPE:
                    game_framework.change_state(title_state)
                case pico2d.SDLK_LEFT:
                    nick.dir -= 1
                case pico2d.SDLK_RIGHT:
                    nick.dir += 1
                # case pico2d.SDLK_LALT:
                #     nick.jump == 1
                # case pico2d.SDLK_LCTRL:
                #     nick.attack = 1
        elif event.type == SDL_KEYUP:
            match event.key:
                case pico2d.SDLK_LEFT:
                    nick.dir += 1
                    nick.face_dir = -1
                case pico2d.SDLK_RIGHT:
                    nick.dir -= 1
                    nick.face_dir = 1
                # case pico2d.SDLK_LALT:
                #     nick.jump -= 1




nick = None
grass = None
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