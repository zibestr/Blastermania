import os
import pygame
from base.core.mapping.level_map import DungeonRoom
from base.core.creatures import RunningSprite


pygame.mixer.init()

sounds_path = f'{os.getcwd()}\\base\\music\\sounds'
hit_sound = pygame.mixer.Sound(os.path.join(sounds_path, 'hit.wav'))
hit_sound.set_volume(0.02)

slime_idle = ['slime\\slime_idle_spritesheet.png', 6, 1]
slime_run = ['slime\\slime_run_spritesheet.png', 6, 1]


class Slime(RunningSprite):
    def __init__(self, x, y, speed, rooms, ai, *group):
        super().__init__(slime_idle, slime_run, x, y, speed, rooms, *group)
        self.is_visible = True
        self.hp = 1
        self.attack = 1
        self.ai = ai
        self.start_x = x
        self.start_y = y
        index = self.rect.collidelist(list(filter(lambda elem: isinstance(elem, DungeonRoom), self.rooms)))
        self.start_room = list(filter(lambda elem: isinstance(elem, DungeonRoom), self.rooms))[index]

        # для интеллекта

    def update(self):
        if self.is_visible:
            self.ai.run(self, self.hero)
            super().update()

    def move(self):
        super().move()
        if self.speed.x != 0 or self.speed.y != 0:
            self.is_running = True
        else:
            self.is_running = False

    def get_damage(self, damage):
        if self.is_visible:
            self.hp -= damage
            hit_sound.play()
            self.hit_animation()
            if self.hp == 0:
                self.is_visible = False
                self.death_animation()

