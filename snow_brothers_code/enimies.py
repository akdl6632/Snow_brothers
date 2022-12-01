from pico2d import *
import game_framework
import game_world
import random
import play_state
import map
import nick

PIXEL_PER_METER = (10.0 / 0.3)
RedDemon_RUN_SPEED_KMPH = 30.0
RedDemon_RUN_SPEED_MPM = (RedDemon_RUN_SPEED_KMPH * 1000.0 / 60.0)
RedDemon_RUN_SPEED_MPS = (RedDemon_RUN_SPEED_MPM / 60.0)
RedDemon_RUN_SPEED_PPS = (RedDemon_RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3

# RedDemon_Xpos = [75, 55, 215, 75, 180]
RedDemon_Xpos = [[375, 275, 1075, 375, 900], [None], []]
RedDemon_Ypos = [[260, 420, 420, 580, 580], [None], []]
RedDemon_dir = [[-1, 1, -1, 1, -1], [None], []]

class RedDemon:
    def __init__(self, i):
        # self.x, self.y = 640, 100 #825
        # self.x, self.y = x, y #825
        # self.x, self.y = random.randint(325, 960) , 100 #825
        self.x, self.y = RedDemon_Xpos[play_state.stage - 1][i], RedDemon_Ypos[play_state.stage - 1][i]
        print(self.x)
        self.frame = 0
        # self.dir, self.face_dir = 1, 1
        self.dir, self.face_dir = RedDemon_dir[play_state.stage - 1][i], RedDemon_dir[play_state.stage - 1][i]
        self.ver = 0
        self.jump = 0
        self.attack = 0
        self.image = load_image('Enemies.png')
        self.hp = 1

    def update(self):
        # self.frame = (self.frame + 1) % 2
        # self.x += self.dir * 1
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        self.x += self.dir * RedDemon_RUN_SPEED_PPS * game_framework.frame_time
        if self.x > 1280:
            self.x = 1280
            self.dir = -1
            self.face_dir = -1
        elif self.x < 0:
            self.x = 0
            self.dir = 1
            self.face_dir = 1
        # self.x = clamp(325, self.x, 960)
        # self.y += self.ver * 1
        # self.y = clamp(100, self.y, MAP_HEIGHT * MAP_SIZE)

    def draw(self):
        if self.dir == -1:
            self.image.clip_draw(29 + int(self.frame) * 25, 526, 24, 26, self.x, self.y, 24 * 2.5, 26 * 2.5)  # 왼쪽 이동
        elif self.dir == 1:
            self.image.clip_draw(477 - int(self.frame) * 25, 526, 24, 26, self.x, self.y, 24 * 2.5, 26 * 2.5)  # 오른쪽 이동
        else:
            # self.image.clip_draw IDLE
            if self.face_dir == 1:
                self.image.clip_draw(505, 526, 23, 26, self.x, self.y, 24 * 2.5, 26 * 2.5)
            else:
                self.image.clip_draw(1, 526, 23, 26, self.x, self.y, 24 * 2.5, 26 * 2.5)

        draw_rectangle(*self.get_bb())

    def handle_collision(self, other, group):
        if group == 'attack:enimies':
            game_world.remove_object(self)
            play_state.Nick_kill += 1

            if play_state.Nick_kill == play_state.All_enimes[play_state.stage]:
                play_state.stage += 1
                print(f'stage is {play_state.stage}')
                map.map_y += 224
                game_framework.change_state(play_state)
    def get_bb(self):
        return self.x - 30, self.y - 33, self.x + 30, self.y + 33

Frog_Xpos = [[None], [375, 275, 1075, 375, 900], []]
Frog_Ypos = [[None], [260, 420, 420, 580, 580], []]
Frog_dir = [[None], [-1, 1, -1, 1, -1], []]

class Frog:
    def __init__(self, i):
        # self.x, self.y = 640, 100 #825
        self.x, self.y = Frog_Xpos[play_state.stage - 1][i], Frog_Ypos[play_state.stage - 1][i]
        self.frame = 0
        self.dir, self.face_dir = 1, 1
        self.ver = 0
        self.jump = 0
        self.attack = 0
        self.image = load_image('Enemies.png')
        self.hp = 1

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
        if self.dir == -1:
            self.image.clip_draw(29 + int(self.frame) * 17, 469, 16, 26, self.x, self.y, 16 * 2.5, 26 * 2.5)  # 왼쪽 이동
        elif self.dir == 1:
            self.image.clip_composite_draw(29 + int(self.frame) * 17, 469, 16, 26, -3.141592, 'v', self.x, self.y, 16 * 2.5, 26 * 2.5)  # 오른쪽 이동
        else:
            # self.image.clip_draw IDLE
            if self.face_dir == 1:
                self.image.clip_composite_draw(1, 469, 23, 26, -3.141592, 'v', self.x, self.y, 24 * 2.5, 26 * 2.5)
            else:
                self.image.clip_draw(1, 469, 23, 26, self.x, self.y, 24 * 2.5, 26 * 2.5)

        draw_rectangle(*self.get_bb())

    def handle_collision(self, other, group):
        if group == 'attack:enimies':
            game_world.remove_object(self)
            play_state.Nick_kill += 1

            if play_state.Nick_kill == play_state.All_enimes[play_state.stage]:
                play_state.stage += 1
                print(f'stage is {play_state.stage}')
                map.map_y += 224
                game_framework.change_state(play_state)
    def get_bb(self):
        return self.x - 19, self.y - 33, self.x + 19, self.y + 33

class Yellow_Troll:
    def __init__(self):
        self.x, self.y = random.randint(325, 960) , 100 #825
        self.frame = 0
        self.dir, self.face_dir = 1, 1
        self.ver = 0
        self.jump = 0
        self.attack = 0
        self.image = load_image('Enemies.png')
        self.hp = 1

    def update(self):
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
        if self.dir == -1:
            self.image.clip_draw(29 + int(self.frame) * 25, 415, 24, 26, self.x, self.y, 24 * 2.5, 26 * 2.5)  # 왼쪽 이동
        elif self.dir == 1:
            self.image.clip_composite_draw(29 + int(self.frame) * 25, 415, 24, 26, -3.141592, 'v', self.x, self.y, 24 * 2.5, 26 * 2.5)  # 오른쪽 이동
        else:
            # self.image.clip_draw IDLE
            if self.face_dir == 1:
                self.image.clip_composite_draw(1, 415, 24, 26, -3.141592, 'v', self.x, self.y, 24 * 2.5, 26 * 2.5)
            else:
                self.image.clip_draw(1, 415, 24, 26, self.x, self.y, 24 * 2.5, 26 * 2.5)

        draw_rectangle(*self.get_bb())

    def handle_collision(self, other, group):
        if group == 'attack:enimies':
            game_world.remove_object(self)
            play_state.Nick_kill += 1

            if play_state.Nick_kill == play_state.All_enimes[play_state.stage]:
                play_state.stage += 1
                print(f'stage is {play_state.stage}')
                map.map_y += 224
                game_framework.change_state(play_state)
    def get_bb(self):
        return self.x - 30, self.y - 33, self.x + 30, self.y + 33