from pico2d import *
import logo_state

import game_framework
import play_state

MAP_WIDTH, MAP_HEIGHT = 256, 223
MAP_SIZE = 5

image = None
bgm2 = None
bgm1 = None

def enter():
    global image, bgm1, bgm2
    image = load_image('snow_brothers.png')
    bgm1 = load_wav('Coin.wav')
    bgm1.set_volume(32)
    bgm2 = load_music('Select.mp3')
    bgm2.set_volume(32)
    bgm2.play()

def exit():
    global image
    del image
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            bgm2.stop()
            bgm1.play()
            game_framework.change_state(play_state)
        elif event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()

def draw():
    clear_canvas()
    image.clip_draw(0, 0, 269, 192, MAP_WIDTH * MAP_SIZE // 2, MAP_HEIGHT * MAP_SIZE // 2, MAP_WIDTH * MAP_SIZE, MAP_HEIGHT * MAP_SIZE)
    update_canvas()

def update():
    pass

def pause():
    pass

def resume():
    pass






