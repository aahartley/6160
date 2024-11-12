import pygame
import sys
import os
import random
from Particle import Particle, ParticleEmitter

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pygame Drawing Shapes')

font = pygame.font.Font(None, 40)



# Function to save the current screen as a PNG image
def save_screenshot(filename='screenshot.png'):
    pygame.image.save(screen, filename)
    print(f"Screenshot saved as {filename}")

clock = pygame.time.Clock()



# Main loop
running = True
frames = 0
while running:
    dt = clock.tick(60)/1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save_screenshot()  # Save screenshot when 'S' key is pressed
            # elif event.key == pygame.K_SPACE:
            # elif event.key == pygame.K_LEFT:
            # elif event.key == pygame.K_RIGHT:
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            print(mouse_pos)
            #print(screen.get_at(mouse_pos))
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))

    # Fill background with black
    screen.fill(black)
    screen.blit(fps_text,(0,0))

    
    frames += 1
    # Update display
    pygame.display.flip()

pygame.quit()
sys.exit()
