import pygame
import sys

pygame.init()
clock = pygame.time.Clock()
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Assignment3")
import parallax
import player
para = parallax.Parallax(screen,"parallax_IMGS/Background_IMGS/", 7, 0, [(0,0), (0,807), (0,624), 
																  (0,805), (0,831), (0,951), (0,1684)])
#character position
player = player.Character((1754, 1675))
#init
para.resize_layers()
player.reposition(para.og_main_width, para.og_main_height, WIDTH, HEIGHT)
# Main loop
run = True
while run:
    dt = clock.tick(30)/1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.VIDEORESIZE:
            #screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            para.resize_layers()
            player.reposition(para.og_main_width, para.og_main_height, event.w, event.h)

            WIDTH = event.w
            HEIGHT = event.h

        para.handle_event(event, dt)
        player.handle_event(event, dt )

    para.update(dt)
    player.update(dt,para)

    screen.fill((0, 0, 0))
    para.draw()
    screen.blit(player.image, player.rect)
    #display aabbs
    # pygame.draw.rect(screen, (0,0,0), (player.position[0], player.position[1],player.rect.width, player.rect.height), 1)
    # pygame.draw.rect(screen, (0,0,0), player.rect, 1)
    # pygame.draw.line(screen, (0,0,0), (WIDTH//2, 0), (WIDTH//2,HEIGHT))
    #pygame.draw.line(screen, (0,0,0), (0, HEIGHT//2), (WIDTH,HEIGHT//2))

    # Update the display
    pygame.display.flip()

pygame.quit()