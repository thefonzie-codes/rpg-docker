import pygame
import sys
import argparse
from entities.ghost import Ghost
from entities.player import Player
from helpers.music import play_music
from helpers.fonts import load_font
from system.camera import Camera
from constants import *
from system.map import Map
from textures.base_floor import BaseFloor

def main():

    parser = argparse.ArgumentParser(description='RPG Game')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()
    
    debug_mode = args.debug
    
    pygame.init()

    # Music"
    play_music("assets/audio/Trilogy - Telecasted.mp3")

    # Screen
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
    screen_width, screen_height = screen.get_size()
    viewport = pygame.math.Vector2(screen_width * 0.8, screen_height * 0.8)

    pygame.display.set_caption('RPG Game')

    ## Font rendering
    pixel_font = load_font('fonts/damage/Jersey10-Regular.ttf', 100)
    title = pixel_font.render('PYGAME RPG', True, COLORS['white'])
    title_rect = title.get_rect()

    # FPS and Game
    clock = pygame.time.Clock()
    running = True
    last_time = pygame.time.get_ticks() / 1000.0  # Convert to seconds

    # Camera
    camera = Camera(viewport.x, viewport.y)
    camera.set_screen_size(screen_width, screen_height)

    # Map
    level_map = Map(PIXEL_SIZE)

    # Entities
    ghost = Ghost() 
    player = Player()

    
    # Create a surface for the game viewport
    game_surface = pygame.Surface((viewport.x, viewport.y))

    # Drawing the black background and blitting the frame
    frame_pos = camera.get_frame_position()
    frame_thickness = 4
    frame = pygame.Rect(
            frame_pos.x - frame_thickness,
            frame_pos.y - frame_thickness,
            viewport.x + (frame_thickness * 2), 
            viewport.y + (frame_thickness * 2),
        )
    
    screen.fill(COLORS['black'])
    screen.blit(title, (
        screen_width // 2 - title_rect.w // 2,
        (screen_height // 2 - viewport.y // 2) // 2 - title_rect.h // 2
        ))
    pygame.draw.rect(screen, COLORS['lightgrey'], frame, frame_thickness)

    while running:
        current_time = pygame.time.get_ticks() / 1000.0  # Convert to seconds
        dt = current_time - last_time  # Delta time in seconds
        last_time = current_time

        # Fill the main screen with light gray (for the frame)

        # Draw the game surface onto the main screen at the centered position
        screen.blit(game_surface, (frame_pos.x, frame_pos.y))
        
        # Fill the game surface with black
        game_surface.fill(COLORS['black'])

        keys = pygame.key.get_pressed()
                
        player.update(keys, level_map, dt)
        ghost.update(level_map, dt)
        camera.update(player)

        # Draw to the game surface instead of directly to the screen
        level_map.draw(game_surface, camera)

        ghost_pos = camera.apply(ghost)
        player_pos = camera.apply(player)

        ghost.draw(game_surface, ghost_pos)
        player.draw(game_surface, player_pos)

        # Debug information
        if debug_mode:  # Print debug info every frame with dt
            print("\n--- DEBUG INFO ---")
            print(f"Delta Time: {dt:.4f} seconds")
            print(f"Camera: pos=({camera.offset.x}, {camera.offset.y}), size=({camera.size.x}, {camera.size.y})")
            print(f"Frame position: ({frame_pos.x}, {frame_pos.y})")
            print(f"Screen size: ({screen_width}, {screen_height})")
            print(f"Player: pos=({player.position.x}, {player.position.y}), size=({player.size.x}, {player.size.y})")
            print(f"Ghost: pos=({ghost.position.x}, {ghost.position.y}), size=({ghost.size.x}, {ghost.size.y})")
            print(f"Map: viewport=({camera.offset.x}-{camera.offset.x + camera.size.x // PIXEL_SIZE}, "
                f"{camera.offset.y}-{camera.offset.y + camera.size.y // PIXEL_SIZE}), "
                f"size=({level_map.size.x}, {level_map.size.y})")
            print("-----------------") 

        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()  # Update the display
        clock.tick(60)  # No FPS cap, just let it run

if __name__ == '__main__':
    main()
