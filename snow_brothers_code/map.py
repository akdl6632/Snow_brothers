from pico2d import *
import play_state
import nick

MAP_WIDTH, MAP_HEIGHT = 256, 223
MAP_SIZE = 5

map_y = 0

Block_SXpos = [[0, 485, 965, 245, 0, 725, 165, 325], [320, 165, 485, 965, 485, 320, 485, 965, 245]]
Block_EXpos = [[320, 800, 1280, 1040, 560, 1280, 1120, 960], [1040, 320, 965, 1120, 965, 1040, 965, 1120, 800]]
# Block_Ypos = [260, 260, 260, 420, 580, 580, 750, 825]
Block_Ypos = [[235, 235, 235, 395, 555, 555, 715, 800], [235, 395, 395, 555, 555, 715, 715, 800, 800]]

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
    def __init__(self, i):
        self.sx, self.ex, self.y = Block_SXpos[play_state.stage - 1][i], Block_EXpos[play_state.stage - 1][i], Block_Ypos[play_state.stage - 1][i]

    def update(self):
        pass

    def draw(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.sx, self.y, self.ex, self.y

    def handle_collision(self, other, group):
        if group == 'nick:map':
            if nick.Is_JUMP == False:
                play_state.nick.y = self.y + 20
                nick.Is_Meet_Wall = True
