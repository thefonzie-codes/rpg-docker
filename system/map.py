import pygame

class Map:
    def __init__(self, pixel_size):
        self.pixel_size = pixel_size
        self.map_img = self.load('assets/maps/level_1.png') 
        self.size = pygame.math.Vector2(
            self.map_img.get_width() // pixel_size,
            self.map_img.get_height() // pixel_size
        )

    def load(self, file_path):
        try:
            print(f"Loading map... {file_path}")
            map = pygame.image.load(file_path).convert_alpha()
            return map
        except FileNotFoundError:
            print(f"Sprite missing for {file_path}")
        except pygame.error as e:
            print(f"Error loading sprite for {file_path}: {e}")

    def draw(self, screen, camera):
        start = pygame.math.Vector2(max(0, camera.offset.x), max(0, camera.offset.y))
        end = pygame.math.Vector2(
            min(self.size.x, camera.offset.x + (camera.size.x // self.pixel_size)), 
            min(self.size.y, camera.offset.y + (camera.size.y // self.pixel_size))
            )

        for x in range(int(start.x), int(end.x)):
            for y in range(int(start.y), int(end.y)):
                screen_position = pygame.math.Vector2(
                        (x - camera.offset.x) * self.pixel_size,
                        (y - camera.offset.y) * self.pixel_size
                    )
                
                source_rect = pygame.Rect(
                        x * self.pixel_size,  
                        y * self.pixel_size,  
                        self.pixel_size,      
                        self.pixel_size       
                    )
                
                screen.blit(self.map_img, screen_position, source_rect)

        # for x in range(int(start.x), int(end.x)):
        #     for y in range(int(start.y), int(end.y)):
        #         screen_position = pygame.math.Vector2((x - camera.offset.x) * self.pixel_size, (y - camera.offset.y) * self.pixel_size)
        #         screen.blit(self.map_img, (0, 0), (screen_position.x, screen_position.y, self.pixel_size, self.pixel_size))

    # def draw(self, screen, camera):
    #     start = pygame.math.Vector2(max(0, camera.offset.x), max(0, camera.offset.y))
    #     end = pygame.math.Vector2(
    #         min(self.size.x, camera.offset.x + (camera.size.x // self.pixel_size)), 
    #         min(self.size.y, camera.offset.y + (camera.size.y // self.pixel_size))
    #         )

    #     for x in range(int(start.x), int(end.x)):
    #         for y in range(int(start.y), int(end.y)):

    #             # There is no point in converting this to a vector2.
    #             pattern_x = x % len(self.floor_texture.pattern[0])
    #             pattern_y = y % len(self.floor_texture.pattern)

    #             tile = self.floor_texture.pattern[pattern_y][pattern_x]

    #             screen_position = pygame.math.Vector2((x - camera.offset.x) * self.pixel_size, (y - camera.offset.y) * self.pixel_size)
    #             pygame.draw.rect(screen, self.floor_texture.colors[tile], (screen_position.x, screen_position.y, self.pixel_size, self.pixel_size))
