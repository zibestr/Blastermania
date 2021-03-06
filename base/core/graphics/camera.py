import pygame


# класс реализующий камеру
class Camera:
    def __init__(self, surface):
        self.sizes = surface.surface.get_size()
        # поверхность, на которой работает камера
        self.rendering_surface = surface
        # точка в которую направлена камера
        center = self.rendering_surface.center
        x = center[0] - self.sizes[0] // 2
        y = center[1] - self.sizes[1] // 2
        self.rect = pygame.Rect(x, y, *self.sizes)

    # метод для движения камеры
    def move(self):
        if not self.rendering_surface.hero.is_collision and self.rendering_surface.hero.is_alive:
            delta = self.rendering_surface.hero.speed
            self.rect.x += delta.x
            self.rect.y += delta.y

    # рендарит поверхность для отрисовки с учётом масштаба
    def render_surface(self):
        self.rendering_surface.surface.fill(pygame.Color(25, 28, 49))
        # рисует сначала тайлы окружения, а потом существ
        self.rendering_surface.tiles_sprites.draw(self)
        self.rendering_surface.creatures_sprites.draw(self)

        return self.rendering_surface.surface
