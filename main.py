from random import random

import pyxel

SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAMEOVER = 2
SCENE_WIN = 3

STAR_COUNT = 20
STAR_COLOR_HIGH = 10
STAR_COLOR_LOW = 9

PLAYER_WIDTH = 8
PLAYER_HEIGHT = 11
PLAYER_SPEED = 5

BULLET_WIDTH = 2
BULLET_HEIGHT = 4
BULLET_COLOR = 11
BULLET_SPEED = 4

ENEMY_WIDTH = 8
ENEMY_HEIGHT = 8
ENEMY_SPEED = 1.5

MED_WIDTH = 8
MED_HEIGHT = 8
MED_SPEED = 1.0

MASK_WIDTH = 8
MASK_HEIGHT = 8
MASK_SPEED = 2

BLAST_START_RADIUS = 1
BLAST_END_RADIUS = 8
BLAST_COLOR_IN = 7
BLAST_COLOR_OUT = 10

HEALING_END_RADIUS = 8

enemy_list = []
bullet_list = []
blast_list = []
med_list = []
healing_list = []
mask_list = []


def update_list(list):
    for elem in list:
        elem.update()


def draw_list(list):
    for elem in list:
        elem.draw()


def cleanup_list(list):
    i = 0
    while i < len(list):
        elem = list[i]
        if not elem.alive:
            list.pop(i)
        else:
            i += 1


class Background:
    def __init__(self):
        self.star_list = []
        for i in range(STAR_COUNT):
            self.star_list.append(
                (random() * pyxel.width, random() * pyxel.height, random() * 1.5 + 1)
            )

    def update(self):
        for i, (x, y, speed) in enumerate(self.star_list):
            y += speed
            if y >= pyxel.height:
                y -= pyxel.height
            self.star_list[i] = (x, y, speed)

    def draw(self):
        for (x, y, speed) in self.star_list:
            pyxel.circ(x, y, 1, STAR_COLOR_HIGH if speed > 1.8 else STAR_COLOR_LOW)


class Player:
    def __init__(self, x, y, shield_enabled):
        self.x = x
        self.y = y
        self.w = PLAYER_WIDTH
        self.h = PLAYER_HEIGHT
        self.alive = True
        self.life = 100
        self.level = 1
        self.shield_enabled = shield_enabled

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= PLAYER_SPEED

        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += PLAYER_SPEED

        if pyxel.btn(pyxel.KEY_UP):
            self.y -= PLAYER_SPEED

        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += PLAYER_SPEED

        self.x = max(self.x, 0)
        self.x = min(self.x, pyxel.width - self.w)
        self.y = max(self.y, 0)
        self.y = min(self.y, pyxel.height - self.h)

        if pyxel.btnp(pyxel.KEY_SPACE):
            Bullet(
                self.x + (PLAYER_WIDTH - BULLET_WIDTH) / 2, self.y - BULLET_HEIGHT / 2, self.shield_enabled
            )

            pyxel.play(0, 0)
            if self.shield_enabled:
                self.shield_enabled = False

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 0, self.w, self.h, 0)


class Bullet:
    def __init__(self, x, y, shield_enabled):
        self.x = x
        self.y = y
        self.shield_enabled = shield_enabled
        if self.shield_enabled:
            self.w = 2000
            self.x = 0
        else:
            self.w = BULLET_WIDTH
        self.h = BULLET_HEIGHT
        self.alive = True

        bullet_list.append(self)

    def update(self):
        self.y -= BULLET_SPEED

        if self.y + self.h - 1 < 0:
            self.alive = False

    def draw(self):
        pyxel.rect(self.x, self.y, self.w, self.h, BULLET_COLOR)


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = ENEMY_WIDTH
        self.h = ENEMY_HEIGHT
        self.dir = 1
        self.alive = True
        self.offset = int(random() * 60)

        enemy_list.append(self)

    def update(self):
        if (pyxel.frame_count + self.offset) % 60 < 30:
            self.x += ENEMY_SPEED
            self.dir = 1
        else:
            self.x -= ENEMY_SPEED
            self.dir = -1

        self.y += ENEMY_SPEED

        if self.y > pyxel.height - 1:
            self.alive = False

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 8, 0, self.w * self.dir, self.h, 0)


class Med:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = MED_WIDTH
        self.h = MED_HEIGHT
        self.dir = 1
        self.alive = True
        self.offset = int(random() * 60)

        med_list.append(self)

    def update(self):
        if (pyxel.frame_count + self.offset) % 60 < 30:
            self.x += MED_SPEED
            self.dir = 1
        else:
            self.x -= MED_SPEED
            self.dir = -1

        self.y += MED_SPEED

        if self.y > pyxel.height - 1:
            self.alive = True

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 18, 0, self.w * self.dir, self.h, 0)


class Mask:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = MASK_WIDTH
        self.h = MASK_HEIGHT
        self.dir = 1
        self.alive = True
        self.offset = int(random() * 60)

        mask_list.append(self)

    def update(self):
        if (pyxel.frame_count + self.offset) % 60 < 30:
            self.x += MASK_SPEED
            self.dir = 1
        else:
            self.x -= MASK_SPEED
            self.dir = -1

        self.y += MASK_SPEED

        if self.y > pyxel.height - 1:
            self.alive = True

    def draw(self):
        pyxel.blt(self.x, self.y, 2, 19, 20, self.w * self.dir, self.h, 0)


class Blast:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = BLAST_START_RADIUS
        self.alive = True

        blast_list.append(self)

    def update(self):
        self.radius += 1

        if self.radius > BLAST_END_RADIUS:
            self.alive = False

    def draw(self):
        pyxel.circ(self.x, self.y, self.radius, BLAST_COLOR_IN)
        pyxel.circb(self.x, self.y, self.radius, BLAST_COLOR_OUT)


class Healing:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = BLAST_START_RADIUS
        self.alive = True

        healing_list.append(self)

    def update(self):
        self.radius += 1

        if self.radius > HEALING_END_RADIUS:
            self.alive = False

    def draw(self):
        pyxel.circ(self.x, self.y, self.radius, 11)
        pyxel.circb(self.x, self.y, self.radius, 7)


class App:
    def __init__(self):
        self.shield_enabled = False
        pyxel.init(120, 160, caption="Pyxel Shooter")
        pyxel.image(0).set(
            0,
            0,
            [
                "000d0000",
                "000d0000",
                "00d6d000",
                "00d6d000",
                "00dcd000",
                "0d755d00",
                "ddddddd0",
                "00a9a000",
                "000a0000",
            ],
        )

        pyxel.image(0).set(
            8,
            0,
            [
                "80202208",
                "02888820",
                "288ee882",
                "08e77e82",
                "28e77e80",
                "288ee882",
                "02888820",
                "80202208",
            ],
        )

        pyxel.image(0).set(
            18,
            0,
            [
                "00044000",
                "00666600",
                "00066000",
                "00600600",
                "06070060",
                "6b7bbbb6",
                "6bbbbbb6",
                "06666660",
            ],
        )
        pyxel.image(2).set(
            19,
            20,
            [
                "0000d0dd",
                "000dfd0d",
                "00df77d0",
                "0df777fd",
                "00d77fd0",
                "0d0dfd00",
                "0dd0d000",
            ],
        )

        define_sound_and_music()

        pyxel.playm(0, loop=True)
        pyxel.sound(0).set("a3a2c1a1", "p", "7", "s", 5)
        pyxel.sound(1).set("a3a2c2c2", "n", "7742", "s", 10)
        pyxel.sound(2).set("c1c1c1a3a3a3c1c1c1", "p", "7", "s", 5)

        self.scene = SCENE_TITLE
        self.score = 0
        self.background = Background()
        self.player = Player(pyxel.width / 2, pyxel.height - 20, self.shield_enabled)

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.background.update()

        if self.scene == SCENE_TITLE:
            self.update_title_scene()
        elif self.scene == SCENE_PLAY:
            self.update_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.update_gameover_scene()
        elif self.scene == SCENE_WIN:
            self.update_win_scene()

    def update_title_scene(self):
        if pyxel.btnp(pyxel.KEY_ENTER):
            self.scene = SCENE_PLAY

    def update_play_scene(self):
        try:
            if pyxel.frame_count % (10 - self.player.level) == 0:
                Enemy(random() * (pyxel.width - PLAYER_WIDTH), 0)
            if pyxel.frame_count % (50 - self.player.level) == 0:
                Med(random() * (pyxel.width - PLAYER_WIDTH), 0)
                Mask(random() * (pyxel.width - PLAYER_WIDTH), 0)
        except ZeroDivisionError:
            self.scene = SCENE_WIN

        for a in enemy_list:
            for b in bullet_list:
                if (
                        a.x + a.w > b.x
                        and b.x + b.w > a.x
                        and a.y + a.h > b.y
                        and b.y + b.h > a.y
                ):
                    a.alive = False
                    b.alive = False

                    blast_list.append(
                        Blast(a.x + ENEMY_WIDTH / 2, a.y + ENEMY_HEIGHT / 2)
                    )

                    pyxel.play(1, 1)

                    self.score += 10

        for med in med_list:
            if (
                    self.player.x + self.player.w > med.x
                    and med.x + med.w > self.player.x
                    and self.player.y + self.player.h > med.y
                    and med.y + med.h > self.player.y
            ):
                med.alive = False
                if self.player.life < 100:
                    self.player.life += 20

                healing_list.append(
                    Healing(
                        self.player.x + PLAYER_WIDTH / 2,
                        self.player.y + PLAYER_HEIGHT / 2,
                    )
                )

                pyxel.play(2, 2)

                self.score += 30
                self.player.level = int((self.score / 100))

        for mask in mask_list:
            if (
                    self.player.x + self.player.w > mask.x
                    and mask.x + mask.w > self.player.x
                    and self.player.y + self.player.h > mask.y
                    and mask.y + mask.h > self.player.y
            ):
                mask.alive = False
                pyxel.play(2, 2)

                self.shield_enabled = True
                self.player.shield_enabled = True

        for enemy in enemy_list:
            if (
                    self.player.x + self.player.w > enemy.x
                    and enemy.x + enemy.w > self.player.x
                    and self.player.y + self.player.h > enemy.y
                    and enemy.y + enemy.h > self.player.y
            ):
                enemy.alive = False
                self.player.life -= 20

                blast_list.append(
                    Blast(
                        self.player.x + PLAYER_WIDTH / 2,
                        self.player.y + PLAYER_HEIGHT / 2,
                    )
                )

                pyxel.play(1, 1)
                if self.player.life == 0:
                    self.scene = SCENE_GAMEOVER

        if self.player.life == 0:
            self.scene = SCENE_GAMEOVER
        self.player.update()
        update_list(bullet_list)
        update_list(enemy_list)
        update_list(med_list)
        update_list(blast_list)
        update_list(healing_list)
        update_list(mask_list)

        cleanup_list(enemy_list)
        cleanup_list(med_list)
        cleanup_list(bullet_list)
        cleanup_list(blast_list)
        cleanup_list(healing_list)
        cleanup_list(mask_list)

    def update_gameover_scene(self):
        update_list(bullet_list)
        update_list(enemy_list)
        update_list(blast_list)
        update_list(med_list)
        update_list(healing_list)
        update_list(mask_list)

        cleanup_list(enemy_list)
        cleanup_list(bullet_list)
        cleanup_list(blast_list)
        cleanup_list(med_list)
        cleanup_list(healing_list)
        cleanup_list(mask_list)

        if pyxel.btnp(pyxel.KEY_ENTER):
            self.scene = SCENE_PLAY
            self.player.x = pyxel.width / 2
            self.player.y = pyxel.height - 20
            self.score = 0
            self.player.level = 1

            enemy_list.clear()
            bullet_list.clear()
            blast_list.clear()
            healing_list.clear()
            mask_list.clear()


    def update_win_scene(self):
        update_list(bullet_list)
        update_list(enemy_list)
        update_list(blast_list)
        update_list(med_list)
        update_list(healing_list)
        update_list(mask_list)

        cleanup_list(enemy_list)
        cleanup_list(bullet_list)
        cleanup_list(blast_list)
        cleanup_list(med_list)
        cleanup_list(healing_list)
        cleanup_list(mask_list)

        if pyxel.btnp(pyxel.KEY_ENTER):
            self.scene = SCENE_PLAY
            self.player.x = pyxel.width / 2
            self.player.y = pyxel.height - 20
            self.score = 0
            self.player.level = 1

            enemy_list.clear()
            bullet_list.clear()
            blast_list.clear()
            healing_list.clear()
            mask_list.clear()

    def draw(self):
        if self.player.level == 7:
            pyxel.cls(14)
        elif self.player.level == 8:
            pyxel.cls(12)
        else:
            pyxel.cls(self.player.level)
        self.background.draw()

        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_PLAY:
            self.draw_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.draw_gameover_scene()
        elif self.scene == SCENE_WIN:
            self.draw_win_scene()

        pyxel.text(39, 4, "SCORE:{:5}".format(self.score), 7)
        pyxel.text(10, 12, "HEALTH:{:3}%".format(self.player.life), 7)
        self.draw_health()
        pyxel.text(75, 12, "LEVEL:{:3}".format(self.player.level), 7)

    def draw_health(self):
        pyxel.image(1).set(
            0,
            0,
            [
                "07700770",
                "78877887",
                "68866886",
                "06888860",
                "00688600",
                "00066000",
                "00000000",
                "00000000",
            ],
        )
        x = 10
        y = 20
        for life in range(self.player.life//20):
            pyxel.blt(x, y, 1, 0, 0, PLAYER_WIDTH, PLAYER_HEIGHT, 0)
            x += 10

    def draw_title_scene(self):
        pyxel.text(18, 66, "Hand Sanitiser Shooter", pyxel.frame_count % 10)
        pyxel.text(9, 75, "BLAST AWAY THE CORONAVIRUS", pyxel.frame_count % 12)
        pyxel.text(31, 126, "- PRESS ENTER -", 13)

    def draw_play_scene(self):
        self.player.draw()
        draw_list(bullet_list)
        draw_list(enemy_list)
        draw_list(blast_list)
        draw_list(healing_list)
        draw_list(med_list)
        draw_list(mask_list)

    def draw_gameover_scene(self):
        draw_list(bullet_list)
        draw_list(enemy_list)
        draw_list(blast_list)
        draw_list(med_list)
        draw_list(healing_list)
        draw_list(mask_list)

        pyxel.text(43, 66, "GAME OVER", 8)
        pyxel.text(7, 117, "KEEP A SAFE SOCIAL DISTANCE", 10)
        pyxel.text(31, 126, "- PRESS ENTER -", 13)

    def draw_win_scene(self):
        draw_list(bullet_list)
        draw_list(enemy_list)
        draw_list(blast_list)
        draw_list(med_list)
        draw_list(healing_list)
        draw_list(mask_list)

        pyxel.text(43, 66, "CONGRATULATIONS!", 8)
        pyxel.text(0, 117, "You have survived the pandemic.", 14)
        pyxel.text(31, 126, "- PRESS ENTER -", 13)

def define_sound_and_music():
    """Define sound and music."""

    # Sound effects
    pyxel.sound(0).set("a3a2c1a1", "p", "7", "s", 5)
    pyxel.sound(1).set("a3a2c2c2", "n", "7742", "s", 10)
    pyxel.sound(2).set("c1c1c1a3a3a3c1c1c1", "p", "7", "s", 5)

    # Music
    pyxel.sound(3).set(
        "r a1b1c2 b1b1c2d2 g2g2g2g2 c2c2d2e2" "f2f2f2e2 f2e2d2c2 d2d2d2d2 g2g2r r ",
        "s",
        "6",
        "nnff vfff vvvv vfff svff vfff vvvv svnn",
        25,
    )

    pyxel.sound(4).set(
        "c1g1c1g1 c1g1c1g1 b0g1b0g1 b0g1b0g1" "a0e1a0e1 a0e1a0e1 g0d1g0d1 g0d1g0d1",
        "t",
        "7",
        "n",
        25,
    )

    pyxel.sound(4).set(
        "f0c1f0c1 g0d1g0d1 c1g1c1g1 a0e1a0e1" "f0c1f0c1 f0c1f0c1 g0d1g0d1 g0d1g0d1",
        "t",
        "7",
        "n",
        25,
    )

    pyxel.music(0).set([3], [3], [3], [3])
    pyxel.music(1).set([4], [4], [4], [4])
    pyxel.music(2).set([5], [5], [5], [5])

App()
