from pico2d import *
import game_world

class Attack:
    image = None

    def __init__(self, x = 400, y = 300, velocity = 1):
        if Attack.image == None:
            Attack.image = load_image('Nick.png')
        self.x, self.y, self.velocity = x, y, velocity

    def draw(self):
        # self.image.draw(self.x, self.y)
        self.image.clip_draw(26, 200, 15, 23, self.x, self.y, 15, 23 * 2.5)

    def update(self):
        self.x += self.velocity

        if self.x < 25 or self.x > 1280 - 25:
            game_world.remove_object(self)


        # if self.attack == 1 and self.face_dir == -1:
        #     self.image.clip_draw(26 - (self.aframe * 25), 200, 15 + (self.aframe * 9), 23, self.x, self.y, 15 + (self.aframe * 9) * 2.5, 23 * 2.5)
        #     self.image.clip_draw(109 + (self.aframe * 9), 200, 8, 23, self.x - (self.aver), self.y, 8 * 2.5, 23 * 2.5)
        # elif self.attack == 1 and self.face_dir == 1:
        #     self.image.clip_draw(274 + (self.aframe * 17), 200, 15 + (self.aframe * 9), 23, self.x, self.y,  15 + (self.aframe * 9) * 2.5, 23 * 2.5)
        #     self.image.clip_draw(190 + (self.aframe * 9), 200, 8, 23, self.x + (self.aver), self.y, 8 * 2.5, 23 * 2.5)