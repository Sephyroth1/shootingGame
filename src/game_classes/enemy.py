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
        self.speed = 2

    def update(self):
        self.rect.y += self.speed

        if self.rect.left < 0:
            self.rect.left = 0
            self.speed = -self.speed
        if self.rect.right > 1280:
            self.rect.right = 1280
            self.speed = -self.speed
        if self.rect.top < 0:
            self.speed = -self.speed
        if self.rect.bottom > 720:
            self.rect.bottom = 720
            self.speed = -self.speed
