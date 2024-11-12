import pygame
import noise
import math
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load the fireball sprite
fireball_sprite = pygame.image.load('fireball.png').convert_alpha()  # Replace with your sprite path
fireball_sprite = pygame.transform.smoothscale(fireball_sprite, (120, 60))  # Scale if necessary

# Fireball properties
fireball_radius = 30
fireball_pos = [WIDTH, HEIGHT // 2]
fireball_speed = 500

# Perlin noise setup
noise_scale = 0.2
noise_offset_x = random.randint(0, 1000)
noise_offset_y = random.randint(0, 1000)
noise_animation_speed = 25  # Controls how fast the noise pattern animates

# Color gradient for fire-like effect
FIRE_GRADIENT = [
    (120, 40, 0),     # Dark red
    (255, 69, 0),     # Orange red
    (255, 140, 0),    # Orange
    (255, 255, 0),    # Yellow
    (255, 255, 200)   # Bright yellow (high intensity)
]
def get_fire_color(value):
    """Map a noise value (0-1) to a color in the fire gradient."""
    index = int(value * (len(FIRE_GRADIENT) - 1))
    return FIRE_GRADIENT[index]




def animate_fireball_color(sprite, time):
    """Animate the colors of the fireball sprite based on Perlin noise."""
    width, height = sprite.get_size()
    surface = pygame.Surface((width, height), pygame.SRCALPHA)

    for x in range(width):
        for y in range(height):
            # Get animated Perlin noise value for current pixel
            nx = noise_offset_x + x * noise_scale
            ny = noise_offset_y + y * noise_scale
            # Add time-based animation by modifying noise input with the current time
            animated_value = noise.pnoise2(nx+-time * noise_animation_speed, ny)

            # Normalize noise value from -1 to 1 into 0 to 1
            normalized_value = (animated_value + 1) / 2

            # Get fire-like color based on the normalized noise value
            fire_color = get_fire_color(normalized_value)

            # Get the original pixel color from the sprite
            original_color = sprite.get_at((x, y))

            # Combine the fire color with the original sprite color
            new_color = (
                min(255, (original_color.r + fire_color[0]) // 2),
                min(255, (original_color.g + fire_color[1]) // 2),
                min(255, (original_color.b + fire_color[2]) // 2),
                original_color.a  # Keep original alpha
            )
            if(x < 32):
                surface.set_at((x,y),original_color)
            # Set the pixel color on the new surface
            else:
                surface.set_at((x, y), new_color)

    return surface

# Main loop
running = True
time = 0  # Track time for noise animation
while running:
    screen.fill((0, 0, 0))
    dt = clock.tick(60) / 1000

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update fireball position
    fireball_pos[0] -= fireball_speed * dt
    if fireball_pos[0] <= 0:
        fireball_pos[0] = WIDTH//2
        fireball_speed =0

    # Animate the fireball color
    animated_fireball = animate_fireball_color(fireball_sprite, time)
    # Draw the animated fireball
    screen.blit(animated_fireball, (fireball_pos[0] - fireball_radius, fireball_pos[1] - fireball_radius))

    print(clock.get_fps())
    # Update the screen
    pygame.display.flip()

    # Update time for noise animation
    time += dt
# Quit pygame
pygame.quit()
