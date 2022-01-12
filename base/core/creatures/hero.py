from base.core.creatures import AnimatedSprite


# класс реализующий героя
class Hero(AnimatedSprite):
    def __init__(self, image_name, colorkey, columns, rows, x, y, speed=None, *group):
        super().__init__(image_name, colorkey, columns, rows, x, y, speed, *group)
