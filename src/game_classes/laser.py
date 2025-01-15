import pygame as pg


class Laser(pg.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = 5
        self.image_path = image_path
        self.image = pg.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.rect.y -= self.speed
