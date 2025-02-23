from random import randint

import pyxel


class App:
    def __init__(self):
        pyxel.init(160, 120, title="Pyxel Jump")

        pyxel.load("assets/jump_game.pyxres")

        # プレイヤー関連
        self.score = 0
        self.game_over_frame = 0
        self.player_x = 36
        self.player_y = -16
        self.player_vy = 0
        self.player_is_alive = True

        # ジャンプ関連
        self.jump_gauge = 20
        self.jump_start_time = 0

        # オブジェクト関連
        self.upper_star = [(-10, 75), (40, 65), (90, 60)]
        self.downer_star = [(10, 25), (70, 35), (120, 15)]
        self.obstacle = [(i * 60, randint(8, 104), True) for i in range(4)]
        self.water = [(i * 60, randint(0, 104), randint(0, 2), True) for i in range(4)]

        pyxel.playm(0, loop=True)

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.update_player()

        pyxel.rect(100,100,130,130,12)

        for i, v in enumerate(self.obstacle):
            self.obstacle[i] = self.update_obstacle(*v)

        for i, v in enumerate(self.water):
            self.water[i] = self.update_water(*v)

    def update_player(self):
        # spaceでjump
        if self.jump_gauge > 0 and self.player_is_alive and pyxel.btn(pyxel.KEY_SPACE) : 
            self.player_vy = min(self.player_vy, -4)
            if self.jump_start_time == 0:
                self.jump_start_time = pyxel.frame_count
                self.jump_gauge -= 1

            elif (pyxel.frame_count - self.jump_start_time) > 7:
                self.jump_gauge -= 1
                self.jump_start_time = pyxel.frame_count

        else :
            self.jump_start_time = 0

        self.player_y += self.player_vy
        self.player_vy = min(self.player_vy + 1, 5)
        self.score = (pyxel.frame_count - self.game_over_frame) // 10

        if self.player_y > pyxel.height:
            if self.player_y > 600:
                self.score = 0
                self.game_over_frame = pyxel.frame_count
                self.jump_gauge = 20
                self.player_x = 36
                self.player_y = -16
                self.player_vy = 0
                self.player_is_alive = True

    def update_obstacle(self, x, y, is_active):
        if is_active:
            if (
                self.player_x + 15 >= x
                and self.player_x <= x + 9
                and self.player_y + 15 >= y
                and self.player_y <= y + 9
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

    def update_water(self, x, y, size, is_active):
        if is_active and abs(x - self.player_x) < 12 and abs(y - self.player_y) < 12:
            is_active = False
            pyxel.play(3, 4)
            self.jump_gauge = min(self.jump_gauge + size + 1, 20)

        x -= 2

        if x < -40:
            x += 240
            y = randint(0, 104)
            size = randint(0, 2)
            is_active = True

        return (x, y, size, is_active)

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
            for x, y in self.upper_star:
                pyxel.blt(x + i * 160 - offset, y, 0, 63, 31, 32, 12, 12)

        offset = (pyxel.frame_count // 8) % 160
        for i in range(2):
            for x, y in self.downer_star:
                pyxel.blt(x + i * 160 - offset, y, 0, 0, 31, 56, 12, 12)

        # draw obstacle
        for x, y, is_active in self.obstacle:
            pyxel.blt(x, y, 0, 0, 16, 8, 8, 12)

        # draw water
        for x, y, size, is_active in self.water:
            if is_active:
                pyxel.blt(x, y, 0, 32 + size * 16, 0, 16, 16, 11)

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

        for i in range(0, self.jump_gauge):
            pyxel.rect(4, 80 - (4 * i), 5, 4, 12)
        
        for i in range(self.jump_gauge, 20):
            pyxel.rectb(4, 80 - (4 * i), 5, 4, 12)


App()
