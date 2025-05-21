import pygame

def play_music(file, volume=0.25, loops=-1):

    try:
        pygame.mixer.music.load(file)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loops)
        print(f"Playing: {file}")
    except pygame.error as e:
        print(f"Error playing music file: {file} - {e}")