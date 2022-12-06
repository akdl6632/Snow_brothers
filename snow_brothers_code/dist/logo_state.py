from pico2d import *
import game_framework
import title_state
import play_state

# running = True
image = None
logo_time = 0.0
MAP_WIDTH, MAP_HEIGHT = 256, 223
MAP_SIZE = 5


def enter():
    global image
    image = load_image('tuk_credit.png')
    pass

def exit():
    global image
    del image
    pass

def update():
    global logo_time
    delay(0.01)
    logo_time += 0.01
    # global running
    if logo_time >= 0.5:
        logo_time = 0
        # running = False
        # game_framework.quit()
        game_framework.change_state(title_state)


def draw():
    clear_canvas()
    image.clip_draw(0, 0, 800, 600, MAP_WIDTH * MAP_SIZE // 2, MAP_HEIGHT * MAP_SIZE // 2, MAP_WIDTH * MAP_SIZE, MAP_HEIGHT * MAP_SIZE)
    update_canvas()

def handle_events():
    events = get_events()





