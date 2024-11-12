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

# Colors (R, G, B) and with Alpha
red = (255, 0, 0)
green = (0, 255, 0)
grass = (124, 252, 0)
blue = (0, 0, 255)
yellow = (212,175,55)
purple = (128, 0, 128)
dark_beige = (217,174,128)
black = (0,0,0)
white = (255,255,255)
night_sky = (19,24,98)
darker_sky = (17,19,56)
brown = (139,69,19)
door = (128,117,115)
blue_water = (153,192,227)
dim_gray = (105,105,105)
yellow = (255,255,224)
glass = (216,228,233)
# Colors with alpha for transparency
transparent_red = (255, 255, 255, 128)  # 50% transparent red
transparent_black = (15, 15, 15, 128)  # 50% transparent red
transparent_green = (0, 255, 0, 128)  # 50% transparent green

# Surface for alpha shapes
alpha_surface = pygame.Surface((width, 400), pygame.SRCALPHA)


# Function to save the current screen as a PNG image
def save_screenshot(filename='screenshot.png'):
    pygame.image.save(screen, filename)
    print(f"Screenshot saved as {filename}")

clock = pygame.time.Clock()

particles = []
emitters = [ParticleEmitter([0,0])]
img = pygame.image.load(os.path.join('.' ,'drag.png')).convert_alpha()
img = pygame.transform.smoothscale(img, (200, 200))
font = pygame.font.Font(None, 36)
sum_x = 0
sum_y = 0
non_transparent_pixel_count = 0
spacing = 5

# for x in range(0,img.get_width(),1):
#     for y in range(0,img.get_height(),1):
#         pixel_color = img.get_at((x, y))   
#         if(pixel_color[3] > 0):
#             p_x = round(x + width/2) 
#             p_y = round(y + height/2)
#             p_x = round((x - img.get_width() // 2) * spacing + width // 2)
#             p_y = round((y - img.get_height() // 2) * spacing + height // 2)

#             particles.append(Particle([p_x,p_y],[0,0],pixel_color,1))
#             sum_x += p_x
#             sum_y += p_y
#             non_transparent_pixel_count += 1
# print(f"non_transparent_pixel_count: {non_transparent_pixel_count}")
# if non_transparent_pixel_count > 0:
#     dragon_center = [sum_x // non_transparent_pixel_count,  sum_y // non_transparent_pixel_count]
#     print(f"Dragon center: {dragon_center}")
# else:
#     print("No non-transparent pixels found!")
# dragon = Body([0,0],dragon_center,particles)


scatter_count = 1000  # The number of particles you want to scatter

# Step 1: Collect all non-transparent pixel positions
non_transparent_pixel_positions = []

for x in range(0, img.get_width()):
    for y in range(0, img.get_height()):
        pixel_color = img.get_at((x, y))

        if pixel_color[3] > 0:  # If pixel is non-transparent
            non_transparent_pixel_positions.append((x, y))

# Step 2: Randomly select positions to scatter particles
scattered_positions = random.sample(non_transparent_pixel_positions, min(scatter_count, len(non_transparent_pixel_positions)))

# Step 3: Place particles at the selected positions
non_transparent_pixel_count = 0
for pos in scattered_positions:
    x, y = pos
    pixel_color = img.get_at((x, y))

    # Calculate position relative to the center and add to particles list
    p_x = round(x + width / 2 - img.get_width() / 2)
    p_y = round(y + height / 2 - img.get_height() / 2)

    particles.append(Particle([p_x, p_y], [0, 0], pixel_color, 1))
    sum_x += p_x
    sum_y += p_y
    non_transparent_pixel_count += 1

print(f"Scattered {non_transparent_pixel_count} particles.")


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
            elif event.key == pygame.K_SPACE:
                pass
            elif event.key == pygame.K_LEFT:
                pass
            elif event.key == pygame.K_RIGHT:
                pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            print(mouse_pos)
            #print(screen.get_at(mouse_pos))

    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
    # Fill background with black
    screen.fill(black)
    screen.blit(fps_text,(0,0))
    #screen.blit(img,(0,0)) 

    for p in particles:
        p.draw(screen)
 
    frames += 1
    # for x in range(0,10000,1):
    #     pygame.draw.circle(screen, (255,0,0),[round(random.uniform(0,800)),round(random.uniform(0,600))],2)


    # Update display
    pygame.display.flip()

pygame.quit()
sys.exit()
