import os

import pygame

pygame.font.init()


# класс реализующий меню паузы
class MenuUI:
    def __init__(self, sizes, game):
        self.surface = pygame.Surface(sizes).convert_alpha()
        self.game = game
        self.font = pygame.font.Font(f'{os.getcwd()}\\base\\core\\graphics\\fonts\\Pixeboy.ttf',
                                     self.surface.get_width() // 20)
        self.button_color = pygame.Color(82, 122, 222)
        self.text_color = pygame.Color('white')
        self.buttons = dict()
        self.create_start_buttons()

    def create_start_buttons(self):
        button_sizes = (self.surface.get_width() // 3, self.surface.get_height() // 7)
        # кнопка Continue
        self.buttons['continue'] = pygame.Rect(button_sizes[0], 2 * button_sizes[1],
                                               *button_sizes)
        # кнопка Options
        self.buttons['music'] = pygame.Rect(button_sizes[0], 3 * button_sizes[1] + button_sizes[1] // 3,
                                            *button_sizes)
        # кнопка Exit
        self.buttons['exit'] = pygame.Rect(button_sizes[0], 4 * button_sizes[1] + 2 * button_sizes[1] // 3,
                                           *button_sizes)

    def render_start_page(self):
        button_sizes = (self.surface.get_width() // 3, self.surface.get_height() // 7)
        pause_title = self.font.render('Pause', True, self.text_color)
        self.surface.blit(pause_title, (button_sizes[0] * 4 // 3, button_sizes[1]))
        # кнопка Continue
        pygame.draw.rect(self.surface,
                         self.button_color,
                         self.buttons['continue'],
                         border_radius=button_sizes[0] // 15)
        continue_title = self.font.render('Continue', True, self.text_color)
        self.surface.blit(continue_title, (button_sizes[0] * 5 // 4,
                                           2 * button_sizes[1] + button_sizes[1] // 3))
        # кнопка Options
        pygame.draw.rect(self.surface,
                         self.button_color,
                         self.buttons['music'],
                         border_radius=button_sizes[0] // 15)
        if self.game.is_music:
            title = 'Music On'
        else:
            title = 'Music Off'
        options_title = self.font.render(title, True, self.text_color)
        self.surface.blit(options_title, (button_sizes[0] * 14 // 11,
                                          3 * button_sizes[1] + 2 * button_sizes[1] // 3))
        # кнопка Exit
        pygame.draw.rect(self.surface,
                         self.button_color,
                         self.buttons['exit'],
                         border_radius=button_sizes[0] // 15)
        exit_title = self.font.render('Exit', True, self.text_color)
        self.surface.blit(exit_title, (button_sizes[0] * 15 // 11,
                                       4 * button_sizes[1] + 3 * button_sizes[1] // 3))

    def render(self):
        self.surface.fill([0, 0, 0, 150])
        self.render_start_page()
        return self.surface
