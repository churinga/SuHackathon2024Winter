from calendar import leapdays

import pygame
import math
import time

class StatsBoard:
    def __init__(self, engine):
        self.engine = engine
        self.up_arrow = pygame.image.load("images/up_arrow.png")
        self.up_arrow = pygame.transform.scale(self.up_arrow, (70, 70))
        self.left_arrow = pygame.image.load("images/left_turn.png")
        self.left_arrow = pygame.transform.scale(self.left_arrow, (70, 70))
        self.right_arrow = pygame.image.load("images/right_turn.png")
        self.right_arrow = pygame.transform.scale(self.right_arrow, (70, 70))
        self.font = engine.fonts["chakra-28-regular"]
        self.font_small = engine.fonts["chakra-22-regular"]
        self.label_font = engine.fonts["chakra-16-regular"]

    def draw(self):
        # Get screen dimensions and calculate the center area
        screen_width, screen_height = self.engine.screen.get_size()
        center_x = screen_width // 2
        center_y = screen_height // 2
        top_y = center_y - 200
        bottom_y = center_y + 200
        left_center_x = center_x - 150
        right_center_x = center_x + 150

        # Draw labels for jetfighter and propfighter
        jetfighter_label_surface = self.font.render("Jet-fighter", True, (255, 255, 255))
        propfighter_label_surface = self.font.render("Prop-fighter", True, (255, 255, 255))

        # Position labels
        self.engine.screen.blit(jetfighter_label_surface, (left_center_x - jetfighter_label_surface.get_width() // 2, top_y + 20))
        self.engine.screen.blit(propfighter_label_surface, (right_center_x - propfighter_label_surface.get_width() // 2, top_y + 20))

        # Draw left column widgets (jetfighter)
        self.draw_speedometer(left_center_x - 50, top_y + 80, self.engine.jetfighter)  # Adjusted for label height
        self.draw_heading(left_center_x, top_y + 200, self.engine.jetfighter)
        self.draw_operation_state(left_center_x, top_y + 250, self.engine.jetfighter)
        self.draw_ammo(left_center_x, top_y + 340, self.engine.jetfighter)

        # Draw divider
        pygame.draw.rect(self.engine.screen, (255, 255, 255), (center_x - 1, top_y, 3, 400))

        # Draw right column widgets (propfighter)
        self.draw_speedometer(right_center_x - 50, top_y + 80, self.engine.propfighter)  # Adjusted for label height
        self.draw_heading(right_center_x, top_y + 200, self.engine.propfighter)
        self.draw_operation_state(right_center_x, top_y + 250, self.engine.propfighter)
        self.draw_timer(right_center_x, top_y + 340)

    def draw_speedometer(self, x, y, fighter):
        # Speedometer parameters
        radius = 50
        center = (x + radius, y + radius)
        min_speed = fighter.min_speed
        max_speed = fighter.top_speed
        curr_speed = fighter.curr_speed

        # Draw the outer circle
        pygame.draw.circle(self.engine.screen, (255, 255, 255), center, radius, 2)

        # Draw min and max speed labels
        min_label_surface = self.label_font.render(f"{int(min_speed)}", True, (255, 255, 255))
        max_label_surface = self.label_font.render(f"{int(max_speed)}", True, (255, 255, 255))
        current_label_surface = self.label_font.render(f"{int(curr_speed)}", True, (255, 255, 255))

        # Position labels
        self.engine.screen.blit(min_label_surface, (center[0] - radius - min_label_surface.get_width() // 2, center[1] - min_label_surface.get_height() // 2))
        self.engine.screen.blit(max_label_surface, (center[0] + radius - max_label_surface.get_width() // 2, center[1] - max_label_surface.get_height() // 2))
        self.engine.screen.blit(current_label_surface, (center[0] - current_label_surface.get_width() // 2, center[1] - current_label_surface.get_height() // 2))

        # Calculate the angle for the needle
        if max_speed > min_speed:
            # Normalize current speed to a value between 0 and 1
            normalized_speed = (curr_speed - min_speed) / (max_speed - min_speed)
            # Calculate the angle (0 degrees for min speed, 180 degrees for max speed)
            needle_angle = 180 * normalized_speed
        else:
            needle_angle = 0  # If min and max speeds are the same, keep the needle at 0

        # Draw the needle
        needle_rad = math.radians(needle_angle)
        needle_x = center[0] - (radius - 10) * math.cos(needle_rad)
        needle_y = center[1] - (radius - 10) * math.sin(needle_rad)
        pygame.draw.line(self.engine.screen, (255, 0, 0), center, (needle_x, needle_y), 4)  # Red needle

    def draw_heading(self, center_x, y, fighter):
        heading_text = f"Heading: {int(fighter.heading)}°"
        text_surface = self.font_small.render(heading_text, True, (255, 255, 255))
        self.engine.screen.blit(text_surface, (center_x - text_surface.get_width() // 2, y))

    def draw_operation_state(self, center_x, y, fighter):
        image = self.up_arrow
        if fighter.turning == 0:
            image = self.up_arrow
        elif fighter.turning == -1:
            image = self.left_arrow
        elif fighter.turning == 1:
            image = self.right_arrow
        self.engine.screen.blit(image, (center_x - image.get_width() // 2, y))

    def draw_ammo(self, center_x, y, fighter):
        ammo_text = f"Ammo: {fighter.curr_ammo} / {fighter.max_ammo}"
        color = (255, 255, 255)
        if fighter.curr_ammo == 0:
            color = (255, 0, 0)
        text_surface = self.font_small.render(ammo_text, True, color)
        self.engine.screen.blit(text_surface, (center_x - text_surface.get_width() // 2, y))

    def draw_timer(self, center_x, y):
        # Calculate elapsed time
        if self.engine.end_ts > 0:
            elapsed_time = self.engine.end_ts - self.engine.start_ts
        else:
            elapsed_time = time.time() - self.engine.start_ts
        hours, remainder = divmod(int(elapsed_time), 3600)
        minutes, seconds = divmod(remainder, 60)

        # Format the timer as HH:MM:SS
        timer_text = f"{hours:02}:{minutes:02}:{seconds:02}"
        timer_surface = self.font_small.render(timer_text, True, (255, 255, 255))

        # Position the timer
        self.engine.screen.blit(timer_surface, (center_x - timer_surface.get_width() // 2, y))
