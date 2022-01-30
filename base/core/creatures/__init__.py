import pygame
import os


# метод загрузки изображения
def load_image(name, colorkey=None):
    fullname = os.path.join(f'{os.getcwd()}\\base\\core\\creatures\\sprites', name)
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


class ObjectLevel:
    def __init__(self, sizes, x, y):
        self.rect = pygame.Rect(x, y, *sizes)

    def draw(self, camera, color):
        if self.rect.colliderect(camera.rect):
            x = self.rect.x - camera.rect.x
            y = self.rect.y - camera.rect.y
            pygame.draw.rect(camera.rendering_surface.surface, color, (x, y, self.rect.width, self.rect.height))


# класс реализующий движущийся объект
class MovingObject(ObjectLevel):
    def __init__(self, sizes, x, y, speed):
        super().__init__(sizes, x, y)
        self.speed = pygame.Vector2(*speed)

    def draw(self, camera, color=pygame.Color('white')):
        super().draw(camera, color)

    def move(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        indexes = self.rect.collidelistall(list(filter(lambda x: x is not self, self.groups()[0].sprites())))
        for index in indexes:
            self.collision(self.groups()[0].sprites()[index])

    # функция коллизии
    def collision(self, collision_object):
        pass

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
                try:
                    if sprite.is_visible:
                        x = sprite.rect.x - camera.rect.x
                        y = sprite.rect.y - camera.rect.y
                        camera.rendering_surface.surface.blit(sprite.image, (x, y))
                except AttributeError:
                    x = sprite.rect.x - camera.rect.x
                    y = sprite.rect.y - camera.rect.y
                    camera.rendering_surface.surface.blit(sprite.image, (x, y))

    def update(self):
        for sprite in self.sprites():
            sprite.update()


# реализация статичного спрайта
class Sprite(pygame.sprite.Sprite):
    def __init__(self, image_name, colorkey, x, y, *group):
        super().__init__(*group)
        self.image = load_image(image_name, colorkey)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)


# реализация движущегося спрайта
class MovingSprite(Sprite, MovingObject):
    def __init__(self, image_name, colorkey, x, y, speed, *group):
        MovingObject.__init__(self, (0, 0), x, y, speed)
        Sprite.__init__(self, image_name, colorkey, x, y, *group)

    def update(self):
        self.move()


# реализация анимированного спрайта
class AnimatedSprite(MovingSprite):
    def __init__(self, image_name, columns, rows, x, y, speed, *group):
        super().__init__(image_name, None, x, y, speed, *group)
        # словарь в котором хранятся данные для анимации спрайтов
        # сигнатура элементов словаря: 'путь в спрайту', количество столбцов, количество строк
        self.spritesheets = dict()
        self.cur_spritesheet = None
        # фреймы анимации
        self.frames = list()
        self.cut_sheet(load_image(image_name), columns, rows)
        # фрейм в данный момент
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.limit = 20
        self.counter = 0

    # метод для смены анимаций
    # mirror отвечает за зеркальное отражение
    def update_animation(self, spritesheet, mirror=False):
        x, y = self.rect.x, self.rect.y
        self.frames = list()
        self.cut_sheet(load_image(spritesheet[0]), spritesheet[1], spritesheet[2], mirror=mirror)
        self.cur_spritesheet = spritesheet
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.limit = 15
        self.counter = 0

    # метод для разделения изображения на фреймы анимации
    # mirror отвечает за зеркальное отражение
    def cut_sheet(self, sheet, columns, rows, mirror=False):
        scale = 3.25
        width = sheet.get_width() // columns
        height = sheet.get_height() // rows
        self.rect = pygame.Rect(0, 0, width * scale, height * scale)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w // scale * i, self.rect.h // scale * j)
                self.frames.append(pygame.transform.flip(pygame.transform.scale(sheet.subsurface(pygame.Rect(
                    frame_location, (width, height))), (width * scale, height * scale)), mirror, False))

    def update(self):
        if self.counter == self.limit:
            self.counter = 0
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        else:
            self.counter += 1
        self.move()


# реализация класса с анимацией для бега
class RunningSprite(AnimatedSprite):
    # аргументы idle_spritesheet и run_spritesheet соответствуют сигнатуре словаря spritesheets
    def __init__(self, idle_spritesheet, run_spritesheet, x, y, speed, rooms, *group):
        super().__init__(*idle_spritesheet, x, y, speed, *group)
        # переменная в которой хранятся данные для анимации спрайтов
        self.spritesheets['run'] = run_spritesheet
        self.spritesheets['idle'] = idle_spritesheet
        self.update_animation(self.spritesheets['idle'])
        self.is_running = False
        self.direction = 1
        self.rooms = rooms
        self.is_collision = False

    def update(self):
        if self.is_running and self.cur_spritesheet != self.spritesheets['run'] or self.direction * self.speed[0] < 0:
            self.update_animation(self.spritesheets['run'], mirror=self.speed[0] < 0)
            try:
                self.direction = self.speed[0] / abs(self.speed[0])
            except ZeroDivisionError:
                self.direction = 1
        elif not self.is_running and self.cur_spritesheet != self.spritesheets['idle']:
            self.update_animation(self.spritesheets['idle'])
        super().update()

    def move(self):
        super().move()
        self.collide(self.rooms)

    def back(self):
        self.rect.x -= self.speed[0]
        self.rect.y -= self.speed[1]
        self.is_collision = True

    # функция коллизии со стенами
    def collide(self, objects):
        indexes = self.rect.collidelistall(list(map(lambda x: x.rect, objects)))
        if len(indexes) == 1:
            rect_room = objects[indexes[0]].rect
            if rect_room.x > self.rect.x or \
                    rect_room.y > self.rect.y or \
                    rect_room.bottom < self.rect.bottom or \
                    rect_room.right < self.rect.right:
                self.back()
            else:
                self.is_collision = False
        elif len(indexes) == 2:
            rect_room1 = objects[indexes[0]].rect
            rect_room2 = objects[indexes[1]].rect
            if rect_room1.y == rect_room2.bottom or rect_room1.bottom == rect_room2.y:
                if max(rect_room1.x, rect_room2.x) > self.rect.x or \
                        min(rect_room1.right, rect_room2.right) < self.rect.right:
                    self.back()
            elif rect_room1.x == rect_room2.right or rect_room1.right == rect_room2.x:
                if max(rect_room1.y, rect_room2.y) > self.rect.y or \
                        min(rect_room1.bottom, rect_room2.bottom) < self.rect.bottom:
                    self.back()
            else:
                self.is_collision = False
