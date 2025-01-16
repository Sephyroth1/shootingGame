import pygame as pg
from game_classes.player import Player
from game_classes.laser import Laser
from game_classes.enemy import Enemy
from game_classes.wall import Wall
from PIL import Image
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
        self.font = pg.font.Font("assets/Bonus/kenvector_future_thin.ttf", 36)
        self.text = f"Score: {self.score}"
        self.text_position = (self.width - 225, 0)
        self.create_obstacles()
        self.create_enemies()

    def create_enemies(self):
        num_of_enemies = random.randint(0, 10)
        level_choice = [1, 2, 3, 4, 5]
        color_choice = ["Black", "Blue", "Green", "Red"]
        enemies_created = []
        for i in range(num_of_enemies):
            rand_level = random.choice(level_choice)
            rand_color = random.choice(color_choice)
            enemy_x = random.randint(0, 1280)
            enemy_y = random.randint(0, 720)
            enemy_width = Image.open(
                f"assets/PNG/Enemies/enemy{rand_color}{rand_level}.png"
            ).size[0]
            enemy_height = Image.open(
                f"assets/PNG/Enemies/enemy{rand_color}{rand_level}.png"
            ).size[1]

            overlap = False

            for enemy in enemies_created:
                enemyx, enemyy = enemy
                if (abs(enemyx - enemy_x) < enemy_width) and (
                    abs(enemyy - enemy_y) < enemy_height
                ):
                    overlap = True
                    break

            if overlap:
                i -= 1
                continue

        enemy = Enemy(
            enemy_x, enemy_y, f"assets/PNG/Enemies/enemy{rand_color}{rand_level}.png"
        )

        self.enemies.add(enemy)
        self.all_sprites.add(enemy)

    def create_obstacles(self):
        num_of_meteors = random.randint(0, 10)
        size_choice = ["big", "med", "small", "tiny"]
        color_choice = ["Grey", "Brown"]
        level_choice = [1, 2]
        meteors_created = []  # List to keep track of meteor positions

        for i in range(num_of_meteors):
            rand_size = random.choice(size_choice)
            if rand_size == "big":
                level_choice = [1, 2, 3, 4]
            else:
                level_choice = [1, 2]
            rand_color = random.choice(color_choice)
            rand_level = random.choice(level_choice)

            # Randomize x and y positions
            wall_x = random.randint(0, 1280)  # Random x position
            wall_y = random.randint(0, 720)  # Random y position
            meteor_width = Image.open(
                f"assets/PNG/Meteors/meteor{rand_color}_{rand_size}{rand_level}.png"
            ).size[
                0
            ]  # You can adjust this according to your meteor image size
            meteor_height = Image.open(
                f"assets/PNG/Meteors/meteor{rand_color}_{rand_size}{rand_level}.png"
            ).size[1]
            overlap = False
            for existing_wall in meteors_created:
                # Check if the new meteor is too close to any existing meteor
                existing_x, existing_y = existing_wall
                if (abs(existing_x - wall_x) < meteor_width) and (
                    abs(existing_y - wall_y) < meteor_height
                ):
                    overlap = True
                    break

            # If overlap is detected, try again by randomizing positions
            if overlap:
                i -= 1  # Retry creating this meteor, decrement counter
                continue

            # If no overlap, create the meteor and add it to the list
            wall = Wall(
                wall_x,
                wall_y,
                f"assets/PNG/Meteors/meteor{rand_color}_{rand_size}{rand_level}.png",
            )
            meteors_created.append((wall_x, wall_y))  # Add the position to the list
            self.meteors.add(wall)

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
            self.meteors.update(self.ship)
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
                if self.ship.rect.colliderect(wall):
                    self.ship.kill()

            self.text = f"Score: {self.score}"
            text_surface = self.font.render(self.text, True, (255, 255, 255))
            for x in range(0, self.screen.get_width(), self.background.get_width()):
                for y in range(
                    0, self.screen.get_height(), self.background.get_height()
                ):
                    self.screen.blit(self.background, (x, y))
            self.screen.blit(text_surface, self.text_position)
            self.meteors.draw(self.screen)
            self.all_sprites.draw(self.screen)
            pg.display.flip()
            self.clock.tick(60)
        pg.quit()


if __name__ == "__main__":
    game = Game(1280, 720)
    game.run()
