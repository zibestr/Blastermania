from random import choice

from base.core.creatures import RunningSprite, Sprite
import pygame
import os

from base.core.creatures.entities import BulletItem, Potion, BulletProjectile

pygame.mixer.init()

hero_idle = ['hero\\knight_idle_spritesheet.png', 6, 1]
hero_run = ['hero\\knight_run_spritesheet.png', 6, 1]
# звуки для игрока
sounds_path = f'{os.getcwd()}\\base\\music\\sounds'
hit_sound = pygame.mixer.Sound(os.path.join(sounds_path, 'hit.wav'))
death_sound = pygame.mixer.Sound(os.path.join(sounds_path, 'death.wav'))
shoot_sounds = [pygame.mixer.Sound(os.path.join(sounds_path, 'shoot_1.wav')),
                pygame.mixer.Sound(os.path.join(sounds_path, 'shoot_1.wav'))]
open_chest_sound = pygame.mixer.Sound(os.path.join(sounds_path, 'open_chest.wav'))
dodge_sound = pygame.mixer.Sound(os.path.join(sounds_path, 'dodge.wav'))

volume = 0.02
hit_sound.set_volume(volume)
dodge_sound.set_volume(volume)
death_sound.set_volume(volume)
shoot_sounds[0].set_volume(volume)
shoot_sounds[1].set_volume(volume)
open_chest_sound.set_volume(volume)


# класс реализующий героя
class Hero(RunningSprite):
    def __init__(self, x, y, speed, rooms, game, group):
        super().__init__(hero_idle, hero_run, x, y, speed, rooms, group)
        self.hp = 4
        self.max_hp = 4
        # даёт бессмертие на полторы секунды, если игроку нанесли урон
        self.cooldown_damaged = 120 * 1.5
        self.time_damaged = 0
        self.is_alive = True

        # переменные дл патронов
        self.amount_bullets = 100
        self.max_bullets = 150

        # переменные, связанные с уклонением
        self.dodge_tick = 0
        self.dodge_limit = 30
        self.dodge_cooldown = 120 * 1.8
        self.dodge_time = 0
        self.dead_inside = False

        self.game = game

    def shoot(self, mouse_pos):
        if self.is_alive:
            bullet = BulletProjectile(self,
                                      self.game.game_surface.surface.get_rect().center,
                                      mouse_pos)
            choice(shoot_sounds).play()

    def dodge(self):
        if self.dodge_time == 0 and not self.is_collision:
            dodge_sound.play()
            self.dodge_tick = 1
            self.dodge_time = 1

    def move(self):
        if 0 < self.dodge_tick < self.dodge_limit and not self.is_collision:
            if abs(self.speed.x) < 2 * 3 and abs(self.speed.y) < 2 * 3:
                self.speed *= 3
            self.dodge_tick += 1
            self.dead_inside = True
        elif self.is_collision:
            self.speed *= 0
        elif self.dodge_limit < self.dodge_tick:
            self.speed /= 3
            self.dodge_tick = 0
            self.dead_inside = False
        else:
            self.dead_inside = False
        if self.dodge_time != 0:
            if self.dodge_time >= self.dodge_cooldown:
                self.dodge_time = 0
            else:
                self.dodge_time += 1
        super().move()

    def update(self):
        super().update()
        if 0 < self.time_damaged < self.cooldown_damaged:
            self.time_damaged += 1
        else:
            self.time_damaged = 0

    def get_damage(self, damage):
        if self.time_damaged == 0 and self.is_alive and not self.dead_inside:
            self.hp -= damage
            hit_sound.play()
            self.hit_animation()
            if self.hp == 0:
                self.is_alive = False
                death_sound.play()
                self.death_animation()
            self.time_damaged = 1

    def collision(self, collision_object):
        super().collision(collision_object)
        # коллизия с врагами
        try:
            if collision_object is not self and not isinstance(collision_object, BulletProjectile) \
                    and collision_object.is_visible:
                self.get_damage(collision_object.attack)
        except AttributeError:
            pass
        # коллизия с зельями
        try:
            if collision_object.is_visible and \
                    collision_object.pickable_timer == collision_object.pickable_time \
                    and self.hp != self.max_hp and \
                    isinstance(collision_object, Potion):
                collision_object.pick_up(self)
        except AttributeError:
            pass
        # коллизия с пулями
        try:
            if collision_object.is_visible and \
                    collision_object.pickable_timer == collision_object.pickable_time \
                    and self.max_bullets != self.amount_bullets and \
                    isinstance(collision_object, BulletItem):
                collision_object.pick_up(self)
        except AttributeError:
            pass
        # коллизия с сундуками
        try:
            if not collision_object.is_opened:
                collision_object.open()
        except AttributeError:
            pass
