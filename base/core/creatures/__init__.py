from base.core.mapping.level_map import ObjectLevel
import pygame
import os


# метод загрузки изображения
def load_image(name, colorkey=None):
    fullname = os.path.join('sprites', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# класс реализующий движущийся объект
class MovingObject(ObjectLevel):
    def __init__(self, sizes, x, y, speed=None):
        super().__init__(sizes, x, y)
        if speed is None:
            self.speed = [0, 0]
        else:
            self.speed = speed

    def draw(self, camera, color=pygame.Color('white')):
        super().draw(camera, color)

    def move(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

    # обновление объекта
    def update(self, camera):
        self.move()
        self.draw(camera)


# класс реализующий группы спрайтов для отрисовки камерой
class SpritesCameraGroup(pygame.sprite.Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)

    # рисует каждый спрайт группы
    def draw(self, camera):
        for sprite in self.sprites():
            if sprite.rect.colliderect(camera.rect):
                x = sprite.rect.x - camera.rect.x
                y = sprite.rect.y - camera.rect.y
                camera.rendering_surface.surface.blits(sprite.image, (x, y,
                                                                      sprite.rect.width, sprite.rect.height))

    def update(self, camera):
        self.draw(camera)


# реализация статичного спрайта
class Sprite(pygame.sprite.Sprite):
    def __init__(self, image_name, colorkey, x, y, *group):
        super().__init__(*group)
        self.image = load_image(image_name, colorkey)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)


# реализация движущегося спрайта
class MovingSprite(Sprite, MovingObject):
    def __init__(self, image_name, colorkey, x, y, speed=None, *group):
        super(MovingObject).__init__((0, 0), x, y, speed=speed)
        super(Sprite).__init__(image_name, colorkey, x, y, *group)

    def update(self, camera=None):
        self.move()


# реализация анимированного спрайта
class AnimatedSprite(MovingSprite):
    def __init__(self, image_name, colorkey, columns, rows, x, y, speed=None, *group):
        super(MovingSprite).__init__(image_name, colorkey, columns, rows, x, y, speed, *group)

        # фреймы анимации
        self.frames = list()
        self.cut_sheet(image_name, columns, rows)
        # фрейм в данный момент
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    # метод для разделения изображения на фреймы анимации
    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, camera=None):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.move()
