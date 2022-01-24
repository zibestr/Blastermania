import os
from random import randint
from pygame.sprite import Sprite
from pygame.transform import scale
from pygame.image import load


# метод загрузки изображения
def load_image(name):
    fullname = os.path.join('D:\\git_lab3_lesson2\\Blastermania\\base\\core\\mapping\\tiles', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        exit()
    image = load(fullname)
    return image


class FloorTile(Sprite):
    def __init__(self, x, y, width, height, group):
        super().__init__(*group)
        self.image = scale(load_image(f'floor\\floor_{randint(1, 17)}.png'), (width, height))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
