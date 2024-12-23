import pygame
import math

import Engine.Utils as Utils


class Bullet(pygame.sprite.Sprite):
    def __init__(self, engine, x, y, heading):
        super().__init__()
        self.engine = engine
        self.x = float(x)
        self.y = float(y)
        self.speed = 300
        self.heading = heading
        self.max_distance = 1200
        self.distance_traveled = 0

        # Get screen dimensions
        self.screen_width = self.engine.screen.get_width()
        self.screen_height = self.engine.screen.get_height()

        # Create a rectangle for the bullet
        self.original_image = pygame.Surface((3, 20), pygame.SRCALPHA)  # Width: 20, Height: 3
        self.original_image.fill((0, 0, 0))  # Fill color: black
        self.image = pygame.transform.rotate(self.original_image, -self.heading)  # Rotate clockwise
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(self.x, self.y))  # Initialize rect

    def update(self):
        # Calculate the change in position based on speed and heading
        radians = math.radians(self.heading)
        dx = self.speed * self.engine.tick * math.sin(radians) / 1000.0  # Change in x
        dy = -self.speed * self.engine.tick * math.cos(radians) / 1000.0  # Change in y (negative for y-axis)

        # Update the position
        self.x += dx
        self.y += dy

        Utils.wrap_around(self, self.screen_width, self.screen_height)

        # Update the distance traveled
        self.distance_traveled += self.speed * self.engine.tick / 1000.0

        # Update the rectangle's position based on the current position
        self.rect.center = (int(self.x), int(self.y))  # Update rect to new image location

        # Check for collision with obstacles
        obstacle = Utils.check_collision_with_group(self, self.engine.obstacles)
        if obstacle:
            self.engine.create_explosion(obstacle, self, 36, "explosion2")
            self.kill()  # Remove the bullet from all groups if it hits an obstacle

        # Check if the bullet has traveled its maximum distance
        if self.distance_traveled >= self.max_distance:
            self.kill()  # Remove the bullet from all groups

    def draw(self):
        self.engine.screen.blit(self.image, self.rect)  # Original position

        # Check for Bullet cutoff and draw on the opposite side
        if self.rect.left < 0:  # Left cutoff
            self.engine.screen.blit(self.image, self.rect.move(self.screen_width, 0))
        elif self.rect.right > self.screen_width:  # Right cutoff
            self.engine.screen.blit(self.image, self.rect.move(-self.screen_width, 0))

        if self.rect.top < 0:  # Top cutoff
            self.engine.screen.blit(self.image, self.rect.move(0, self.screen_height))
        elif self.rect.bottom > self.screen_height:  # Bottom cutoff
            self.engine.screen.blit(self.image, self.rect.move(0, -self.screen_height))
