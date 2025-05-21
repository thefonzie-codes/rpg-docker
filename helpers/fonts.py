import pygame

def load_font(name: str, size: int = 36):
    try:
        pixel_font = pygame.font.Font(name, size)
        return pixel_font
    except pygame.error as e:
        print(f"Error loading font: {e}")
        return pygame.font.SysFont('Arial', size)      
    except FileNotFoundError:
        print(f"Error: Font not found, using default.")
        return pygame.font.SysFont('Arial', size)