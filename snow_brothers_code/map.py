from pico2d import *

MAP_WIDTH, MAP_HEIGHT = 256, 223
MAP_SIZE = 5

class Map:
    def __init__(self):
        self.image = load_image('stage1.png')
        self.frame = 2250

    def update(self):
        pass

    # 필드 내 모든적을 잡으면 y값을 증가 시켜서 다음 맵 출력
    def draw(self):
        self.image.clip_draw(1, 18, 256, 223, MAP_WIDTH * MAP_SIZE // 2, MAP_HEIGHT * MAP_SIZE // 2, MAP_WIDTH * MAP_SIZE, MAP_HEIGHT * MAP_SIZE)