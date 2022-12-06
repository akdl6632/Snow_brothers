from pico2d import *

import game_framework
import game_world
from attack import Attack

import time

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

JUMP_SPEED_KMPH = 40.0
JUMP_SPEED_MPM = (JUMP_SPEED_KMPH * 1000.0 / 60.0)
JUMP_SPEED_MPS = (JUMP_SPEED_MPM / 60.0)
JUMP_SPEED_PPS = (JUMP_SPEED_MPS * PIXEL_PER_METER)

JUMP_PER_TIME = 1.0 / TIME_PER_ACTION

frame_time = 0.5
current_time = time.time()

# 점프 최댓값
JUMP_MAX = 230
JUMP_Y = 0.0
Is_JUMP = False
Is_Meet_Wall = True

RD, LD, RU, LU, TIMER, ATTACK, AU, AD, GO_IDLE, GO_Dead, GO_RUN, GO_Alive, Dead, Alive = range(14)
event_name = ['RD', 'LD', 'RU', 'LU', 'TIMER', 'ATTACK', 'AU', 'AD', 'GO_IDLE', 'GO_Dead', 'GO_RUN', 'GO_Alive', 'Dead', 'Alive']

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
    def enter(self, event):
        # print('ENTER IDLE')
        # print(f'{self.dir, self.face_dir}')
        self.dir = 0
        self.timer = 100

        global Is_Meet_Wall
        # print(Is_Meet_Wall)

        if self.y > 100:
            Is_Meet_Wall = False
        # if event == AU:
        #     self.dir -= 1

    @staticmethod
    def exit(self, event):
        # print('EXIT IDLE')
        # self.face_dir = self.dir
        # print(self.face_dir)
        if event == ATTACK:
            self.fire_snow()

    @staticmethod
    def do(self):
        # IDLE state 때 이미지 변화 없음
        # 그냥 키를 때면 IDLE 상태가 됨
        # print(Is_Meet_Wall)
        global Is_Meet_Wall

        # if self.y < 100:
        #     Is_Meet_Wall = True
        #
        # if Is_Meet_Wall == False:
        #     self.y -= 0.5
        # pass


    @staticmethod
    def draw(self):
        # self.image.clip_draw IDLE
        if self.face_dir == 1:
            self.image.clip_draw(299, 236, 16, 26, self.x, self.y, 16 * 2.5, 26 * 2.5)
        else:
            self.image.clip_draw(1, 236, 16, 26, self.x, self.y, 16 * 2.5, 26 * 2.5)


class RUN:
    def enter(self, event):
        # print('ENTER RUN')
        # print(f'{self.face_dir}')
        self.state_Alive = False
        if event == RD:
            self.dir += 1
        elif event == RU:
            self.dir -= 1
        if event == LD:
            self.dir -= 1
        elif event == LU:
            self.dir += 1

        global Is_Meet_Wall

        # if self.y > 100:
        #     Is_Meet_Wall = False

    def exit(self, event):
        # print('EXIT RUN')
        self.face_dir = self.dir
        if event == ATTACK:
            self.fire_snow()

    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time

        self.x = clamp(0, self.x, 1280)

        global Is_Meet_Wall

        # if self.y < 100:
        #     Is_Meet_Wall = True

        # if Is_Meet_Wall == False:
        #     self.y -= 0.5
        if self.y > 100:
            self.y -= 0.5

    def draw(self):
        if self.dir == -1:
            self.image.clip_draw(21 + int(self.frame) * 17, 236, 16, 26, self.x, self.y, 16 * 2.5, 26 * 2.5)  # 왼쪽 이동
        elif self.dir == 1:
            self.image.clip_draw(279 - int(self.frame) * 17, 236, 16, 26, self.x, self.y, 16 * 2.5, 26 * 2.5)  # 오른쪽 이동

class DO_ATTACK:
    def enter(self, event):
        self.A_bgm = load_wav('attack.wav')
        self.A_bgm.set_volume(50)
        self.A_bgm.play(1)
        self.frame = 0

    def exit(self, event):
        # print('EXIT ATTACK')
        if event == ATTACK:
            self.fire_snow()

    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * JUMP_PER_TIME * game_framework.frame_time) % 2
        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
        self.x = clamp(0, self.x, 1280)

        if self.frame >= 1.5:
            self.add_event(GO_IDLE)

        # print(f'{self.frame}')

    def draw(self):
        if self.face_dir == -1:
            self.image.clip_draw(26 - int(self.frame) * 25, 200, 15 + int(self.frame) * 9, 23, self.x, self.y, 15 * 2.5 + int(self.frame) * 9, 23 * 2.5)
            #     self.image.clip_draw(26 - (self.aframe * 25), 200, 15 + (self.aframe * 9), 23, self.x, self.y, 15 + (self.aframe * 9) * 2.5, 23 * 2.5)
        elif self.face_dir == 1:
            self.image.clip_draw(274 + int(self.frame) * 17, 200, 15 + int(self.frame) * 9, 23, self.x, self.y, 15 * 2.5 + (int(self.frame) * 9), 23 * 2.5)

class JUMP:
    def enter(self, event):
        self.J_bgm = load_wav('Jump.wav')
        self.J_bgm.set_volume(60)
        self.J_bgm.play(1)
        # 점프 누르고 이동을 위해 구현
        if event == RD:
            self.dir += 1
        elif event == LD:
            self.dir -= 1
        elif event == RU:
            self.dir -= 1
        elif event == LU:
            self.dir += 1


        global JUMP_Y
        JUMP_Y = 0.0

        global Is_JUMP
        if Is_JUMP == False:
            Is_JUMP = True

    def exit(self, event):
        # print('EXIT JUMP')
        if event == ATTACK:
            self.fire_snow()

        global Is_JUMP
        Is_JUMP = False

    def do(self):
        # 한번 누르면 일정시간 비행 후 낙하.
        # 시간
        # global current_time
        # global frame_time
        #
        # frame_time = time.time() - current_time
        # frame_rate = 1 / frame_time
        # current_time += frame_time
        # print(f'frame time is = {frame_time}')
        # 어떻게 하는지 모르겠다
        # 그냥 최대 점프 범위 설정하고 그만큼만 뛰게 하자

        global JUMP_Y
        global Is_JUMP

        # if JUMP_Y < JUMP_MAX and Is_JUMP:

        if JUMP_Y >= JUMP_MAX: # 최대 범위를 넘어가면 점프 그만.
            # Is_JUMP = False
            # Nick.add_event(IDLE)
            self.add_event(GO_IDLE)
            # self.add_event(GO_RUN)

        if Is_JUMP: # 점프키가 눌렸다면 점프하게 구현
            JUMP_Y += 1.5


            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
            if self.face_dir == 1:
                self.y += 1 * JUMP_SPEED_PPS * game_framework.frame_time
            elif self.face_dir == -1:
                self.y -= -1 * JUMP_SPEED_PPS * game_framework.frame_time

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time

        self.x = clamp(0, self.x, 1280)
    def draw(self):
        global Is_JUMP
        if Is_JUMP:
            # print(Is_JUMP, self.face_dir)
            if self.face_dir == -1:
                self.image.clip_draw(75 + int(self.frame) * 17, 236, 16, 36, self.x, self.y, 16 * 2.5, 36 * 2.5)
            elif self.face_dir == 1:
                self.image.clip_draw(225 - int(self.frame) * 17, 236, 16, 36, self.x, self.y, 16 * 2.5, 36 * 2.5)

next_state = {
    IDLE:  {RU: IDLE,  LU: IDLE,  RD: RUN,  LD: RUN, ATTACK: DO_ATTACK, AD: JUMP, GO_Dead: Dead},
    RUN:   {RU: IDLE, LU: IDLE, RD: RUN, LD: RUN, ATTACK: DO_ATTACK, AD: JUMP, GO_Dead: Dead},
    DO_ATTACK: {RU: IDLE, LU: IDLE, RD: RUN, LD: RUN, ATTACK: DO_ATTACK, AU: IDLE, GO_IDLE: IDLE, GO_Dead: Dead},
    JUMP: {RU: JUMP, LU: JUMP, AU: JUMP, RD: RUN, LD: RUN, ATTACK: DO_ATTACK, GO_IDLE: IDLE, GO_RUN: RUN, GO_Dead: Dead},
    Dead: {RU: Dead,  LU: Dead,  RD: Dead,  LD: Dead, ATTACK: Dead, JUMP: Dead, AD: Dead, GO_Dead: Dead, GO_Alive: Alive},
    Alive: {RU: IDLE, LU: IDLE, RD: RUN, LD: RUN, ATTACK: DO_ATTACK, AD: JUMP, GO_RUN: RUN, GO_Dead: Dead},
}

class Alive:
    def enter(self, event):
        self.state_alive = True
        self.state_Dead = False

        if event == RD:
            self.dir += 1
        elif event == LD:
            self.dir -= 1
        elif event == RU:
            self.dir -= 1
        elif event == LU:
            self.dir += 1

        self.frame = 0
        self.timer = 0

    def exit(self):
        pass

    def do(self):
        self.timer = get_time()
        if self.timer >= 5:
            self.frame += 1
            self.timer = get_time()

        if self.frame == 5:
            state_alive = False
            self.add_event(GO_RUN)

    def draw(self):
        if self.frame == 1:
            self.image.clip_draw(1, 281, 8, 31, self.x, self.y, 8 * 2.5, 31 * 2.5)
        elif self.frame == 2:
            self.image.clip_draw(9, 281, 19, 31, self.x, self.y, 19 * 2.5, 31 * 2.5)
        else:
            self.image.clip_draw(28 + int(self.frame - 3) * 16, 281, 16, 31, self.x, self.y, 16 * 2.5, 31 * 2.5)
class Dead:
    def enter(self, event):
        print('a')
        self.frame = 0
        self.timer = 0
        self.state_Dead = True

    def exit(self, event):
        pass

    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        self.timer = get_time()
        # if self.timer >= 5:
        #     self.add_event(GO_Alive)

    def draw(self):
        self.image.clip_draw(1 + int(self.frame) * 32, 91, 16, 36, self.x, self.y, 16 * 2.5, 36 * 2.5)

class Nick:
    def __init__(self):
        self.x, self.y = 100, 100
        self.frame = 0
        self.dir, self.face_dir = 0, 1
        self.image = load_image('Nick.png')
        self.font = load_font('ENCR10B.TTF', 16)

        self.event_que = []
        self.cur_state = IDLE
        self.cur_state.enter(self, None)

        self.state_alive = False
        self.state_Dead = False




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

        global Is_Meet_Wall

        if self.y < 100:
            Is_Meet_Wall = True

        if Is_Meet_Wall == False:
            self.y -= 1.5

    def draw(self):
        self.cur_state.draw(self)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def fire_snow(self):
        attack = Attack(self.x, self.y, self.face_dir)
        game_world.add_object(attack, 1)
        game_world.add_collision_pairs(attack, None, 'attack:enimies')
        game_world.add_collision_pairs(attack, None, 'attack:map')
        game_world.add_collision_pairs(attack, None, 'attack:bosses')

    def get_bb(self):
        return self.x - 19, self.y - 33, self.x + 19, self.y + 33

    def handle_collision(self, other, group):
        if self.state_alive == False or self.Dead == False: # 부활 상태 또는 사망 상태가 아니라면 충돌
            if group == 'nick:enimies':
                pass

        if group == 'nick:map':
            pass
