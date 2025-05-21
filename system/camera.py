import pygame

class Camera:

    def __init__(self, width, height):
        self.size = pygame.math.Vector2(width, height)
        self.offset = pygame.math.Vector2(0, 0)
        self.screen_size = pygame.math.Vector2(0, 0)  # Store actual screen dimensions
        
    def set_screen_size(self, width, height):
        self.screen_size = pygame.math.Vector2(width, height)

    def update(self, target, pixel_size = 4):
        target_center = pygame.math.Vector2(target.position.x + target.size.x // 2, target.position.y + target.size.y // 2)
        self.offset = target_center - (self.size // (2 * pixel_size))

    def apply(self, entity):
        return pygame.math.Vector2(entity.position.x - self.offset.x, entity.position.y - self.offset.y)  # Return tuple for drawing
        
    def get_frame_position(self):
        # Calculate position to center the viewport on screen
        frame = (self.screen_size - self.size) // 2
        return pygame.math.Vector2(frame.x, frame.y)