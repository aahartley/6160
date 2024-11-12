import pygame

pygame.init()

clock = pygame.time.Clock()

FPS = 60

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 432

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Class 12 Parallax Effect")


#define game variables
starts = [0,0,0,0,0]
ys = [0,0,150,150,300]
speed = 5
speed_modifiers = [1, 1.25, 1.5, 1.75, 2] 

#draw ground image
ground_image = pygame.image.load("BG1/ground.png").convert_alpha()

#load images
bg_images = []

#load image sequences
for i in range(0,4):
	bg_image = pygame.image.load(f"BG1/IMG_{i}.png").convert_alpha()
	bg_images.append(bg_image)
	
bg_width = bg_images[0].get_width()	
ground_width = ground_image.get_width()	
ground_height = ground_image.get_height()	

#draw background images 
def draw_bg():
    for i, img in enumerate(bg_images):
        screen.blit(img, (starts[i] - bg_width, ys[i]))
        screen.blit(img, (starts[i], ys[i]))
        screen.blit(img, (starts[i] + bg_width, ys[i]))


	
#draw background
def draw_ground():
	for i in range(3):
		screen.blit(ground_image, (starts[4] +(i-1)*bg_width, ys[4]))


run = True
start = 0
start2 =0
while run:
	clock.tick(FPS)
	draw_bg()
	draw_ground()

	
	#input data. Left and right keys to create the parallax effect
	key = pygame.key.get_pressed()	
	if key[pygame.K_LEFT]:
		for i in range(len(starts)):
			starts[i] += speed * speed_modifiers[i]

	if key[pygame.K_RIGHT]:
		for i in range(len(starts)):
			starts[i] -= speed * speed_modifiers[i]

	for event in pygame.event.get():
		if(event.type == pygame.QUIT):
			run = False
	for i in range(len(starts)):
		if (abs(starts[i]) >= bg_width):
			starts[i]=0

	pygame.display.update()

pygame.quit()
