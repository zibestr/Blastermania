import pygame


# класс реализующий камеру
class Camera:
    def __init__(self, surface):
        self.sizes = surface.surface.get_size()
        # поверхность, на которой работает камера
        self.rendering_surface = surface
        # точка в которую направлена камера
        center = [self.rendering_surface.center[0],
                  self.rendering_surface.center[1]]
        x = center[0] - self.sizes[0] // 2
        y = center[1] - self.sizes[1] // 2
        self.rect = pygame.Rect(x, y, *self.sizes)

    # метод для движения камеры
    def move(self):
        delta = self.rendering_surface.hero.speed
        self.rect.x += delta[0]
        self.rect.y += delta[1]

    # рендарит поверхность для отрисовки с учётом масштаба
    def render_surface(self):
        self.rendering_surface.surface.fill(pygame.Color('black'))
        current_level = self.rendering_surface.current_level
        for obj in self.rendering_surface.levels[current_level].objects:
            obj.draw(self)
        return self.rendering_surface.surface
