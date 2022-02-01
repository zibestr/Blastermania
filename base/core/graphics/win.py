import os
import pygame

pygame.font.init()


# класс реализующий меню паузы
class WinUI:
    def __init__(self, sizes):
        self.surface = pygame.Surface(sizes).convert_alpha()
        self.font1 = pygame.font.Font(f'{os.getcwd()}\\base\\core\\graphics\\fonts\\Pixeboy.ttf',
                                      self.surface.get_width() // 8)
        self.font1.underline = True
        self.font2 = pygame.font.Font(f'{os.getcwd()}\\base\\core\\graphics\\fonts\\Pixeboy.ttf',
                                      self.surface.get_width() // 28)
        self.text_color = pygame.Color(255, 225, 64)

    def render_title(self):
        title = self.font1.render('You Win!', True, self.text_color)
        advice = self.font2.render('Escape to exit', True, self.text_color)
        self.surface.blit(title, (self.surface.get_width() // 16 * 5,
                                  self.surface.get_height() // 2))
        self.surface.blit(advice, (self.surface.get_width() // 9 * 4 - self.surface.get_width() / 38.4,
                                   self.surface.get_height() // 3 * 2))

    def render(self):
        self.surface.fill([0, 0, 0, 100])
        self.render_title()
        return self.surface
