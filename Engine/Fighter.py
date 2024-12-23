import pygame
import math
import time

import Engine.Utils as Utils


class Fighter(pygame.sprite.Sprite):
    def __init__(self, engine, image_file: str, top_speed: float, min_speed: float, curr_speed: float, acceleration: float,
                 turn_speed: float, max_ammo: int, curr_ammo: int, ammo_regen_time: int, 
                 ammo_fire_delay: float, x: float, y: float, turning: int, heading: float):
        super().__init__()
        self.engine = engine
        self.image_file = image_file  # String pointing to the image file path
        self.image = pygame.image.load(self.image_file)  # Load the image file
        self.image = pygame.transform.scale(self.image, (80, 80))  # Scale the loaded image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.top_speed = top_speed  # Maximum speed of the fighter plane
        self.min_speed = min_speed  # Minimum speed of the fighter plane
        self.curr_speed = curr_speed  # Current moving speed
        self.acceleration = acceleration  # How fast it accelerates or decelerates per sec
        self.turn_speed = turn_speed  # Fixed turning speed in degrees/sec
        self.max_ammo = max_ammo  # Maximum ammo capacity
        self.curr_ammo = curr_ammo  # Current ammo available
        self.ammo_regen_time = ammo_regen_time  # Time in seconds to regenerate one ammo
        self.ammo_fire_delay = ammo_fire_delay  # Delay in seconds between firing two ammo
        self.prev_ammo_fire_ts = 0  # The timestamp of when ammo was last fired
        self.prev_ammo_regen_ts = time.time()  # The timestamp of when ammo was last regenerated
        self.x = x  # Current x-coordinate on screen
        self.y = y  # Current y-coordinate on screen
        self.turning = turning  # 0: not turning, 1: clockwise, -1: counterclockwise
        self.heading = heading  # Current heading (angle in degrees with the y-axis)

        # Get screen dimensions
        self.screen_width = self.engine.screen.get_width()
        self.screen_height = self.engine.screen.get_height()

        self.killed = False

    def update(self):
        # Calculate movement based on heading and speed
        self.x += self.curr_speed * math.sin(math.radians(self.heading)) * (
                    self.engine.tick / 1000.0)
        self.y -= self.curr_speed * math.cos(math.radians(self.heading)) * (
                    self.engine.tick / 1000.0)

        # Adjust heading based on turning state
        if self.turning == 1:
            self.heading += self.turn_speed * (self.engine.tick / 1000.0)  # Clockwise
        elif self.turning == -1:
            self.heading -= self.turn_speed * (self.engine.tick / 1000.0)  # Counterclockwise

        # Keep heading within 0-360 degrees
        self.heading %= 360

        # Wrap around the screen edges
        Utils.wrap_around(self, self.screen_width, self.screen_height)

        # Update ammo regen
        if self.curr_ammo < self.max_ammo:
            if time.time() - self.prev_ammo_regen_ts > self.ammo_regen_time:
                self.curr_ammo += 1
                self.prev_ammo_regen_ts = time.time()
        else:
            self.prev_ammo_regen_ts = time.time()

    def wrap_around(self,):
        # Wrap fighter around the screen edges
        if self.x < 0:
            self.x = self.screen_width
        elif self.x > self.screen_width:
            self.x = 0

        if self.y < 0:
            self.y = self.screen_height
        elif self.y > self.screen_height:
            self.y = 0

    def create_wrapped_mask(self, image_rotated):
        # Assuming at least one of self.rect.left|right|top|bottom is out of range.
        left1 = self.rect.left
        right1 = self.rect.right
        top1 = self.rect.top
        bottom1 = self.rect.bottom
        left2 = self.rect.left
        right2 = self.rect.right
        top2 = self.rect.top
        bottom2 = self.rect.bottom

        if self.rect.left < 0:
            left2 += self.screen_width
            right2 += self.screen_width
        elif self.rect.right > self.screen_width:
            left1 -= self.screen_width
            right1 -= self.screen_width
        if self.rect.top < 0:
            top2 += self.screen_height
            bottom2 += self.screen_height
        elif self.rect.bottom > self.screen_height:
            top1 -= self.screen_height
            bottom1 -= self.screen_height
        mask = pygame.mask.from_surface(image_rotated)
        merged_mask = pygame.Mask((right2 - left1, bottom2 - top1))
        merged_mask.draw(mask, (0, 0))
        merged_mask.draw(mask, (left2 - left1, top2 - top1))
        return merged_mask

    def draw(self):
        if self.killed:
            return

        # Display Fighter
        image_rotated = pygame.transform.rotate(self.image, -self.heading)
        self.mask = pygame.mask.from_surface(image_rotated)
        self.rect = image_rotated.get_rect(center=(self.x, self.y))
        self.engine.screen.blit(image_rotated, self.rect)

        # Check for JetFighter cutoff and draw on the opposite side
        wrapped = False
        if self.rect.left < 0:  # Left cutoff
            self.engine.screen.blit(image_rotated, self.rect.move(self.screen_width, 0))
            wrapped = True
        elif self.rect.right > self.screen_width:  # Right cutoff
            self.engine.screen.blit(image_rotated, self.rect.move(-self.screen_width, 0))
            wrapped = True

        if self.rect.top < 0:  # Top cutoff
            self.engine.screen.blit(image_rotated, self.rect.move(0, self.screen_height))
            wrapped = True
        elif self.rect.bottom > self.screen_height:  # Bottom cutoff
            self.engine.screen.blit(image_rotated, self.rect.move(0, -self.screen_height))
            wrapped = True

        if wrapped:
            self.mask = self.create_wrapped_mask(image_rotated)

    def kill(self):
        self.killed = True

    def get_tip_coord(self):
        # Calculate the tip position (assuming the tip is at the front of the fighter) based on the current heading
        heading_radians = math.radians(self.heading)
        fighter_height = self.image.get_height()
        tip_x = self.x + (fighter_height / 2 + 10.0) * math.sin(heading_radians)
        tip_y = self.y - (fighter_height / 2 + 10.0) * math.cos(heading_radians)
        return tip_x, tip_y

class JetFighter(Fighter):
    def __init__(self, engine):
        super().__init__(
            engine,
            image_file="images/jetfighter.png",
            top_speed=200.0,
            min_speed=60.0,
            curr_speed=120.0,
            acceleration=5,
            turn_speed=45.0,
            max_ammo=5,
            curr_ammo=5,
            ammo_regen_time=3,
            ammo_fire_delay=1.0,
            x=100.0,
            y=100.0,
            turning=0,
            heading=90.0
        )

class PropFighter(Fighter):
    def __init__(self, engine):
        super().__init__(
            engine,
            image_file="images/propfighter.png",
            top_speed=150.0,
            min_speed=50.0,
            curr_speed=100.0,
            acceleration=5,
            turn_speed=30.0,
            max_ammo=0,
            curr_ammo=0,
            ammo_regen_time=9999,
            ammo_fire_delay=1.0,
            x=1500.0,
            y=1100.0,
            turning=0,
            heading=270.0
        )
