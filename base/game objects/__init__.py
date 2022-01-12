from base.core.mapping.level_map import ObjectLevel


# класс для движущихся объектов
class MovingObject(ObjectLevel):
    def __init__(self, sizes, x, y, speed):
        super().__init__(sizes, x, y)
        self.speed = speed

    def move(self, delta_time):
        self.x += self.speed[0] * delta_time
        self.y += self.speed[1] * delta_time
