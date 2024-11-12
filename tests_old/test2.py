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

# Function to interpolate between two values
def lerp(start, end, t):
    return start + (end - start) * t

# Function to draw the morphing shape (circle -> rectangle)
def draw_morphing_shape(screen, time, duration):
    # Calculate the interpolation factor (t) based on time and duration
    t = min(time / duration, 1.0)  # Clamps t between 0 and 1

    # Interpolate width, height, and corner radius
    max_radius = 100
    target_width = 200
    target_height = 150

    # Interpolate from a circle to a rectangle
    width = lerp(max_radius * 2, target_width, t)
    height = lerp(max_radius * 2, target_height, t)
    corner_radius = lerp(max_radius, 0, t)  # Reduce the corner radius

    # Draw the morphing shape (rounded rectangle that transitions from circle to rectangle)
    rect = pygame.Rect(400 - width // 2, 300 - height // 2, width, height)
    
    # Draw rounded rectangle or circle
    if corner_radius > 0:
        pygame.draw.rect(screen, WHITE, rect, border_radius=int(corner_radius))
    else:
        pygame.draw.rect(screen, WHITE, rect)

# Main loop
running = True
start_time = pygame.time.get_ticks() / 1000  # Starting time in seconds
duration = 3  # Duration for the morph in seconds

while running:
    screen.fill(BLACK)

    # Get the time elapsed
    current_time = pygame.time.get_ticks() / 1000 - start_time

    # Draw the morphing shape
    draw_morphing_shape(screen, current_time, duration)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the screen
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
