import pico2d
import game_framework

import logo_state


MAP_WIDTH, MAP_HEIGHT = 256, 223
MAP_SIZE = 5

pico2d.open_canvas(MAP_WIDTH * MAP_SIZE, MAP_HEIGHT * MAP_SIZE)
game_framework.run(logo_state)
pico2d.clear_canvas()