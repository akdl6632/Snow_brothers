from pico2d import *
import play_state
import nick
import enimies
import game_framework
import game_world

MAP_WIDTH, MAP_HEIGHT = 256, 223
MAP_SIZE = 5

map_y = 0

Block_SXpos = [[0, 485, 965, 245, 0, 725, 165, 325],
               [320, 165, 485, 965, 320, 165, 485, 965, 245],
               [5, 405, 1045, 5, 565, 1205, 5, 245, 565, 885, 1205, 5, 325, 1125, 245],
               [160, 725, 5, 725, 240, 565, 165, 405],
               [165, 720, 5, 965, 165, 800, 5, 485, 720, 965, 165],
               [5, 325, 1125, 5, 1125, 5, 325, 725, 1125, 5, 965, 245],
               [240, 730, 5, 1045, 480, 320, 1040, 165, 645, 245, 965, 565, 5, 805],
               [5, 325, 1125, 165, 800, 5, 725, 245, 405],
               [160, 725, 5, 405, 1045, 160, 725, 5, 480, 1125, 325],
               [245, 5, 885, 245, 5]]
Block_EXpos = [[320, 800, 1280, 1040, 560, 1280, 1120, 960],
               [1040, 320, 965, 1120, 800, 320, 965, 1120, 800],
               [240, 880, 1280, 80, 720, 1280, 80, 400, 720, 1040, 1280, 160, 960, 1280, 1040],
               [560, 1125, 560, 1280, 320, 1045, 880, 1120],
               [565, 1120, 320, 1280, 485, 1120, 320, 565, 800, 1280, 1120],
               [160, 960, 1280, 160, 1280, 160, 560, 960, 1280, 320, 1280, 1040],
               [560, 1045, 240, 1280, 720, 480, 1280, 320, 1040, 565, 1280, 805, 400, 1120],
               [160, 960, 1280, 485, 1120, 560, 1280, 1040, 880],
               [560, 1125, 240, 880, 1280, 560, 1125, 175, 805, 1280, 960],
               [720, 560, 1280, 720, 560]]
Block_Ypos = [[235, 235, 235, 395, 555, 555, 715, 800],
              [235, 395, 395, 555, 555, 715, 715, 880, 880],
              [235, 235, 235, 395, 395, 395, 555, 555, 555, 555, 555, 715, 715, 715, 880],
              [235, 235, 395, 395, 555, 555, 715, 880],
              [235, 235, 395, 395, 555, 555, 715, 715, 715, 715, 880],
              [235, 235, 235, 395, 395, 555, 555, 555, 555, 715, 715, 880],
              [235, 235, 315, 315, 395, 475, 475, 555, 555, 715, 715, 800, 880, 880],
              [235, 235, 235, 395, 395, 555, 555, 715, 800],
              [235, 235, 395, 395, 395, 555, 555, 715, 715, 715, 880],
              [235, 400, 480, 570, 730]]

class Map:
    def __init__(self):
        if play_state.stage <= 10:
            self.image = load_image('stage1.png')
            self.bgm = load_music('World1.mp3')
            self.bgm.set_volume(32)
            self.bgm.repeat_play()
            if play_state.stage == 10:
                self.bgm.stop()
                self.bgm2 = load_music('Boss')
                self.bgm2.set_volume(32)
                self.bgm2.repeat_play()
        elif play_state.stage > 10 and play_state.stage <= 20:
            self.image = load_image('stage2.png')
        elif play_state.stage > 20 and play_state.stage <= 30:
            self.image = load_image('stage3.png')
        else:
            print('??????')
        self.frame = 2250

    def update(self):
        pass
        # if play_state.stage == 2:
        #     self.image = load_image('stage2.png')
        #     print('stage2 start')

    # ?????? ??? ???????????? ????????? y?????? ?????? ????????? ?????? ??? ??????
    def draw(self):
        global map_y
        self.image.clip_draw(1, 18 + map_y, 256, 223, MAP_WIDTH * MAP_SIZE // 2, MAP_HEIGHT * MAP_SIZE // 2, MAP_WIDTH * MAP_SIZE, MAP_HEIGHT * MAP_SIZE)
        # draw_rectangle(*self.get_bb())

    def get_bb(self):
        pass
class Block:
    def __init__(self, i):
        self.sx, self.ex, self.y = Block_SXpos[play_state.stage - 1][i], Block_EXpos[play_state.stage - 1][i], Block_Ypos[play_state.stage - 1][i]
        # print(self.sx, self.y, self.ex, self.y)

    def update(self):
        pass

    def draw(self):
        pass

    def get_bb(self):
        return self.sx, self.y, self.ex, self.y

    def handle_collision(self, other, group):
        global map_y

        if group == 'nick:map':
            if nick.Is_JUMP == False:
                play_state.nick.y = self.y + 20
                nick.Is_Meet_Wall = True

        if group == 'RedDemon:map':
            pass

        if group == 'Frog:map':
            pass

        if group == 'Yellow_Troll:map':
            pass

