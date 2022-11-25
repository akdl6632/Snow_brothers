from pico2d import *
import game_framework
import game_world
import random

PIXEL_PER_METER = (10.0 / 0.3)
RedDemon_RUN_SPEED_KMPH = 30.0
RedDemon_RUN_SPEED_MPM = (RedDemon_RUN_SPEED_KMPH * 1000.0 / 60.0)
RedDemon_RUN_SPEED_MPS = (RedDemon_RUN_SPEED_MPM / 60.0)
RedDemon_RUN_SPEED_PPS = (RedDemon_RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3

class Boss2:
    def __init__(self):
        self.x, self.y = 640, 100 #825
        self.frame = 0
        self.dir, self.face_dir = 1, 1
        self.ver = 0
        self.jump = 0
        self.attack = 0
        self.image = load_image('Bosses.png')
        self.hp = 2

    def update(self):
        # self.frame = (self.frame + 1) % 2
        # self.x += self.dir * 1
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        self.x += self.dir * RedDemon_RUN_SPEED_PPS * game_framework.frame_time
        if self.x > 960:
            self.x = 960
            self.dir = -1
            self.face_dir = -1
        elif self.x < 325:
            self.x = 325
            self.dir = 1
            self.face_dir = 1
        # self.x = clamp(325, self.x, 960)
        # self.y += self.ver * 1
        # self.y = clamp(100, self.y, MAP_HEIGHT * MAP_SIZE)

    def draw(self):
        self.image.clip_draw(130, 522, 128, 64, self.x, self.y)
        # if self.dir == -1:
        #     self.image.clip_draw(29 + int(self.frame) * 25, 526, 24, 26, self.x, self.y, 24 * 2.5, 26 * 2.5)  # 왼쪽 이동
        # elif self.dir == 1:
        #     self.image.clip_draw(477 - int(self.frame) * 25, 526, 24, 26, self.x, self.y, 24 * 2.5, 26 * 2.5)  # 오른쪽 이동
        # else:
        #     # self.image.clip_draw IDLE
        #     if self.face_dir == 1:
        #         self.image.clip_draw(505, 526, 23, 26, self.x, self.y, 24 * 2.5, 26 * 2.5)
        #     else:
        #         self.image.clip_draw(1, 526, 23, 26, self.x, self.y, 24 * 2.5, 26 * 2.5)

        draw_rectangle(*self.get_bb())

    def handle_collision(self, other, group):
        if group == 'attack:boss':
            game_world.remove_object(self)

    def get_bb(self):
        return self.x - 19, self.y - 33, self.x + 19, self.y + 33