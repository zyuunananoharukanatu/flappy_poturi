from random import randint

import pyxel


class App:
    def __init__(self):
        pyxel.init(160, 120, caption="Pyxel Jump")

        pyxel.load("assets/jump_game.pyxel")

        self.score = 0
        self.player_x = 36
        self.player_y = -16
        self.player_vy = 0
        self.player_is_alive = True

        self.far_cloud = [(-10, 75), (40, 65), (90, 60)]
        self.near_cloud = [(10, 25), (70, 35), (120, 15)]
        self.floor = [(i * 60, randint(8, 104), True) for i in range(4)]
        self.fruit = [(i * 60, randint(0, 104), randint(0, 2), True) for i in range(4)]

        pyxel.playm(0, loop=True)

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.update_player()

        for i, v in enumerate(self.floor):
            self.floor[i] = self.update_floor(*v)

        for i, v in enumerate(self.fruit):
            self.fruit[i] = self.update_fruit(*v)

    def update_player(self):
        # spaceでjump
        if self.player_is_alive and pyxel.btn(pyxel.KEY_SPACE) : 
            self.player_vy = min(self.player_vy, -4)

        self.player_y += self.player_vy
        self.player_vy = min(self.player_vy + 1, 5)

        if self.player_y > pyxel.height:
            if self.player_y > 600:
                self.score = 0
                self.player_x = 36
                self.player_y = -16
                self.player_vy = 0
                self.player_is_alive = True

    def update_floor(self, x, y, is_active):
        if is_active:
            if (
                self.player_x + 16 >= x
                and self.player_x <= x + 40
                and self.player_y + 16 >= y
                and self.player_y <= y + 8
                and self.player_vy > 0
            ):
                is_active = False
                pyxel.play(3, 3)
                if self.player_is_alive:
                    self.player_is_alive = False
                    pyxel.play(3, 5)
        else:
            y += 6

        x -= 4

        if x < -40:
            x += 240
            y = randint(8, 104)
            is_active = True

        return (x, y, is_active)

    def update_fruit(self, x, y, kind, is_active):
        if is_active and abs(x - self.player_x) < 12 and abs(y - self.player_y) < 12:
            is_active = False
            self.score += (kind + 1) * 100
            pyxel.play(3, 4)

        x -= 2

        if x < -40:
            x += 240
            y = randint(0, 104)
            kind = randint(0, 2)
            is_active = True

        return (x, y, kind, is_active)

    def draw(self):
        pyxel.cls(0)

        # draw sky
        pyxel.blt(0, 88, 0, 0, 120, 160, 32)

        # draw mountain
        pyxel.blt(0, 88, 0, 0, 64, 160, 24, 0)

        # draw small mountain
        offset = pyxel.frame_count % 160
        for i in range(2):
            pyxel.blt(i * 160 - offset, 104, 0, 0, 48, 160, 16, 0)

        # draw star
        offset = (pyxel.frame_count // 16) % 160
        for i in range(2):
            for x, y in self.far_cloud:
                pyxel.blt(x + i * 160 - offset, y, 0, 63, 31, 32, 24, 12)

        offset = (pyxel.frame_count // 8) % 160
        for i in range(2):
            for x, y in self.near_cloud:
                pyxel.blt(x + i * 160 - offset, y, 0, 0, 31, 56, 24, 12)

        # draw floors
        for x, y, is_active in self.floor:
            pyxel.blt(x, y, 0, 0, 16, 40, 8, 12)

        # draw fruits
        for x, y, kind, is_active in self.fruit:
            if is_active:
                pyxel.blt(x, y, 0, 32 + kind * 16, 0, 16, 16, 11)

        # draw player
        pyxel.blt(
            self.player_x,
            self.player_y,
            0,
            16 if self.player_vy > 0 else 0,
            0,
            16,
            16,
            11,
        )

        # draw score
        s = "SCORE {:>4}".format(self.score)
        pyxel.text(5, 4, s, 1)
        pyxel.text(4, 4, s, 7)


App()
