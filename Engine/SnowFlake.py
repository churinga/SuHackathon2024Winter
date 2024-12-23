import pygame
import random
import math

class SnowFlake(pygame.sprite.Sprite):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine

        # Load the snowflake image
        self.image = pygame.image.load("images/snow_flake.png").convert_alpha()
        self.image.set_alpha(random.randint(80, 200))

        # Randomly scale the image
        scale_factor = random.randint(30, 150) / self.image.get_width()
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * scale_factor), int(self.image.get_height() * scale_factor)))
        self.wind_direction = 0  # change wind direction every 1000 ticks
        self.speed_x = 0.0
        self.speed_y = 0.5
        self.max_speed = 0.25
        self.acceleration = 0.001
        self.counter = 0

        # Initialize position randomly on the screen
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, self.engine.screen.get_width() - self.rect.width)
        self.rect.y = random.randint(0, self.engine.screen.get_height() - self.rect.height)

        self.x = self.rect.x
        self.y = self.rect.y

    def update(self):
        # Randomly move the snowflake to a nearby position
        if self.counter % 1000 == 0:
            self.wind_direction = random.choice([-1, 0, 1])
        self.speed_x = self.speed_x + self.acceleration * self.wind_direction
        if self.speed_x > self.max_speed:
            self.speed_x = self.max_speed
        elif self.speed_x < -self.max_speed:
            self.speed_x = -self.max_speed
        move_x = random.random() * self.speed_x
        move_y = random.random() * self.speed_y
        self.x += move_x
        self.y += move_y
        self.counter += 1

        # Update position
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if self.rect.y > self.engine.screen.get_height():
            self.rect.y = -self.rect.height
            self.y = self.rect.y

        if self.rect.x > self.engine.screen.get_width():
            self.rect.x = -self.rect.width
            self.x = self.rect.x
        elif self.rect.x < -self.rect.width:
            self.rect.x = self.engine.screen.get_width() + self.rect.width
            self.x = self.rect.x

    def draw(self):
        # Draw the snowflake on the screen
        self.engine.screen.blit(self.image, self.rect.topleft)