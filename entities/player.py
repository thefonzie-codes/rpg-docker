import pygame
import os
from constants import COLORS
from helpers.fonts import load_font

class Player:
    def __init__(self, x=32, y=32):
        self.__max_health__ = 100
        self.__current_health__ = 100
        self.position = pygame.math.Vector2(x, y)  # Replace x, y with Vector2
        self.size = pygame.math.Vector2(8, 13)
        self.moving = False
        self.last_direction = 'right'
        self.animation_time_start = 0
        self.animation_duration = 0.5  # Duration of animation cycle in seconds
        self.models = self.load_sprites('assets/sprites/Player')

    def load_sprites(self, dir):
        print("\n Loading sprites... \n")
        sprites = {
            "left": [],
            "right": []
            }
        files = sorted(os.listdir(dir))
        for file in files:
            if file.endswith('.png'):
                try:
                    sprite_path = os.path.join(dir, file)
                    print(f"{sprite_path}")
                    sprite = pygame.image.load(sprite_path).convert_alpha()
                    sprites['right'].append(sprite)
                    sprites['left'].append(pygame.transform.flip(sprite, True, False))
                except FileNotFoundError:
                    print(f"Sprite missing for {file}")
                except pygame.error as e:
                    print(f"Error loading sprite for {file}: {e}")

        return sprites

    def move(self, keys, map, dt):
        movement = pygame.math.Vector2(0, 0)  # Initialize movement vector
        speed = 50  # Pixels per second
        if keys[pygame.K_a]:
            self.moving = True
            movement.x -= speed * dt
            self.last_direction = 'left'
            if self.animation_time_start == 0:
                self.animation_time_start = pygame.time.get_ticks() / 1000.0
        if keys[pygame.K_d]:
            self.moving = True
            movement.x += speed * dt
            self.last_direction = 'right'
            if self.animation_time_start == 0:
                self.animation_time_start = pygame.time.get_ticks() / 1000.0
        if keys[pygame.K_w]:
            self.moving = True
            movement.y -= speed * dt
            if self.animation_time_start == 0:
                self.animation_time_start = pygame.time.get_ticks() / 1000.0
        if keys[pygame.K_s]:
            self.moving = True
            movement.y += speed * dt
            if self.animation_time_start == 0:
                self.animation_time_start = pygame.time.get_ticks() / 1000.0

        if movement.length() > 0:  # Only update position if there's movement
            self.position += movement
        else:
            self.moving = False
            self.animation_time_start = 0

        # Clamp position within map bounds
        self.position = pygame.math.Vector2(
            max(0, min(self.position.x, map.size.x - self.size.x)), 
            max(0, min(self.position.y, map.size.y - self.size.y))
            )

    def update(self, keys, map, dt):
        self.move(keys, map, dt)

    def draw(self, screen, position, pixel_size=4):
        model = self.models['right'][0]
        if self.moving == False:
                model = self.models[self.last_direction][0]

        else:
            current_time = pygame.time.get_ticks() / 1000.0
            elapsed = current_time - self.animation_time_start
            if elapsed < self.animation_duration / 2:
                model = self.models[self.last_direction][1]
            else:
                model = self.models[self.last_direction][0]
            if elapsed >= self.animation_duration:
                self.animation_time_start = current_time  # Reset animation cycle
        
        screen.blit(model, (
            (position.x) * pixel_size, 
            (position.y) * pixel_size))
