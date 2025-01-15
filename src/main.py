import pygame as pg
from game_classes.player import Player
from game_classes.laser import Laser
from game_classes.enemy import Enemy
from game_classes.wall import Wall
import random


class Game:
    def __init__(self, width, height):
        pg.init()
        self.screen = pg.display.set_mode((width, height))
        self.width = width
        self.height = height
        self.clock = pg.time.Clock()
        self.all_sprites = pg.sprite.Group()
        self.ship = Player(
            self.width // 2, self.height // 2, "assets/PNG/playerShip1_blue.png"
        )
        self.score = 0
        self.all_sprites.add(self.ship)
        self.projectiles = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.meteors = pg.sprite.Group()
        self.running = True
        self.shoot_delay = 500
        self.last_shoot_time = 0
        self.background = pg.image.load("assets/Backgrounds/black.png")
        self.font = pg.font.Font("assets/Bonus/kenvector_future.ttf", 36)
        self.text = f"Score: {self.score}"
        self.text_position = (self.width - 225, 0)
        self.create_obstacles()
        for i in range(3):
            enemy = Enemy(100 + i * 150, 100, "assets/PNG/Enemies/enemyBlack1.png")
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)

    def create_obstacles(self):
        for i in range(5):
            wall_x = random.randint(0, 1280)
            wall_y = random.randint(0, 720)
            wall_rect = pg.Rect(wall_x, wall_y, 43, 43)
            for sprite in self.all_sprites:
                if not sprite.rect.colliderect(wall_rect):
                    wall = Wall(
                        wall_x, wall_y, "assets/PNG/Meteors/meteorBrown_med1.png"
                    )
                    self.meteors.add(wall)
                    self.all_sprites.add(wall)

    def run(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
            current_time = pg.time.get_ticks()
            if self.ship not in self.all_sprites:
                self.running = False
            keys = pg.key.get_pressed()

            if (
                keys[pg.K_SPACE]
                and current_time - self.last_shoot_time > self.shoot_delay
            ):
                l = Laser(
                    self.ship.rect.x,
                    self.ship.rect.y,
                    "assets/PNG/Lasers/laserBlue01.png",
                )
                self.last_shoot_time = current_time
                self.projectiles.add(l)
                self.all_sprites.add(l)
            self.all_sprites.update()

            for proj in self.projectiles:
                if pg.sprite.spritecollide(proj, self.enemies, True):
                    self.score += 1
                    proj.kill()

            for enemy in self.enemies:
                if self.ship.rect.colliderect(enemy):
                    self.ship.kill()
                    enemy.kill()

            for wall in self.meteors:
                if pg.sprite.spritecollide(wall, self.projectiles, True):
                    proj.kill()

            self.text = f"Score: {self.score}"
            text_surface = self.font.render(self.text, True, (255, 255, 255))
            for x in range(0, self.screen.get_width(), self.background.get_width()):
                for y in range(
                    0, self.screen.get_height(), self.background.get_height()
                ):
                    self.screen.blit(self.background, (x, y))
            self.screen.blit(text_surface, self.text_position)
            self.all_sprites.draw(self.screen)
            pg.display.flip()
            self.clock.tick(60)
        pg.quit()


if __name__ == "__main__":
    game = Game(1280, 720)
    game.run()
