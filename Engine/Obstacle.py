import pygame

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, engine, width, height):
        super().__init__()  # Initialize the parent Sprite class
        self.engine = engine  # Store the reference to the Engine object
        self.width = width
        self.height = height

        # Create a surface for the obstacle
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((50, 50, 50))  # Dark gray color
        self.mask = pygame.mask.from_surface(self.image)

        # Get the rectangle for positioning
        self.rect = self.image.get_rect(center=(self.engine.screen_width // 2, self.engine.screen_height // 2))

    def update(self):
        # Update logic for the obstacle can go here if needed
        pass

    def draw(self):
        # Draw the obstacle on the screen
        self.engine.screen.blit(self.image, self.rect)