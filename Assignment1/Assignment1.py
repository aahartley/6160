import pygame
import sys
from math import radians 

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Austin Hartley - Assignment1')

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
human_surface = pygame.Surface((width, height), pygame.SRCALPHA)
skyline_surface = pygame.Surface((width, height), pygame.SRCALPHA)

# Function to save the current screen as a PNG image
def save_screenshot(filename='Hartley_Assignment1.png'):
    pygame.image.save(screen, filename)
    print(f"Screenshot saved as {filename}")

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save_screenshot()  # Save screenshot when 'S' key is pressed
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            print(mouse_pos)
            #print(screen.get_at(mouse_pos))
    #print(clock.get_fps()) #test to see how slow 
    # Fill background with black
    screen.fill(black)
    human_surface.fill((0,0,0,0))

    #skyline
    pygame.draw.rect(skyline_surface, night_sky, (0, 0, 800, 400))
    # Draw a transparent dark film rectangle
    pygame.draw.rect(alpha_surface, transparent_black, (0, 0, 800, 400))
    skyline_surface.blit(alpha_surface, (0, 0))
    # MOON
    pygame.draw.circle(skyline_surface, white, (700, 100), 25)
    pygame.draw.circle(skyline_surface,darker_sky, (690, 100), 22)
    #bulding
    pygame.draw.rect(skyline_surface, dim_gray, (200, 150, 400, 250))
    #door
    pygame.draw.rect(skyline_surface, door, (500, 300, 50, 100))
    pygame.draw.circle(skyline_surface, yellow, (543,350), 5)
    #window
    pygame.draw.rect(skyline_surface, glass, (500, 200, 40, 40))
    pygame.draw.rect(skyline_surface, black, (500, 220, 40, 5))
    pygame.draw.rect(skyline_surface, black, (518, 200, 5, 40))

    screen.blit(skyline_surface,(0,0))

    # sand
    pygame.draw.rect(screen, dark_beige, (0, 400, 800, 100))
    #water
    pygame.draw.rect(screen, blue_water, (0, 500, 800, 100))

    #neck
    pygame.draw.rect(human_surface, dark_beige, (389, 278, 13,12))
    # head
    pygame.draw.circle(human_surface, dark_beige, (395, 255), 28)
    #left eye
    pygame.draw.polygon(human_surface, white, [(372, 251),(377, 246),(385, 246),(390, 251)])
    pygame.draw.circle(human_surface, black, (382, 249), 3)
    #right eye
    pygame.draw.polygon(human_surface, white, [(399, 251),(404, 246),(412, 246),(417, 251)])
    pygame.draw.circle(human_surface, black, (409, 249), 3)
    #nose
    pygame.draw.aalines(human_surface, black,False, [(394, 256),(400, 265),(397, 267)])
    #mouth
    pygame.draw.arc(human_surface, black, (385,258,25,20),radians(200),radians(340))
    #torso
    pygame.draw.polygon(human_surface, red, [(391, 289),(368, 298),(376, 364),(414, 364),(422, 298),(399, 289)] )
    #left arm
    pygame.draw.polygon(human_surface, red, [(369, 315),(364, 318),(343, 330),(363, 355),(357, 360),(326, 330),(369, 299)])
    #left hand
    pygame.draw.ellipse(human_surface, dark_beige, (356, 355, 20, 10))
    #right arm
    pygame.draw.polygon(human_surface, red, [(420, 315),(426, 318),(447, 330),(427, 355),(433, 360),(464, 330),(422, 299)])
    #right hand
    pygame.draw.ellipse(human_surface, dark_beige, (413, 355, 20, 10))
    #waist
    waist_vert = [(376, 365),(368, 395),(395, 410),(422, 395),(414, 365)]
    pygame.draw.polygon(human_surface, blue, waist_vert )
    #left foot
    pygame.draw.ellipse(human_surface, black, (340, 465, 40, 20))
    #right foot
    pygame.draw.ellipse(human_surface, black, (410, 465, 40, 20))
    #left leg
    pygame.draw.polygon(human_surface, blue,[(368, 395),(358, 427),(355, 469),(377, 472),(378, 444),(394, 409)] )
    #right leg
    pygame.draw.polygon(human_surface, blue, [(422, 394),(432, 427),(435, 469),(413, 472),(412, 444),(396, 409)])
    screen.blit(human_surface,(0,0))

    #reflection
    reflection_surface2 = pygame.transform.flip(skyline_surface.subsurface(0,120,800,100), False, True)
    reflection_surface2.set_alpha(128)
    scaled_surface2 = pygame.transform.smoothscale(reflection_surface2, (reflection_surface2.get_width() // 10, reflection_surface2.get_height() // 10))
    scaled_surface2 = pygame.transform.smoothscale(scaled_surface2, (reflection_surface2.get_width(), reflection_surface2.get_height()))
    screen.blit(scaled_surface2, (0, 500))

    reflection_surface = pygame.transform.flip(human_surface.subsurface(0,365,800,100), False, True)
    reflection_surface.set_alpha(128)
    scaled_surface = pygame.transform.smoothscale(reflection_surface, (reflection_surface.get_width() // 10, reflection_surface.get_height() // 10))
    scaled_surface = pygame.transform.smoothscale(scaled_surface, (reflection_surface.get_width(), reflection_surface.get_height()))
    screen.blit(scaled_surface, (0, 500))


    #water
    rect_surface = pygame.Surface((800, 100), pygame.SRCALPHA)  # Create a new transparent surface
    pygame.draw.rect(rect_surface , (blue_water[0],blue_water[1], blue_water[2],179), (0, 0, 800, 100))
    pygame.draw.rect(rect_surface , (black[0],black[1], black[2],179), (0, 0, 800, 3))
    # pygame.draw.ellipse(rect_surface, (white[0],white[1],white[2],255), (360, 45, 80, 30),1)
    # pygame.draw.ellipse(rect_surface, (white[0],white[1],white[2],255), (330, 30, 140, 60),1)
    # pygame.draw.ellipse(rect_surface, (white[0],white[1],white[2],255), (310, 20, 180, 80),1)
    # pygame.draw.ellipse(rect_surface, (white[0],white[1],white[2],255), (290, 10, 220, 100),1)
    # pygame.draw.ellipse(rect_surface, (white[0],white[1],white[2],255), (250, 25, 400, 100),1)
    # pygame.draw.ellipse(rect_surface, (white[0],white[1],white[2],255), (130, 10, 600, 160),1)
    # pygame.draw.ellipse(rect_surface, (white[0],white[1],white[2],255), (50, 5, 750, 200),1)
    # pygame.draw.ellipse(rect_surface, (white[0],white[1],white[2],255), (10, 1, 880, 220),1)
    scaled_surface3 = pygame.transform.smoothscale(rect_surface, (rect_surface.get_width() // 2, rect_surface.get_height() // 2))
    scaled_surface3 = pygame.transform.smoothscale(scaled_surface3, (rect_surface.get_width(), rect_surface.get_height()))
    screen.blit(scaled_surface3,(0,500))



    #sand
    pygame.draw.rect(screen, grass, (0, 400, 800, 100))
    pygame.draw.rect(screen, brown, (0, 490, 800, 10))
    #redraw what was covered
    screen.blit(human_surface.subsurface((0,400,800,100)),(0,400))

    # Update display
    pygame.display.flip()

pygame.quit()
sys.exit()
