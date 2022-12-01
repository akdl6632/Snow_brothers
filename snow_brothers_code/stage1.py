from pico2d import *
import play_state
import nick

MAP_WIDTH, MAP_HEIGHT = 256, 223
MAP_SIZE = 5

map_y = 0

Block_SXpos = [0, 485, 965, 245, 0, 725, 165, 325]
Block_EXpos = [320, 800, 1280, 1040, 560, 1280, 1120, 960]
Block_Ypos = [235, 235, 235, 395, 555, 555, 715, 800]

class Map:
    def __init__(self):
        self.image = load_image('stage1.png')
        # self.canvas_width = 235
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        # self.w = 235
        self.w = self.image.w
        self.h = self.image.h

    def draw(self):
        # self.image.clip_draw_to_origin(
        #     self.window_left + 2, self.window_bottom + 17,
        #     self.canvas_width * 18 + 110, self.canvas_height * 10,
        #     0, 0
        # )
        self.image.clip_draw_to_origin(
            self.window_left, self.window_bottom,
            self.canvas_width, self.canvas_height,
            0, 0
        )

    def update(self):
        self.window_left = clamp(0,
            int(play_state.nick.x) - self.canvas_width//2,
            self.w - self.canvas_width - 1)
        self.window_bottom = clamp(0,
            int(play_state.nick.y) - self.canvas_height // 2,
            self.h - self.canvas_height - 1)

    def handle_event(self, event):
        pass

class Block:
    def __init__(self, i):
        self.sx, self.ex, self.y = Block_SXpos[i], Block_EXpos[i], Block_Ypos[i]

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
