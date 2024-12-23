import pygame

def check_collision(sprite1, sprite2):
    return pygame.sprite.collide_mask(sprite1, sprite2)

def check_collision_with_group(sprite1, group):
    # Check for rectangle-based collisions
    potential_collisions = pygame.sprite.spritecollide(sprite1, group, False)

    # Check for pixel-perfect collisions
    for sprite in potential_collisions:
        if sprite != sprite1 and pygame.sprite.collide_mask(sprite1, sprite):
            return sprite

    return None

def find_closest_collision_point(mask1, mask2, offset):
    """
    Finds the closest collision point between two masks if overlap fails.
    :param mask1: pygame.Mask of the first sprite
    :param mask2: pygame.Mask of the second sprite
    :param offset: Tuple (x_offset, y_offset) from mask1 to mask2
    :return: Closest collision point as (x, y) or None if no pixels are near.
    """
    min_distance = float('inf')
    closest_point = None

    # Loop through mask1's non-transparent pixels
    for x1, y1 in mask1.outline():
        # Translate mask1's pixel position to mask2's coordinate space
        x2 = x1 - offset[0]
        y2 = y1 - offset[1]

        # Check if the translated pixel is within mask2's bounds and is non-transparent
        if 0 <= x2 < mask2.get_size()[0] and 0 <= y2 < mask2.get_size()[1] and mask2.get_at((x2, y2)):
            # Compute Euclidean distance between points
            distance = math.sqrt((x1 - x2 - offset[0]) ** 2 + (y1 - y2 - offset[1]) ** 2)
            if distance < min_distance:
                min_distance = distance
                closest_point = (x1, y1)

    return closest_point

def wrap_around(obj, screen_width, screen_height):
    # Wrap bullet around the screen edges
    if obj.x < 0:
        obj.x = screen_width
    elif obj.x > screen_width:
        obj.x = 0

    if obj.y < 0:
        obj.y = screen_height
    elif obj.y > screen_height:
        obj.y = 0
