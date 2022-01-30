from base.core.creatures import AnimatedSprite, load_image


class Chest(AnimatedSprite):
    def __init__(self, x, y, group):
        super().__init__('chest\\chest_spritesheet.png', 8, 1, x, y, [0, 0], group)
        self.container = Potion(self.rect.x, self.rect.y, self.groups()[0])

    def open(self):
        open_chest = OpenChest(self.rect.x, self.rect.y, self.groups()[0])
        self.groups()[0].add(open_chest)
        self.container.is_visible = True
        del self


class OpenChest(AnimatedSprite):
    def __init__(self, x, y, group):
        super().__init__('chest\\chest_open.png', 1, 1, x, y, [0, 0], group)


class Potion(AnimatedSprite):
    def __init__(self, x, y, group):
        super().__init__('potion\\potion_red.png', 1, 1, x, y, [0, 0], group)
        self.hp_heal = 1
        self.is_visible = False
        self.pickable_timer = 0
        self.pickable_time = 5

    def pick_up(self, hero):
        if self.rect.colliderect(hero.rect):
            hero.hp += self.hp_heal
            del self

    def update(self):
        super().update()
        if self.is_visible:
            if 0 <= self.pickable_timer < self.pickable_time:
                self.pickable_timer += 1
