import pygame as pg


class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image_path = image_path
        self.x = x
        self.y = y
        self.image = pg.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
