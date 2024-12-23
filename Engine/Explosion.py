import pygame
from PIL import Image

class Explosion(pygame.sprite.Sprite):
    frames_cache = {}  # map from size to list of frame images

    def __init__(self, engine, x, y, size):
        """
        :param x: center x of the explosion animation
        :param y: center y of the explosion animation
        :param size: dimension of the explosion (original size is 71x100, so if size is 71, it uses the original size)
        """
        super().__init__()
        self.engine = engine
        self.frame_index = 1
        if size not in Explosion.frames_cache:
            Explosion.frames_cache[size] = Explosion.load_gif_frames("images/explosion.gif", size)
        self.frames = Explosion.frames_cache[size]
        self.x = x
        self.y = y
        self.size = size
        self.starting_tick = pygame.time.get_ticks()
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(self.x, self.y))

    # Function to load GIF frames as pygame surfaces
    @staticmethod
    def load_gif_frames(gif_path, size):
        frames = []
        with Image.open(gif_path) as gif:
            for frame in range(gif.n_frames):
                gif.seek(frame)
                # Convert PIL image to a format pygame can use
                frame_surface = pygame.image.fromstring(
                    gif.tobytes(), gif.size, gif.mode
                )
                frame_surface = pygame.transform.scale(frame_surface,
                                                       (size, frame_surface.get_height() * size // frame_surface.get_width()))
                frames.append(frame_surface)
        return frames

    def update(self):
        current_tick = pygame.time.get_ticks()
        if current_tick - self.starting_tick > 100:
            # need to cut the 1st, because it somehow is not transparent
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
            self.starting_tick = current_tick
            if self.frame_index == 0:
                self.kill()

    def draw(self):
        if self.frame_index > 0:
            self.engine.screen.blit(self.image, self.rect)

