from pico2d import *

MAP_WIDTH, MAP_HEIGHT = 256, 223
MAP_SIZE = 5

Blocks = []

class Map:
    def __init__(self):
        self.image = load_image('stage1.png')
        self.frame = 2250

    def update(self):
        pass

    # 필드 내 모든적을 잡으면 y값을 증가 시켜서 다음 맵 출력
    def draw(self):
        self.image.clip_draw(1, 18, 256, 223, MAP_WIDTH * MAP_SIZE // 2, MAP_HEIGHT * MAP_SIZE // 2, MAP_WIDTH * MAP_SIZE, MAP_HEIGHT * MAP_SIZE)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        # return 0, 0, 256 * 5, 70
        return Blocks
class Block:
    def __init__(self, x, y, width, height):
        self.x, self.y, self.width, self.height = x, y, width, height
    def draw(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - self.width / 2, self.y - self.height / 2, self.x + self.width / 2, self.y + self.height / 2

    # collide 랑만 비교하기,     def handle_collision(self, other, group): 할 필요 없을 듯
