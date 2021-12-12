import pygame


# класс реализующий камеру
class Camera:
    def __init__(self, surface):
        self.sizes = surface.surface.get_size() * 1
        # поверхность, на которой работает камера
        self.rendering_surface = surface
        # коэффициент масштабирования изображения
        self.scale = 5.5
        # точка в которую направлена камера
        self.center = list(self.rendering_surface.center)

    @property
    def x(self):
        return self.center[0] - self.sizes[0] // 2

    @property
    def y(self):
        return self.center[1] - self.sizes[1] // 2

    # рендарит поверхность для отрисовки с учётом масштаба
    def render_scale_surface(self):
        self.rendering_surface.surface.fill(pygame.Color('black'))
        current_level = self.rendering_surface.current_level
        for obj in self.rendering_surface.levels[current_level].objects:
            obj.draw(self)
        return self.rendering_surface.surface

    # изменить масштаб
    def get_scale(self, scale):
        if 5.0 <= scale <= 6.0:
            self.scale = scale
