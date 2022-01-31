import os
import pygame
from base.core.creatures import AnimatedSprite

pygame.mixer.init()

sounds_path = f'{os.getcwd()}\\base\\music\\sounds'
open_sound = pygame.mixer.Sound(os.path.join(sounds_path, 'open_chest.wav'))
open_sound.set_volume(0.04)

pick_up_sound = pygame.mixer.Sound(os.path.join(sounds_path, 'pick_up.wav'))
pick_up_sound.set_volume(0.03)


class Chest(AnimatedSprite):
    def __init__(self, x, y, group):
        super().__init__('chest\\chest_spritesheet.png', 8, 1, x, y, [0, 0], group)
        self.container = Potion(self.rect.x, self.rect.y, self.groups()[0])
        self.is_opened = False

    def open(self):
        open_sound.play()
        self.update_animation(['chest\\chest_open.png', 1, 1])
        self.container.is_visible = True
        self.is_opened = True


class Potion(AnimatedSprite):
    def __init__(self, x, y, group):
        super().__init__('potion\\potion_red.png', 1, 1, x, y, [0, 0], group)
        self.hp_heal = 1
        self.is_visible = False
        self.pickable_timer = 0
        self.pickable_time = 10

    def pick_up(self, hero):
        if hero.is_alive:
            if self.rect.colliderect(hero.rect):
                pick_up_sound.play()
                hero.hp += self.hp_heal
                self.is_visible = False

    def update(self):
        super().update()
        if self.is_visible:
            if 0 <= self.pickable_timer < self.pickable_time:
                self.pickable_timer += 1


def Bullet(AnimatedSprite):
    # self.speed = pygame.Vector2(x_курсора - x_игрока, y_курсора - y_игрока).scale_to_length(скорость_пули)
    pass
