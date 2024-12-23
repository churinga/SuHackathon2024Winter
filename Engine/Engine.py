import traceback

import pygame
import time
import threading

from Engine.Obstacle import Obstacle
from Engine.Fighter import JetFighter, PropFighter
from Engine.Bullet import Bullet
from Engine.Explosion import Explosion
from Engine.SnowFlake import SnowFlake
from Engine.StatsBoard import StatsBoard
from Engine.Strategy import Strategy
import Engine.Utils as Utils

class Engine:
    def __init__(self):
        pygame.init()

        self.fonts = {}
        self.load_fonts()
        self.sounds = {}
        self.load_sounds()

        self.screen_width = 1600
        self.screen_height = 1200
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.mode = 1  # 1 for single player, and 2 for two players
        self.jetfighter = JetFighter(self)
        self.propfighter = PropFighter(self)
        self.stats_board = StatsBoard(self)
        self.obstacle = Obstacle(self, 600, 400)
        self.obstacles = pygame.sprite.Group()
        self.obstacles.add(self.obstacle)
        self.explosions = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.bgcolor = (222, 222, 222)
        self.running = False
        self.updating = False
        self.tick = 25  # msecs per frame
        self.start_ts = time.time()
        self.end_ts = 0
        self.ending_text = ""
        self.game_over_sound_played = False
        self.strategy_obj = None  # Placeholder for user-defined function
        self.decision_thread = None  # Thread for decision function

    def load_fonts(self):
        fonts = {
            "chakra-56-regular": {
                "name": "fonts/ChakraPetch-Regular.ttf",
                "size": 56
            },
            "chakra-28-regular": {
                "name": "fonts/ChakraPetch-Regular.ttf",
                "size": 28
            },
            "chakra-22-regular": {
                "name": "fonts/ChakraPetch-Regular.ttf",
                "size": 22
            },
            "chakra-16-regular": {
                "name": "fonts/ChakraPetch-Regular.ttf",
                "size": 16
            },
            "chakra-108-bold": {
                "name": "fonts/ChakraPetch-Bold.ttf",
                "size": 108
            },
            "chakra-80-bold": {
                "name": "fonts/ChakraPetch-Bold.ttf",
                "size": 80
            },
            "chakra-64-bold": {
                "name": "fonts/ChakraPetch-Bold.ttf",
                "size": 64
            },
            "chakra-32-bold": {
                "name": "fonts/ChakraPetch-Bold.ttf",
                "size": 32
            },
        }

        for key in fonts.keys():
            font = pygame.font.Font(fonts[key]["name"], fonts[key]["size"])
            self.fonts[key] = font

    def load_sounds(self):
        pygame.mixer.init()

        self.sounds = {
            "banner": pygame.mixer.Sound("sounds/banner.mp3"),
            "game_start": pygame.mixer.Sound("sounds/game_start.mp3"),
            "game_over": pygame.mixer.Sound("sounds/game_over.mp3"),
            "shooting": pygame.mixer.Sound("sounds/shooting.mp3"),
            "explosion": pygame.mixer.Sound("sounds/explosion.mp3"),
            "explosion2": pygame.mixer.Sound("sounds/explosion2.mp3"),
        }

    def start_decision_thread(self):
        """Start a separate thread for the user-defined decision function."""
        if self.mode == 1 and self.strategy_obj is not None:
            print("Starting decision thread...")
            self.decision_thread = threading.Thread(target=self.run_decision_function)
            self.decision_thread.daemon = True  # Daemon thread will exit when the main program exits
            self.decision_thread.start()

    def run_decision_function(self):
        """Run the user-defined function at regular intervals."""
        count = 0
        time.sleep(self.tick / 1000.0)  # Sleep for one tick at the start

        while self.running:
            start_time = time.perf_counter()  # Record the start time
            # Gather bullet info into a list
            bullet_info = []
            for bullet in self.bullets:
                bullet_info.append({
                    "x": bullet.x,
                    "y": bullet.y,
                    "heading": bullet.heading,
                    "speed": bullet.speed,
                    "distance_traveled": bullet.distance_traveled,
                    "max_distance": bullet.max_distance,
                })
            # Jetfighter info
            jetfighter_info = {
                "x": self.jetfighter.x,
                "y": self.jetfighter.y,
                "heading": self.jetfighter.heading,
                "turning": self.jetfighter.turning,
                "turn_speed": self.jetfighter.turn_speed,
                "curr_speed": self.jetfighter.curr_speed,
                "top_speed": self.jetfighter.top_speed,
                "min_speed": self.jetfighter.min_speed,
                "curr_ammo": self.jetfighter.curr_ammo,
                "max_ammo": self.jetfighter.max_ammo,
                "ammo_regen_time": self.jetfighter.ammo_regen_time,
                "ammo_fire_delay": self.jetfighter.ammo_fire_delay,
            }
            # Propfighter info
            propfighter_info = {
                "x": self.propfighter.x,
                "y": self.propfighter.y,
                "heading": self.propfighter.heading,
                "turning": self.propfighter.turning,
                "turn_speed": self.propfighter.turn_speed,
                "curr_speed": self.propfighter.curr_speed,
                "min_speed": self.propfighter.min_speed,
                "top_speed": self.propfighter.top_speed,
            }
            # Obstacle info
            obstacle_info = {
                "x": self.obstacle.rect.x,
                "y": self.obstacle.rect.y,
                "width": self.obstacle.rect.width,
                "height": self.obstacle.rect.height,
            }
            try:
                cmd = self.strategy_obj.decision(
                    seq=count,
                    jetfighter_info=jetfighter_info,
                    propfighter_info=propfighter_info,
                    obstacle_info=obstacle_info,
                    bullet_info=bullet_info,
                )  # Call the user-defined function
            except Exception:
                print(f"Player strategy function had a brain fart: {traceback.format_exc()}")
                cmd = Strategy.NOOP

            self.handle_player_cmd(cmd)
            ts = time.perf_counter()

            # Calculate remaining time to delay
            elapsed_time = (ts - start_time) * 1000  # Convert to milliseconds
            #print(f"[{ts} Decision function returned command: {cmd}. elapsed time={elapsed_time} msecs] ")
            remaining_time = self.tick - elapsed_time
            count += int(elapsed_time // self.tick) + 1
            if remaining_time < 0:
                print(f"Decision function took too long to run (took {elapsed_time} msecs). Skipping frame(s).")
                remaining_time = remaining_time % self.tick
            time.sleep(remaining_time / 1000.0)  # Sleep for the remaining time
        print("Decision thread ended.")

    def set_strategy_obj(self, strategy_obj:Strategy):
        """Set the user-defined function to be called in the thread."""
        self.strategy_obj = strategy_obj

    def handle_player_cmd(self, cmd):
        if cmd == Strategy.TURN_LEFT:
            self.jetfighter.turning = -1
        elif cmd == Strategy.TURN_RIGHT:
            self.jetfighter.turning = 1
        elif cmd == Strategy.GO_STRAIGHT:
            self.jetfighter.turning = 0
        elif cmd == Strategy.ACCELERATE:
            self.jetfighter.curr_speed += self.jetfighter.acceleration
            self.jetfighter.curr_speed = min(self.jetfighter.curr_speed, self.jetfighter.top_speed)
        elif cmd == Strategy.DECELERATE:
            self.jetfighter.curr_speed -= self.jetfighter.acceleration
            self.jetfighter.curr_speed = max(self.jetfighter.curr_speed, self.jetfighter.min_speed)
        elif cmd == Strategy.FIRE_AMMO:
            self.handle_fire_ammo()

    def handle_fire_ammo(self):
        # Check whether the jetfighter can fire a bullet
        if self.jetfighter.curr_ammo > 0 and time.time() >= self.jetfighter.prev_ammo_fire_ts + self.jetfighter.ammo_fire_delay:
            # OK to fire
            self.jetfighter.prev_ammo_fire_ts = time.time()
            self.jetfighter.curr_ammo -= 1

            tip_x, tip_y = self.jetfighter.get_tip_coord()

            # Create a new Bullet instance
            bullet = Bullet(
                engine=self,  # Pass the engine object
                x=tip_x,  # X coordinate at the tip of the jetfighter
                y=tip_y,  # Y coordinate at the tip of the jetfighter
                heading=self.jetfighter.heading,  # Use the jetfighter's heading
            )
            self.bullets.add(bullet)  # Add the bullet to the sprite group
            self.sounds["shooting"].play()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                # If game has already ended, press any key to exit the program
                if self.end_ts > 0 and time.time() - self.end_ts > 1.5 and not self.updating:
                    pygame.quit()
                    exit()

                # Check for key presses
                keys = pygame.key.get_pressed()

                # Propfighter controls
                if keys[pygame.K_LEFT]:
                    if self.propfighter.turning == 0:
                        self.propfighter.turning = -1
                    elif self.propfighter.turning == 1:
                        self.propfighter.turning = 0

                if keys[pygame.K_RIGHT]:
                    if self.propfighter.turning == 0:
                        self.propfighter.turning = 1
                    elif self.propfighter.turning == -1:
                        self.propfighter.turning = 0

                if keys[pygame.K_UP]:
                    self.propfighter.curr_speed += self.propfighter.acceleration
                    if self.propfighter.curr_speed > self.propfighter.top_speed:
                        self.propfighter.curr_speed = self.propfighter.top_speed

                if keys[pygame.K_DOWN]:
                    self.propfighter.curr_speed -= self.propfighter.acceleration
                    if self.propfighter.curr_speed < self.propfighter.min_speed:
                        self.propfighter.curr_speed = self.propfighter.min_speed

                # Jetfighter controls
                if keys[pygame.K_a] and self.mode == 2:
                    if self.jetfighter.turning == 0:
                        self.jetfighter.turning = -1
                    elif self.jetfighter.turning == 1:
                        self.jetfighter.turning = 0

                if keys[pygame.K_d] and self.mode == 2:
                    if self.jetfighter.turning == 0:
                        self.jetfighter.turning = 1
                    elif self.jetfighter.turning == -1:
                        self.jetfighter.turning = 0

                if keys[pygame.K_w] and self.mode == 2:
                    self.jetfighter.curr_speed += self.jetfighter.acceleration
                    if self.jetfighter.curr_speed > self.jetfighter.top_speed:
                        self.jetfighter.curr_speed = self.jetfighter.top_speed

                if keys[pygame.K_s] and self.mode == 2:
                    self.jetfighter.curr_speed -= self.jetfighter.acceleration
                    if self.jetfighter.curr_speed < self.jetfighter.min_speed:
                        self.jetfighter.curr_speed = self.jetfighter.min_speed

                # Check for space key to fire a bullet
                if event.key == pygame.K_SPACE and self.mode == 2:
                    self.handle_fire_ammo()

    def update_battlefield(self):
        self.obstacle.update()

        # Display both fighters
        self.jetfighter.update()
        self.propfighter.update()

        # Display bullets
        self.bullets.update()

        # Draw explosions, if any
        self.explosions.update()

    def draw_battlefield(self):
        self.screen.fill(self.bgcolor)

        # Draw the obstacle
        self.obstacle.draw()

        # Display both fighters
        self.jetfighter.draw()
        self.propfighter.draw()

        # Stats board
        self.stats_board.draw()

        # Display bullets
        for bullet in self.bullets:
            bullet.draw()

        # Draw explosions, if any
        for explosion in self.explosions:
            if not self.updating:
                # explosions still need updating to finish animation
                explosion.update()
            explosion.draw()

        # If game is over, display "Game Over" after 1.5s and end the game
        if self.end_ts > 0 and time.time() - self.end_ts > 1.5:
            self.display_game_ending()

        pygame.display.flip()

    def check_victory(self):
        # Return 0 for no one wins, 1 for jetfighter victory, -1 for propfighter victory
        # Check if a bullet hits propfighter
        bullet = Utils.check_collision_with_group(self.propfighter, self.bullets)
        if bullet:
            print(f"Propfighter hit by a bullet! Jetfighter won!!")
            self.create_explosion(bullet, self.propfighter, 71, "explosion")
            self.bullets.remove(bullet)
            self.propfighter.kill()
            self.ending_text = f"Jet-fighter won!! Prop-fighter survived {int(time.time() - self.start_ts)} seconds."
            return 1
        # Check if jetfighter collides with obstacle
        obstacle = Utils.check_collision_with_group(self.jetfighter, self.obstacles)
        if obstacle:
            print(f"Jetfighter hit by an obstacle! Propfighter won!!")
            self.create_explosion(obstacle, self.jetfighter, 71, "explosion")
            self.jetfighter.kill()
            self.ending_text = f"Jet-fighter committed suicide!! Prop-fighter won!!"
            return -1
        # Check if propfighter collides with obstacle
        obstacle = Utils.check_collision_with_group(self.propfighter, self.obstacles)
        if obstacle:
            print(f"Propfighter hit by an obstacle! Jetfighter won!!")
            self.create_explosion(obstacle, self.propfighter, 71, "explosion")
            self.propfighter.kill()
            self.ending_text = f"Jet-fighter won!! Prop-fighter survived {int(time.time() - self.start_ts)} seconds."
            return 1
        # Check if propfighter collides with jetfighter. In this case, propfighter wins.
        if Utils.check_collision(self.propfighter, self.jetfighter):
            print(f"Jetfighter crashed with propfighter! Propfighter won!!")
            self.create_explosion(self.jetfighter, self.propfighter, 71, "explosion")
            self.jetfighter.kill()
            self.propfighter.kill()
            self.ending_text = f"Jet-fighter crashed into Prop-fighter!! Prop-fighter won!!"
            return -1
        return 0

    def create_explosion(self, sprite1, sprite2, size, sound):
        offset = (sprite2.rect.left - sprite1.rect.left, sprite2.rect.top - sprite1.rect.top)
        collision_coord = sprite1.mask.overlap(sprite2.mask, offset)
        if collision_coord is None:
            offset = (sprite2.rect.x - sprite1.rect.x, sprite2.rect.y - sprite1.rect.y)
            closest_point = Utils.find_closest_collision_point(sprite1.mask, sprite2.mask, offset)
            if closest_point is not None:
                collision_x, collision_y = collision_coord
            else:
                # Failed to find closest point. Create explosion at sprite2
                collision_x, collision_y = sprite2.rect.x, sprite2.rect.y
        else:
            collision_x, collision_y = collision_coord
        explosion = Explosion(self, collision_x + sprite1.rect.x, collision_y + sprite1.rect.y, size)
        self.explosions.add(explosion)
        self.sounds[sound].play()

    def display_game_ending(self):
        game_over = self.fonts["chakra-80-bold"].render("GAME OVER", True, (255, 165, 0))
        self.screen.blit(game_over, ((self.screen.get_width() - game_over.get_width()) // 2, 150))
        press_key = self.fonts["chakra-28-regular"].render("Press any key to exit...", True, (66, 66, 66))
        self.screen.blit(press_key, ((self.screen.get_width() - press_key.get_width()) // 2, 1060))
        ending_text = self.fonts["chakra-32-bold"].render(self.ending_text, True, (66, 66, 66))
        self.screen.blit(ending_text, ((self.screen.get_width() - ending_text.get_width()) // 2, 290))
        if not self.game_over_sound_played:
            self.sounds["game_over"].play()
            self.game_over_sound_played = True

    def display_banner(self):
        pygame.display.set_caption("Game Selection")
        font = self.fonts["chakra-108-bold"]
        title = font.render("Welcome to", True, (255, 255, 255))
        title2 = font.render("Su Family Hackathon", True, (255, 255, 255))
        font = self.fonts["chakra-64-bold"]
        subtitle = font.render("2024 Winter Special Edition", True, (255, 255, 255))
        font = self.fonts["chakra-56-regular"]
        label_1 = font.render("1 Player", True, (255, 255, 255))
        label_2 = font.render("2 Players", True, (255, 255, 255))

        rect_1 = label_1.get_rect(center=(800, 800))
        rect_2 = label_2.get_rect(center=(800, 900))

        snowflakes = pygame.sprite.Group()
        for i in range(15):
            snowflake = SnowFlake(self)
            snowflakes.add(snowflake)

        self.sounds["banner"].play()

        while True:
            self.screen.fill((0, 0, 0))

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if rect_1.collidepoint(pygame.mouse.get_pos()):
                        self.mode = 1
                    elif rect_2.collidepoint(pygame.mouse.get_pos()):
                        self.mode = 2
                    self.sounds["banner"].stop()
                    return

            # Hover detection
            mouse_pos = pygame.mouse.get_pos()
            if rect_1.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, (88, 88, 88), rect_1)
            else:
                pygame.draw.rect(self.screen, (0, 0, 0), rect_1)

            if rect_2.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, (88, 88, 88), rect_2)
            else:
                pygame.draw.rect(self.screen, (0, 0, 0), rect_2)

            # Draw title and subtitle
            self.screen.blit(title, ((self.screen.get_width() - title.get_width()) // 2, 200))
            self.screen.blit(title2, ((self.screen.get_width() - title2.get_width()) // 2, 330))
            self.screen.blit(subtitle, ((self.screen.get_width() - subtitle.get_width()) // 2, 500))

            # Draw snowflakes
            snowflakes.update()
            for snowflake in snowflakes:
                snowflake.draw()

            # Draw labels
            self.screen.blit(label_1, rect_1)
            self.screen.blit(label_2, rect_2)

            pygame.display.flip()

    def run(self):
        pygame.display.set_caption("Battle!")

        self.running = True
        self.updating = True
        self.start_ts = time.time()
        self.start_decision_thread()  # Start the thread when the function is set

        self.sounds["game_start"].play()

        while self.running:
            start_time = pygame.time.get_ticks()  # Start timing

            # Handle events
            self.check_events()
            if self.updating:
                self.update_battlefield()
            self.draw_battlefield()
            if self.updating:
                if self.check_victory() != 0:
                    self.end_ts = time.time()
                    self.updating = False
                    print(f"Game ended! Prop-fighter survived for {int(self.end_ts - self.start_ts)} seconds!")

            # Calculate elapsed time
            elapsed_time = pygame.time.get_ticks() - start_time

            # Calculate remaining time to delay
            remaining_time = self.tick - elapsed_time
            if remaining_time > 0:
                pygame.time.delay(remaining_time)  # Delay only if there's time left

        self.running = False
        pygame.quit()
