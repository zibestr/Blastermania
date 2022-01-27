import os
import pygame


# метод загрузки изображения
def load_image(name):
    fullname = os.path.join('D:\\git_lab3_lesson2\\Blastermania\\base\\core\\graphics\\ui', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        exit()
    image = pygame.image.load(fullname)
    return image


# класс реализующий интерфейс игрока
class HUD:
    def __init__(self, sizes, hero):
        self.surface = pygame.Surface((sizes[0], sizes[1])).convert_alpha()
        self.surface.fill([0, 0, 0, 0])
        self.health_ui = load_image('health_ui.png')
        self.heath_bar = None
        self.dodge_ui = load_image('dodge_icon.png')
        self.hero = hero

    # рендер полоски здоровья
    def health_bar(self):
        sizes = self.health_ui.get_rect().w, self.health_ui.get_rect().h
        scale = self.surface.get_width() / 4.0 / sizes[0]
        pygame.draw.rect(self.surface, pygame.Color(150, 0, 0), (10 + int(19 * scale), 20,
                                                                 int(self.hero.hp * sizes[0] / 5.3 * scale),
                                                                 int(sizes[1] / 2 * scale)))
        self.heath_bar = pygame.transform.scale(self.health_ui, (scale * sizes[0],
                                                                 scale * sizes[1]))
        self.surface.blit(self.heath_bar, (10, 10))

    # рендер иконки отката уклонения
    def dodge_icon(self):
        sizes = self.surface.get_width() * 0.05, self.surface.get_width() * 0.05
        dodge_surface = pygame.transform.scale(self.dodge_ui, sizes).convert_alpha()
        if self.hero.dodge_time != 0:
            dodge_surface.set_alpha(50)
            font = pygame.font.Font(None, 40)
            timer = font.render(str(round((self.hero.dodge_cooldown - self.hero.dodge_time) / 120, 1)), True,
                                (255, 255, 255))
            dodge_surface.blit(timer, (8, 8))

        self.surface.blit(dodge_surface,
                          (self.surface.get_width() * 0.05 + self.heath_bar.get_width(), 10))

    def render(self):
        self.health_bar()
        self.dodge_icon()
        return self.surface
