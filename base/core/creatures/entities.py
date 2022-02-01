import math
import os
import pygame
from base.core.creatures import AnimatedSprite
from base.core.creatures.fly_creature import FlyingCreature
from base.core.creatures.slime import Slime
from base.core.creatures.goblin import Goblin

pygame.mixer.init()

sounds_path = f'{os.getcwd()}\\base\\music\\sounds'
open_sound = pygame.mixer.Sound(os.path.join(sounds_path, 'open_chest.wav'))
open_sound.set_volume(0.04)

pick_up_sound = pygame.mixer.Sound(os.path.join(sounds_path, 'pick_up.wav'))
pick_up_sound.set_volume(0.03)


class Chest(AnimatedSprite):
    def __init__(self, x, y, group):
        super().__init__('chest\\chest_spritesheet.png', 8, 1, x, y, [0, 0], group)
        self.container = None
        self.is_opened = False

    def open(self):
        open_sound.play()
        self.update_animation(['chest\\chest_open.png', 1, 1])
        self.container.is_visible = True
        self.is_opened = True


class PotionChest(Chest):
    def __init__(self, x, y, group):
        super().__init__(x, y, group)
        self.container = Potion(self.rect.x, self.rect.y, self.groups()[0])


class BulletChest(Chest):
    def __init__(self, x, y, group):
        super().__init__(x, y, group)
        self.container = BulletItem(self.rect.x, self.rect.y, self.groups()[0])


class Item(AnimatedSprite):
    def __init__(self, image, x, y, group):
        super().__init__(image, 1, 1, x, y, [0, 0], group)
        self.hp_heal = 1
        self.is_visible = False
        self.pickable_timer = 0
        self.pickable_time = 10

    def pick_up(self, hero):
        pass

    def update(self):
        super().update()
        if self.is_visible:
            if 0 <= self.pickable_timer < self.pickable_time:
                self.pickable_timer += 1


class Potion(Item):
    def __init__(self, x, y, group):
        super().__init__('potion\\potion_red.png', x, y, group)

    def pick_up(self, hero):
        if hero.is_alive:
            if self.rect.colliderect(hero.rect):
                pick_up_sound.play()
                hero.hp += self.hp_heal
                self.is_visible = False


class BulletItem(Item):
    def __init__(self, x, y, group):
        super().__init__('bullets\\spentshell.png', x, y, group)
        self.bullets = 50

    def pick_up(self, hero):
        if hero.is_alive:
            if self.rect.colliderect(hero.rect):
                pick_up_sound.play()
                hero.amount_bullets += self.bullets
                if hero.amount_bullets > hero.max_bullets:
                    hero.amount_bullets = hero.max_bullets
                self.is_visible = False


class BulletProjectile(AnimatedSprite):
    def __init__(self, hero, start_coords, shoot_coords):
        super().__init__('laser\\laser.png', 4, 1, hero.rect.x, hero.rect.y,
                         [0, 0], hero.groups()[0], scale=2)
        dx = shoot_coords[0] - start_coords[0]
        dy = shoot_coords[1] - start_coords[1]
        angle = math.atan2(dy, dx)
        self.speed = pygame.Vector2(5 * math.cos(angle),
                                    5 * math.sin(angle)) + hero.speed
        self.is_visible = True
        self.attack = 1
        self.rooms = hero.rooms

    # функция коллизии со стенами
    def collide(self, objects):
        indexes = self.rect.collidelistall(list(map(lambda x: x.rect, objects)))
        if len(indexes) == 1:
            rect_room = objects[indexes[0]].rect
            if rect_room.x > self.rect.x or \
                    rect_room.y > self.rect.y or \
                    rect_room.bottom < self.rect.bottom or \
                    rect_room.right < self.rect.right:
                self.is_visible = False
        elif len(indexes) == 2:
            rect_room1 = objects[indexes[0]].rect
            rect_room2 = objects[indexes[1]].rect
            if rect_room1.y == rect_room2.bottom or rect_room1.bottom == rect_room2.y:
                if max(rect_room1.x, rect_room2.x) > self.rect.x or \
                        min(rect_room1.right, rect_room2.right) < self.rect.right:
                    self.is_visible = False
            elif rect_room1.x == rect_room2.right or rect_room1.right == rect_room2.x:
                if max(rect_room1.y, rect_room2.y) > self.rect.y or \
                        min(rect_room1.bottom, rect_room2.bottom) < self.rect.bottom:
                    self.is_visible = False

    def damage(self):
        sprites = self.groups()[0].sprites()
        monsters = list(filter(lambda sprite: isinstance(sprite, Goblin) or
                                              isinstance(sprite, Slime) or
                                              isinstance(sprite, FlyingCreature),
                               sprites))
        index = self.rect.collidelist(list(map(lambda x: x.rect, monsters)))
        if index != -1 and monsters[index].is_visible:
            monsters[index].get_damage(self.attack)
            self.is_visible = False

    def move(self):
        if self.is_visible:
            super().move()
            self.collide(self.rooms)
            self.damage()
