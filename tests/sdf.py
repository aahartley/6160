import pygame
import math
import noise

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Create a surface for trails
trail_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

# Simple fire-like color gradient (black -> red -> yellow -> white)
def fire_color(intensity):
    if intensity < 0.33:
        red = int(255 * intensity * 3)
        return (red, 0, 0)  # Red
    elif intensity < 0.66:
        yellow = int(255 * (intensity - 0.33) * 3)
        return (255, yellow, 0)  # Yellow
    else:
        blue = int(255 * (intensity - 0.66) * 3)
        return (255, 255, min(255, max(0, blue)))  # White with clamping


# Perlin noise-based coloring function
def get_perlin_color(x, y, time, scale=0.1):
    noise_val = noise.pnoise3(x * scale, y * scale, time * 0.9)
    normalized_val = (noise_val + 1) / 2  # Normalize to 0-1
    return fire_color(normalized_val)

# Sphere SDF Function (Signed Distance Function)
def sphere_sdf(x, y, center, radius):
    return math.sqrt((x - center[0])**2 + (y - center[1])**2) - radius

# Main function to draw the fireball and trails
def draw_fireball(screen, time, trail_positions):
    width, height = screen.get_size()
    center = (width // 2, height // 2)
    radius = 25
    
    # Clear the trail surface
    trail_surface.fill((0, 0, 0, 0))  # Transparent background
    
    # Iterate over the 2D grid
    for x in range(375, 425):
        for y in range(275, 325):
            # Get the Signed Distance from the sphere's center
            dist = sphere_sdf(x, y, center, radius)
            
            if dist < 0:  # Inside the sphere
                # Apply a dynamic fire-like texture using Perlin noise
                color = get_perlin_color(x, y, time)
                screen.set_at((x, y), color)  # Directly set the pixel color

    # Draw trails with fading effect
    for i, (trail_x, trail_y) in enumerate(trail_positions):
        # Calculate alpha based on the trail's age
        alpha = max(0, 255 - i * 10)  # Fade out with distance from the current position
        color = (*fire_color(0.5), alpha)  # Use a fixed intensity for trail color
        # Draw the trail at the position with the current alpha
        if 0 <= trail_x < width and 0 <= trail_y < height:
            trail_surface.set_at((trail_x, trail_y), color)

    # Blit the trail surface onto the main screen
    screen.blit(trail_surface, (0, 0))

def main():
    running = True
    time = 0
    trail_positions = []  # List to hold trail positions

    while running:
        screen.fill((0, 0, 0))  # Clear the screen with black

        # Draw the 2D fireball
        draw_fireball(screen, time, trail_positions)

        # Update display
        pygame.display.flip()
        
        # Add the fireball's current position to the trail
        trail_positions.append((400, 300))  # Hardcoded center position for the fireball
        if len(trail_positions) > 20:  # Limit the number of trail positions
            trail_positions.pop(0)  # Remove the oldest position

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        time += 0.1  # Increase time for animation
        clock.tick(30)  # Limit FPS to 30
    
    pygame.quit()

if __name__ == "__main__":
    main()
