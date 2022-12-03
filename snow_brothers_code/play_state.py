from pico2d import *
import game_framework
import logo_state
import title_state
import game_world

from nick import Nick
from map import Map
from map import Block
from enimies import RedDemon
from enimies import Frog
from enimies import Yellow_Troll
from bosses import Boss2

nick = None
map = None

Nick_kill = 0
stage = 1

# enimies = None
RedDemons = []
Frogs = []
Yellow_Trolls = []
Boss = []
Blocks = []


RedDemonlist = dict()
# RedDemonlist = {1: 5, 2: 0, 3: 4, 4: 0, 5: 4, 6: 2, 7: 6, 8: 4, 9: 2}
RedDemonlist = {1: 5, 2: 0, 3: 4, 4: 0, 5: 4, 6: 2, 7: 6, 8: 4, 9: 2}

Froglist = dict()
Froglist = {1: 0, 2: 1, 3: 2, 4: 2, 5: 2, 6: 4, 7: 0, 8: 2, 9: 2, 10: 0}

Yellow_Trolllist = dict()
Yellow_Trolllist = {1: 0, 2: 4, 3: 0, 4: 3, 5: 1, 6: 1, 7: 0, 8: 2, 9: 2, 10: 0}

All_enimes = dict()
All_enimes = {1: 5, 2: 5, 3: 6, 4: 5, 5: 7, 6: 7, 7: 6, 8: 8, 9: 6, 10: 0}

Bosslist = dict()
Bosslist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 1}

Blocks = dict()
Blocklist = {1: 8, 2: 9, 3: 15, 4: 8, 5: 11, 6: 12, 7: 14, 8: 9, 9: 11, 10: 5}

MAP_WIDTH, MAP_HEIGHT = 256, 223
MAP_SIZE = 5
x = 0

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        else:
            nick.handle_event(event)


# 초기화
def enter():
    game_world.clear()
    global Nick_kill
    global RedDemons, Frogs, Yellow_Trolls, Boss
    global Blocks
    global stage

    global nick, map
    nick = Nick()
    map = Map()
    game_world.add_object(map, 0)
    game_world.add_object(nick, 1)

    Nick_kill = 0

    Blocks = [Block(i) for i in range(Blocklist[stage])]
    game_world.add_objects(Blocks, 1)


    RedDemons = [RedDemon(i) for i in range(RedDemonlist[stage])]
    game_world.add_objects(RedDemons, 1)

    Frogs = [Frog(i) for i in range(Froglist[stage])]
    game_world.add_objects(Frogs, 1)

    Yellow_Trolls = [Yellow_Troll(i) for i in range(Yellow_Trolllist[stage])]
    game_world.add_objects(Yellow_Trolls, 1)

    Boss = [Boss2() for i in range(Bosslist[stage])]
    game_world.add_objects(Boss, 1)

    # game_world.add_collision_pairs(nick, RedDemons, 'nick:enimies')
    game_world.add_collision_pairs(None, RedDemons, 'attack:enimies')
    game_world.add_collision_pairs(None, Frogs, 'attack:enimies')
    game_world.add_collision_pairs(None, Yellow_Trolls, 'attack:enimies')
    game_world.add_collision_pairs(None, Boss, 'attack:bosses')
    game_world.add_collision_pairs(nick, Blocks, 'nick:map')
    game_world.add_collision_pairs(RedDemons, Blocks, 'RedDemon:map')
    game_world.add_collision_pairs(Frogs, Blocks, 'Frog:map')
    game_world.add_collision_pairs(Yellow_Trolls, Blocks, 'Yellow_Troll:map')
    game_world.add_collision_pairs(None, Blocks, 'attack:map')

# 종료
def exit():
    game_world.clear()

def update():
    for game_object in game_world.all_objects():
        game_object.update()
    # delay(0.01)

    for a, b, group in game_world.all_collision_pairs():
        if collide(a, b):
            # print('COLLISION ', group)
            # print(a, b, group)
            a.handle_collision(b, group)
            b.handle_collision(a, group)

    # print(game_world.collision_group)

def draw_world():
    for game_object in game_world.all_objects():
        game_object.draw()

def draw():
    clear_canvas()
    draw_world()
    update_canvas()

def pause():
    pass

def resume():
    pass

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


def test_self():
    import play_state

    pico2d.open_canvas()
    game_framework.run(play_state)
    pico2d.clear_canvas()

if __name__ == '__main__':
    test_self()


# class Map:
#     def __init__(self):
#         self.image = load_image('stage1.png')
#         self.frame = 2250
#
#     # 필드 내 모든적을 잡으면 y값을 증가 시켜서 다음 맵 출력
#     def draw(self):
#         self.image.clip_draw(1, 18, 256, 223, MAP_WIDTH * MAP_SIZE // 2, MAP_HEIGHT * MAP_SIZE // 2, MAP_WIDTH * MAP_SIZE, MAP_HEIGHT * MAP_SIZE)
#
#

#
# # class attack:
# #     def __init__(self):
# #         self.x, self.y = 0, 100
# #         self.frame = 0
# #         self.jframe = 0
# #         self.aframe = 0
# #         self.aver = 0
# #         self.dir, self.face_dir = 0, 1
# #         self.ver = 0
# #         self.jump = 0
# #         self.attack = 0
# #         self.image = load_image('Nick.png')
# #
# #     def update(self):
# #         self.frame = (self.frame + 1) % 2
# #         self.x += self.dir * 1
# #         self.y += self.ver * 1
# #         if self.aver == 5:
# #             self.aver = 0
# #
# #     def draw(self):
# #         if self.attack == 1 and self.face_dir == -1:
# #             self.image.clip_draw(26 - (self.aframe * 25), 200, 15 + (self.aframe * 9), 23, self.x, self.y,
# #                                  15 + (self.aframe * 9) * 2.5, 23 * 2.5)
# #             if self.aver < 5:
# #                 self.image.clip_draw(109 + (self.aframe * 9), 200, 8, 23, self.x - (self.aver + 50), self.y, 8 * 2.5,
# #                                      23 * 2.5)
# #         elif self.attack == 1 and self.face_dir == 1:
# #             self.image.clip_draw(274 + (self.aframe * 17), 200, 15 + (self.aframe * 9), 23, self.x, self.y,
# #                                  15 + (self.aframe * 9) * 2.5, 23 * 2.5)
# #             if self.aver < 3:
# #                 self.image.clip_draw(190 + (self.aframe * 9), 200, 8, 23, self.x + (self.aver + 50), self.y, 8 * 2.5,
# #                                      23 * 2.5)
# #         elif self.jump == 1 and self.face_dir == -1:
# #             self.image.clip_draw(75 + (self.jframe * 17), 236, 16, 36, self.x, self.y, 16 * 2.5, 36 * 2.5)
# #         elif self.jump == 1 and self.face_dir == 1:
# #             self.image.clip_draw(225 - (self.jframe * 17), 236, 16, 36, self.x, self.y, 16 * 2.5, 36 * 2.5)
# #         elif self.dir == -1:
# #             self.image.clip_draw(21 + (self.frame * 17), 236, 16, 26, self.x, self.y, 16 * 2.5, 26 * 2.5)  # 왼쪽 이동
# #         elif self.dir == 1:
# #             self.image.clip_draw(279 - (self.frame * 17), 236, 16, 26, self.x, self.y, 16 * 2.5, 26 * 2.5)  # 오른쪽 이동
# #         else:
# #             # self.image.clip_draw IDLE
# #             if self.face_dir == 1:
# #                 self.image.clip_draw(299, 236, 16, 26, self.x, self.y, 16 * 2.5, 26 * 2.5)
# #             else:
# #                 self.image.clip_draw(1, 236, 16, 26, self.x, self.y, 16 * 2.5, 26 * 2.5)
#
#
# class Nick:
#     def __init__(self):
#         self.x, self.y = 0, 100
#         self.frame = 0
#         self.jframe = 0
#         self.aframe = 0
#         self.aver = 0
#         self.dir, self.face_dir = 0, 1
#         self.ver = 0
#         self.jump = 0
#         self.attack = 0
#         self.image = load_image('Nick.png')
#
#     def update(self):
#         self.frame = (self.frame + 1) % 3
#         self.jframe = (self.jframe + 1) % 4
#         self.aframe = (self.aframe + 1) % 2
#         self.x += self.dir * 1
#         self.y += self.ver * 1
#         self.x = clamp(0, self.x, 1280)
#         self.y = clamp(100, self.y, 1115)
#         if self.attack == 1:
#             self.aver += 1
#
#     def draw(self):
#         elif self.jump == 1 and self.face_dir == -1:
#             self.image.clip_draw(75 + (self.jframe * 17), 236, 16, 36, self.x, self.y, 16 * 2.5, 36 * 2.5)
#         elif self.jump == 1 and self.face_dir == 1:
#             self.image.clip_draw(225 - (self.jframe * 17), 236, 16, 36, self.x, self.y, 16 * 2.5, 36 * 2.5)
#
#
# # def handle_events():
# #     # global running
# #     events = get_events()
# #     for event in events:
# #         if event.type == SDL_QUIT:
# #             game_framework.quit()
# #         elif event.type == SDL_KEYDOWN:
# #             match event.key:
# #                 case pico2d.SDLK_ESCAPE:
# #                     game_framework.change_state(title_state)
# #                 case pico2d.SDLK_LEFT:
# #                     nick.dir -= 1
# #                 case pico2d.SDLK_RIGHT:
# #                     nick.dir += 1
# #                 case pico2d.SDLK_LALT:
# #                     nick.jump = 1
# #                     delay(0.05)
# #                     nick.ver += 1
# #                 case pico2d.SDLK_LCTRL:
# #                     nick.attack = 1
# #                 case pico2d.SDLK_DOWN:
# #                     nick.ver -= 2
# #         elif event.type == SDL_KEYUP:
# #             match event.key:
# #                 case pico2d.SDLK_LEFT:
# #                     nick.dir += 1
# #                     nick.face_dir = -1
# #                 case pico2d.SDLK_RIGHT:
# #                     nick.dir -= 1
# #                     nick.face_dir = 1
# #                 case pico2d.SDLK_LALT:
# #                     nick.jump = 0
# #                     if nick.ver > 0:
# #                         nick.ver -= 1
# #                     else:
# #                         nick.ver = 0
# #                 case pico2d.SDLK_LCTRL:
# #                     nick.attack = 0
# #                     nick.aver = 0
# #                 case pico2d.SDLK_DOWN:
# #                     nick.ver += 2
#
#
# nick = None
# map = None
# running = True
# radDemon = None
#
#
# def enter():
#     global nick, map, running, redDemon
#     nick = Nick()
#     map = Map()
#     redDemon = RedDemon()
#     running = True
#
#
# def exit():
#     global nick, map, redDemon
#     del nick
#     del map
#     del redDemon
#
#
# def update():
#     nick.update()
#     redDemon.update()
#
#
# def draw():
#     clear_canvas()
#     map.draw()
#     nick.draw()
#     redDemon.draw()
#     update_canvas()