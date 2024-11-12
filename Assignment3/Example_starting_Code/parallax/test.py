import pygame

pygame.init()

clock = pygame.time.Clock()

FPS = 60

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 432

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Class 12 Parallax Effect")


#define game variables
scroll = 0

ground_image = pygame.image.load("BG1/ground.png").convert_alpha()

#load images
bg_images = []
for i in range(0,4):
	bg_image = pygame.image.load(f"BG1/IMG_{i}.png").convert_alpha()
	bg_images.append(bg_image)
	
bg_width = bg_images[0].get_width()	
ground_width = ground_image.get_width()	
ground_height = ground_image.get_height()	


def draw_bg():
	for x in range(5):
		speed = 1		
		screen.blit(bg_images[0],((x*bg_width-scroll*speed,0)))
		screen.blit(bg_images[1],((x*bg_width-scroll*speed,0)))
		screen.blit(bg_images[2],((x*bg_width-scroll*speed,150)))
		screen.blit(bg_images[3],((x*bg_width-scroll*speed,150)))
		speed +=0.2

def draw_ground():
	for x in range(5):	
		screen.blit(ground_image, ((x * ground_width) - scroll*2, 300))

run = True
while run:
	clock.tick(FPS)
	
	draw_bg()
	draw_ground()
	
	key = pygame.key.get_pressed()
	
	if key[pygame.K_LEFT]and scroll>0:
		scroll -=5

	if key[pygame.K_RIGHT]and scroll<3000:
		scroll +=5	
	
	for event in pygame.event.get():
		if(event.type == pygame.QUIT):
			run = False
	
	pygame.display.update()

pygame.quit()
