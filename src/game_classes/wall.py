import pygame as pg


class Wall(pg.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.x = x
        self.y = y
        self.image_path = image_path
        self.image = pg.image.load(self.image_path)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
