from pico2d import *

import game_framework
import game_world
from attack import Attack

MAP_WIDTH, MAP_HEIGHT = 256, 223
MAP_SIZE = 5

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3



RD, LD, RU, LU, TIMER, ATTACK, AU, AD = range(8)
event_name = ['RD', 'LD', 'RU', 'LU', 'TIMER', 'ATTACK', 'AU', 'AD']

key_event_table = {
    (SDL_KEYDOWN, SDLK_LCTRL): ATTACK,
    (SDL_KEYDOWN, SDLK_LALT): AD,
    (SDL_KEYDOWN, SDLK_RIGHT): RD,
    (SDL_KEYDOWN, SDLK_LEFT): LD,
    (SDL_KEYUP, SDLK_RIGHT): RU,
    (SDL_KEYUP, SDLK_LEFT): LU,
    (SDL_KEYUP, SDLK_LALT): AU
}

class IDLE:
    @staticmethod
    def enter(self,event):
        print('ENTER IDLE')
        self.dir = 0
        self.timer = 100
        if event == AU:
            self.dir -= 1

    @staticmethod
    def exit(self, event):
        print('EXIT IDLE')
        if event == ATTACK:
            self.fire_snow()

    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        self.timer -= 1
        if self.timer == 0:
            self.add_event(TIMER)
        if self.y != 70:
            self.y += self.dir


    @staticmethod
    def draw(self):
        # self.image.clip_draw IDLE
        if self.face_dir == 1:
            self.image.clip_draw(299, 236, 16, 26, self.x, self.y, 16 * 2.5, 26 * 2.5)
        else:
            self.image.clip_draw(1, 236, 16, 26, self.x, self.y, 16 * 2.5, 26 * 2.5)


class RUN:
    def enter(self, event):
        print('ENTER RUN')
        if event == RD:
            self.dir += 1
        elif event == LD:
            self.dir -= 1
        elif event == RU:
            self.dir -= 1
        elif event == LU:
            self.dir += 1

    def exit(self, event):
        print('EXIT RUN')
        self.face_dir = self.dir
        if event == ATTACK:
            self.fire_snow()

    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time

        self.x = clamp(0, self.x, 1280)

    def draw(self):
        if self.dir == -1:
            self.image.clip_draw(21 + int(self.frame) * 17, 236, 16, 26, self.x, self.y, 16 * 2.5, 26 * 2.5)  # 왼쪽 이동
        elif self.dir == 1:
            self.image.clip_draw(279 - int(self.frame) * 17, 236, 16, 26, self.x, self.y, 16 * 2.5, 26 * 2.5)  # 오른쪽 이동

class DO_ATTACK:
    def enter(self, event):
        print('ENTER ATTACK')

    def exit(self, event):
        print('EXIT RUN')
        self.face_dir = self.dir
        if event == ATTACK:
            self.fire_snow()

    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
        self.x = clamp(0, self.x, 1280)

    def draw(self):
        if self.face_dir == -1:
            self.image.clip_draw(26 - int(self.frame) * 25, 200, 15 + int(self.frame) * 9, 23, self.x, self.y, 15 * 2.5 + int(self.frame) * 9, 23 * 2.5)
            #     self.image.clip_draw(26 - (self.aframe * 25), 200, 15 + (self.aframe * 9), 23, self.x, self.y, 15 + (self.aframe * 9) * 2.5, 23 * 2.5)
        elif self.face_dir == 1:
            self.image.clip_draw(274 + int(self.frame) * 17, 200, 15 + int(self.frame) * 9, 23, self.x, self.y, 15 * 2.5 + (int(self.frame) * 9), 23 * 2.5)

class JUMP:
    def enter(self, event):
        print('ENTER JUNP')
        if event == AD:
            self.dir += 1
        elif event == AD:
            self.dir -= 1

    def exit(self, event):
        print('EXIT JUMP')
        self.face_dir = self.dir
        if event == ATTACK:
            self.fire_snow()
    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        self.y += self.dir * RUN_SPEED_PPS * game_framework.frame_time
        print(f'{self.y}')
    def draw(self):
        if self.face_dir == -1:
            self.image.clip_draw(75 + int(self.frame) * 17, 236, 16, 36, self.x, self.y, 16 * 2.5, 36 * 2.5)
            print('그려지는중')
        elif self.face_dir == 1:
            self.image.clip_draw(225 - int(self.frame) * 17, 236, 16, 36, self.x, self.y, 16 * 2.5, 36 * 2.5)
            print('그려지는중')

next_state = {
    IDLE:  {RU: RUN,  LU: RUN,  RD: RUN,  LD: RUN, ATTACK: DO_ATTACK, AD: JUMP},
    RUN:   {RU: IDLE, LU: IDLE, RD: IDLE, LD: IDLE, ATTACK: DO_ATTACK, AD: JUMP},
    DO_ATTACK: {RU: IDLE, LU: IDLE, RD: IDLE, LD: IDLE, ATTACK: DO_ATTACK, AD: JUMP},
    JUMP: {RU: RUN,  LU: RUN,  RD: RUN,  LD: RUN, ATTACK: DO_ATTACK, AU: IDLE}
}

class Nick:
    def __init__(self):
        self.x,self.y = 0, 100
        self.frame = 0
        self.dir, self.face_dir = 0, 1
        self.image = load_image('Nick.png')
        self.font = load_font('ENCR10B.TTF', 16)

        self.event_que = []
        self.cur_state = IDLE
        self.cur_state.enter(self, None)


    def update(self):
        self.cur_state.do(self)

        if self.event_que:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            try:
                self.cur_state = next_state[self.cur_state][event]
            except KeyError:
                print(f'ERROR: State {self.cur_state.__name__}    Event {event_name[event]}')
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)
        self.font.draw(self.x - 60, self.y + 50, f'Time: {get_time():.2f}', (255, 255, 0))
        draw_rectangle(*self.get_bb())

    def add_event(self, event):
        self.event_que.insert(0, event)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def fire_snow(self):
        print('FIRE SNOW')
        # if self.face_dir == -1:
        #     attack = Attack(self.x, self.y, self.face_dir)
        #     print(type(attack))
        # else:
        attack = Attack(self.x, self.y, self.face_dir)

        game_world.add_object(attack, 1)

    def get_bb(self):
        return self.x - 19, self.y - 33, self.x + 19, self.y + 33

    def handle_collision(self, other, group):
        pass


# def handle_events():
#     global running
#     events = get_events()
#     for event in events:
#         if event.type == SDL_QUIT:
#             running = False
#         elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
#             running = False
#
#
# nick = None
# map = None
# running = True
#
# def enter():
#     global nick, map, running
#     nick = Nick()
#     map = Map()
#     running = True
#
# def exit():
#     global nick, map
#     del nick
#     del map
#
# def update():
#     nick.update()
#
# def draw():
#     clear_canvas()
#     map.draw()
#     nick.draw()
#     update_canvas()
#
#
# open_canvas(MAP_WIDTH * MAP_SIZE, MAP_HEIGHT * MAP_SIZE)
#
# enter()
# # game main loop code
# while running:
#     handle_events()
#     update()
#     draw()
#     delay(0.1)
# exit()
#
# # finalization code
# close_canvas()
