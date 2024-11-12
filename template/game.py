import pygame
import sys

from scripts.utils import load_image, load_images
#from scripts.entities import PhysicsEntity
#from scripts.particles 

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('title')

        self.width, self.height = 640, 480
        self.screen = pygame.display.set_mode((self.width, self.height))


        self.clock = pygame.time.Clock()

        self.assets = {


        }
        self.font = pygame.font.Font(None, 40)



    def run(self):
        running = True
        frames = 0
        while running:
            dt = self.clock.tick(60)/1000

            fps_text = self.font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))

            self.screen.fill('black')
            screen.blit(fps_text,(0,0))
        



            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        pass
                    if event.key == pygame.K_RIGHT:
                        pass
                    if event.key == pygame.K_UP:
                        pass

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        pass
                    if event.key == pygame.K_RIGHT:
                        pass
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    print(mouse_pos)
                    #print(screen.get_at(mouse_pos))

          

            
            frames += 1
            pygame.display.update()
            #tick here?

Game().run()
