from pico2d import *
import game_framework
import game_world
import time
import random

PIXEL_PER_METER = (10.0 / 0.3)
RedDemon_RUN_SPEED_KMPH = 30.0
RedDemon_RUN_SPEED_MPM = (RedDemon_RUN_SPEED_KMPH * 1000.0 / 60.0)
RedDemon_RUN_SPEED_MPS = (RedDemon_RUN_SPEED_MPM / 60.0)
RedDemon_RUN_SPEED_PPS = (RedDemon_RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3
class Boss1:
    def __init__(self):
        self.x, self.y = 1000, 800
        self.hp = 10
        self.frame = 1
        self.floor = 1
        self.time = 0
        self.image = load_image('Bosses.png')

    def update(self):
        self.time = get_time()

        # print(self.time // 10)

        if int(self.time) // 10 == 0:
            self.frame = 1

        else:
            self.time = 0

        if self.y >= 390:
            self.y -= 0.5

    def draw(self):
        if self.frame == 0:
            self.image.clip_draw(9, 753, 24, 8, self.x - 78 + 80, self.y + 23, 24 * 5, 8 * 5)
            self.image.clip_draw(9, 745, 47, 8, self.x - 20 + 80, self.y - 17, 47 * 5, 8 * 5)
            self.image.clip_draw(1, 729, 56, 16, self.x - 38 + 80, self.y - 77, 56 * 5, 16 * 5)
            self.image.clip_draw(9, 721, 48, 8, self.x - 18 + 80, self.y - 137, 48 * 5, 8 * 5)
            self.image.clip_draw(9, 713, 55, 8, self.x + 80, self.y - 177, 55 * 5, 8 * 5)
            self.image.clip_draw(26, 705, 39, 9, self.x + 40 + 80, self.y - 217, 39 * 5, 8 * 5)
            self.image.clip_draw(17, 690, 39, 15, self.x + 80, self.y - 275, 39 * 5, 15 * 5)

        elif self.frame == 1:
            self.image.clip_draw(77, 768, 23, 16, self.x - 115 + 80, self.y + 119, 23 * 5, 16 * 5)
            self.image.clip_draw(69, 753, 58, 15, self.x - 63 + 80, self.y + 42, 58 * 5, 15 * 5)
            self.image.clip_draw(96, 745, 32, 8, self.x + 80 + 7, self.y - 15, 32 * 5, 8 * 5)
            self.image.clip_draw(80, 729, 48, 16, self.x - 33 + 80, self.y - 75, 48 * 5, 16 * 5)
            self.image.clip_draw(96, 722, 32, 8, self.x + 80 + 7, self.y - 135, 32 * 5, 8 * 5)
            self.image.clip_draw(96, 706, 23, 16, self.x - 10 + 80, self.y - 195, 23 * 5, 16 * 5)
            self.image.clip_draw(96, 689, 31, 16, self.x + 80, self.y - 275, 31 * 5, 16 * 5)

    def handle_collision(self, other, group):
        if group == 'attack:bosses':
            print('a')
            self.hp -= 1
            if self.hp <= 0:
                game_world.remove_object(self)

    def get_bb(self):
        return self.x - 19, self.y - 33, self.x + 19, self.y + 33


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
