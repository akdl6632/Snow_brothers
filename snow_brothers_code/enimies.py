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

R_Is_Meet_Wall = False
F_Is_Meet_Wall = True
Y_Is_Meet_Wall = True

# RedDemon_Xpos = [75, 55, 215, 75, 180]
RedDemon_Xpos = [[375, 275, 1075, 375, 900],
                 [None],
                 [125, 1175, 325, 975],
                 [None],
                 [85, 160, 15, 245],
                 [15, 235],
                 [75, 165, 235, 50, 45, 170],
                 [10, 240, 70, 185],
                 [65, 195],
                 [None]]
RedDemon_Ypos = [[260, 420, 420, 580, 580],
                 [None],
                 [260, 260, 580, 580],
                 [None],
                 [260, 260, 420, 420],
                 [420, 420],
                 [260, 260, 340, 740, 905, 905],
                 [260, 260, 825, 825],
                 [260, 260],
                 [None]]
RedDemon_dir = [[-1, 1, -1, 1, -1],
                [None],
                [1, -1, 1, -1],
                [None],
                [-1, 1, 1, -1],
                [1, -1],
                [-1, -1, 1, 1, 1, 1],
                [1, -1, -1, 1],
                [1, -1],
                [None]]

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

        # global R_Is_Meet_Wall
        #
        # # print(R_Is_Meet_Wall)
        #
        # # R_Is_Meet_Wall = False
        #
        # if self.y < 100:
        #     R_Is_Meet_Wall = True
        #
        # if R_Is_Meet_Wall == False:
        #     self.y -= 1.5

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
                play_state.nick.x ,play_state.nick.y = 100, 100
                game_framework.change_state(play_state)

        global R_Is_Meet_Wall

        if group == 'RedDemon:map':
            pass

    def get_bb(self):
        return self.x - 30, self.y - 33, self.x + 30, self.y + 33

Frog_Xpos = [[None],
             [495],
             [75, 1200],
             [55, 205],
             [80, 175],
             [90, 175, 115, 145],
             [None],
             [40, 210],
             [None],
             [None]]
Frog_Ypos = [[None],
             [745],
             [740, 740],
             [260, 260],
             [740, 740],
             [580, 580, 905, 905],
             [None],
             [580, 580],
             [None],
             [None]]
Frog_dir = [[None],
            [-1],
            [-1, -1],
            [1, -1],
            [-1, 1],
            [1, -1, -1, 1],
            [None],
            [-1, 1],
            [None],
            [None]]

class Frog:
    def __init__(self, i):
        # self.x, self.y = 640, 100 #825
        self.x, self.y = Frog_Xpos[play_state.stage - 1][i], Frog_Ypos[play_state.stage - 1][i]
        self.frame = 0
        self.dir, self.face_dir = Frog_dir[play_state.stage -1][i], Frog_dir[play_state.stage -1][i]
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
                play_state.nick.x ,play_state.nick.y = 100, 100
                game_framework.change_state(play_state)
    def get_bb(self):
        return self.x - 19, self.y - 33, self.x + 19, self.y + 33

# stage 8 2 개임 1개만 만들어서 오류남
Yellow_Troll_Xpos = [[None],
                     [375, 925, 350, 650],
                     [None],
                     [195, 75, 125],
                     [130],
                     [130],
                     [None],
                     [130, 130],
                     [40, 130],
                     [None]]
Yellow_Troll_Ypos = [[None],
                     [265, 425, 910, 910],
                     [None],
                     [380, 740, 905],
                     [905],
                     [260],
                     [None],
                     [260, 905],
                     [120, 740],
                     [None]]
Yellow_Troll_dir = [[None],
                    [1, -1, 1, 1],
                    [None],
                    [1, 1, 1],
                    [1],
                    [1],
                    [None],
                    [-1, 1],
                    [1, 1],
                    [None]]
class Yellow_Troll:
    def __init__(self, i):
        self.x, self.y = Yellow_Troll_Xpos[play_state.stage - 1][i], Yellow_Troll_Ypos[play_state.stage - 1][i]
        self.frame = 0
        self.dir, self.face_dir = Yellow_Troll_dir[play_state.stage -1][i], Yellow_Troll_dir[play_state.stage -1][i]
        self.ver = 0
        self.jump = 0
        self.attack = 0
        self.image = load_image('Enemies.png')
        self.hp = 1

    def update(self):
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
                play_state.nick.x ,play_state.nick.y = 100, 100
                game_framework.change_state(play_state)
    def get_bb(self):
        return self.x - 30, self.y - 33, self.x + 30, self.y + 33