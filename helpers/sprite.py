import pygame

def load_sprites(img_file):
    try:
        sprite = pygame.image.load(img_file).convert_alpha()
        return sprite
    except FileNotFoundError:
        print(f"Sprite missing for {img_file}")
    except pygame.error as e:
        print(f"Error loading sprite for {img_file}: {e}")
