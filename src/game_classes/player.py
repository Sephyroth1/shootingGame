import pygame as pg


class Player(pg.sprite.Sprite):
    def __init__(self, x, y, image_path, health=100):
        super().__init__()
        self.x = x
        self.y = y
        self.image_path = image_path
        self.image = pg.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        self.health = health

    def update(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.rect.x -= self.speed
        elif keys[pg.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pg.K_UP]:
            self.rect.y -= self.speed
        elif keys[pg.K_DOWN]:
            self.rect.y += self.speed

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 1280:
            self.rect.right = 1280
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 720:
            self.rect.bottom = 720
