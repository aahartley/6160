import pygame
import math

# Initialize Pygame
pygame.init()

# Set screen dimensions
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Function to draw a circle that morphs
def draw_morphing_circle(screen, time):
    radius = 50 + int(20 * math.sin(time))  # Morph radius over time
    x = 400 + int(100 * math.cos(time))  # Move in a circular path
    y = 300 + int(100 * math.sin(time))  # Move in a circular path
    pygame.draw.circle(screen, WHITE, (x, y), radius)

running = True
start_time = pygame.time.get_ticks() / 1000

# Main loop
while running:
    screen.fill(BLACK)

    # Get the time elapsed
    current_time = pygame.time.get_ticks() / 1000 - start_time

    # Draw morphing circle
    draw_morphing_circle(screen, current_time)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the screen
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
