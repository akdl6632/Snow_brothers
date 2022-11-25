from pico2d import *
import play_state

MAP_WIDTH, MAP_HEIGHT = 256, 223
MAP_SIZE = 5

Blocks = []
map_y = 0


class Map:
    def __init__(self):
        if play_state.stage <= 10:
            self.image = load_image('stage1.png')
        elif play_state.stage > 10 and play_state.stage <= 20:
            self.image = load_image('stage2.png')
        elif play_state.stage > 20 and play_state.stage <= 30:
            self.image = load_image('stage3.png')
        else:
            print('오류')
        self.frame = 2250

    def update(self):
        pass
        # if play_state.stage == 2:
        #     self.image = load_image('stage2.png')
        #     print('stage2 start')

    # 필드 내 모든적을 잡으면 y값을 증가 시켜서 다음 맵 출력
    def draw(self):
        global map_y
        self.image.clip_draw(1, 18 + map_y, 256, 223, MAP_WIDTH * MAP_SIZE // 2, MAP_HEIGHT * MAP_SIZE // 2, MAP_WIDTH * MAP_SIZE, MAP_HEIGHT * MAP_SIZE)
        # draw_rectangle(*self.get_bb())

    def get_bb(self):
        # return 0, 0, 256 * 5, 70
        # return Blocks
        pass
class Block:
    def __init__(self, x, y, width, height):
        self.x, self.y, self.width, self.height = x, y, width, height
    def draw(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - self.width / 2, self.y - self.height / 2, self.x + self.width / 2, self.y + self.height / 2

    # collide 랑만 비교하기,     def handle_collision(self, other, group): 할 필요 없을 듯
