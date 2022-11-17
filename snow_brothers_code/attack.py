from pico2d import *
import game_framework
import game_world

PIXEL_PER_METER = (10.0 / 0.3)
ATTACK_SPEED_KMPH = 40.0
ATTACK_SPEED_MPM = (ATTACK_SPEED_KMPH * 1000.0 / 60.0)
ATTACK_SPEED_MPS = (ATTACK_SPEED_MPM / 60.0)
ATTACK_SPEED_PPS = (ATTACK_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5

y_down = 0.2

class Attack:
    image = None

    def __init__(self, x = 400, y = 300, face_dir = 1):
        self.frame = 0
        if Attack.image == None:
            Attack.image = load_image('Nick.png')
        self.x, self.y, self.face_dir = x, y, face_dir

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        self.x += self.face_dir * ATTACK_SPEED_PPS * game_framework.frame_time
        global y_down
        if int(self.frame) == 1:
            self.y -= y_down

        # 공격이 일정 범위 이상 이동하면 삭제되도록 설정
        if self.y < 80:
            # print(self.y)
            # print('삭제')
            game_world.remove_object(self)

    def draw(self):
        if self.face_dir == -1:
            if int(self.frame) == 0:
                self.image.clip_draw(118, 200, 8, 23, self.x - 40, self.y, 8 * 2.5, 23 * 2.5)
            else:
                self.image.clip_draw(110, 210, 6, 11, self.x - 40, self.y, 6 * 2.5, 11 * 2.5)
        elif self.face_dir == 1:
            if int(self.frame) == 0:
                self.image.clip_draw(190, 200, 8, 23, self.x + 40, self.y, 8 * 2.5, 23 * 2.5)
            else:
                self.image.clip_draw(200, 210, 6, 11, self.x + 40, self.y, 6 * 2.5, 11 * 2.5)

        draw_rectangle(*self.get_bb())

    def get_bb(self):
        # return self.x - 4, self.y - 12, self.x + 4, self.y + 12
        if self.face_dir == -1:
            if int(self.frame) == 0:
                return self.x - 4 - 40, self.y - 12, self.x + 4 - 40, self.y + 25
            else:
                return self.x - 4 - 40, self.y - 12, self.x + 4 - 40, self.y + 12
        elif self.face_dir == 1:
            if int(self.frame) == 0:
                return self.x - 4 + 40, self.y - 12, self.x + 4 + 40, self.y + 25
            else:
                return self.x - 4 + 40, self.y - 12, self.x + 4 + 40, self.y + 12

    def handle_collision(self, other, group):
        if group == 'attack:enimies':
            game_world.remove_object(self)