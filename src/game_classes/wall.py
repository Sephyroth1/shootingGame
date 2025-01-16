import pygame as pg
import math


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
        self.speed = 2

    def update(self, ship):
        if ship is not None:
            dx = ship.x - self.x
            dy = ship.y - self.y

            distance = math.sqrt(dx**2 + dy**2)
            if distance != 0:
                dx /= distance
                dy /= distance

            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed
        else:
            print("Ship does not exist")
