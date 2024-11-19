import pygame
import sys
import time
from scripts.utils import load_image, load_images, scale_image
from scripts.particles import Particle, ParticleEmitter, BasicParticle
import scripts.sims as sims
import scripts.particle_emitters as pe
import scripts.player as char
import scripts.tiles as tile
import scripts.enemy as en
import scripts.fireball as fb
import random
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Exiled Legends')

        #self.width, self.height = 1280, 720
        self.width, self.height = 1600, 900

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        self.assets = {
            "smoke" : load_image("particles/smoke.png"),
            "fireball" : pygame.transform.smoothscale((load_image('fireball.png')), (40,20)).convert_alpha()
        }
        self.font = pygame.font.Font(None, 36)
        self.particle_emitters = [ParticleEmitter([self.width//2, self.height-100], 100, 1000, self.assets["smoke"])]

        # self.smoke_sim = sims.create_smoke_sim()
        # self.smoke_sim.add_emitter(pe.ParticleEmitter([self.width//2,self.height-100], 'random'))
        self.enemy_sprites = pygame.sprite.Group()
        self.fireball_sprites = pygame.sprite.Group()
        self.projectile_sprites = pygame.sprite.Group()
        
        self.player = char.Character([self.width//2, self.height//2], 0.8)

        self.floor = tile.Tile(self.width, self.height)
        self.enemy_manager = en.EnemyManager(self.enemy_sprites, self.width, self.height, self.floor.find_corners())
        self.fireball_manager = fb.FireballManager(self.fireball_sprites, self.assets['fireball'], self.floor.find_corners())

        self.runnning = False
        self.render_list = []
        self.seconds = 0
        self.current_level = 1
        self.last_level_increase_time = -1 

        self.frames = 0
        self.re = False


    def menu(self):
        menu_loop = True
        while menu_loop:
            self.screen.fill('black')
            menu_msg = "Press space to start"
            menu_text = self.font.render(menu_msg, True, (255,255,255))
            self.screen.blit(menu_text, ((self.width//2)-self.font.size(menu_msg)[0]//2, (self.height//2)- self.font.size(menu_msg)[1]//2))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.running = True
                        menu_loop = False
            pygame.display.update()


    def game_over(self):
        over_loop = True
        while over_loop:
            #self.screen.fill('black')
            over_msg = "Press space to restart"
            over_text = self.font.render(over_msg, True, (255,255,255), (0,0,0))
            self.screen.blit(over_text, ((self.width//2)-self.font.size(over_msg)[0]//2, (self.height//2)- self.font.size(over_msg)[1]//2))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.running = True
                        over_loop = False
                        self.reset()
                        self.re = True
            pygame.display.update()
    def reset(self):
        self.current_level = 1
        self.enemy_manager.reset()
        self.fireball_manager.reset()
        self.player.reset()
        self.seconds = 0
        self.frames = 0

    def run(self):
        self.menu()
        self.frames = 0
        particles = 0
        while self.running:
            dt = self.clock.tick(60)/1000
            if self.re:
                self.reset()
                self.re = False
            if self.frames == 0:
                dt = 0.016

            self.seconds += dt
            if int(self.seconds) % 30 == 0 and self.last_level_increase_time != int(self.seconds) and int(self.seconds) != 0:
                if self.current_level < 3:
                    self.current_level += 1
                    print(self.current_level)
                self.last_level_increase_time = int(self.seconds)  
            fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 255))
            score_text = self.font.render(f"Score: {self.seconds:.2f}", True, (255, 255, 255))
            self.screen.fill((0,0,0))
            self.floor.draw(self.screen)

            self.screen.blit(fps_text,(0,0))
            self.screen.blit(score_text,(1400,0))

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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # mouse_pos = pygame.mouse.get_pos()
                    # print(mouse_pos)
                    pass
                self.player.handle_event(event)
                          
            self.player.update(dt)
            for proj in self.player.projectiles:
                self.projectile_sprites.add(proj)
            self.render_list.append((self.player.position[1],self.player))
            #pygame.draw.rect(self.screen, (255,0,0), self.player.rect, 1)
            # pygame.draw.line(self.screen, (255,0,0), (self.player.rect.width//2+self.player.rect.x,self.player.rect.y ), (self.player.rect.width//2+self.player.rect.x,self.player.rect.y + self.player.rect.height))
            # pygame.draw.line(self.screen, (255,0,0), (self.player.rect.x, self.player.rect.height//2+self.player.rect.y), (self.player.rect.x + self.player.rect.width,self.player.rect.height//2+self.player.rect.y))
            #print(self.player.rect)
            # pos = pygame.Rect((self.player.position[0], self.player.position[1],320,320))

            # pos.center = self.player.position
            #pygame.draw.rect(self.screen, (0,255,0),pos , 1)
            # if self.player.target_position != None:
            #     pygame.draw.line(self.screen, (0,255,0), self.player.position, self.player.target_position)

            # pygame.draw.line(self.screen, (255,0,0), (self.width//2, 0), (self.width//2,self.height))
            # pygame.draw.line(self.screen, (255,0,0), (0, self.height//2), (self.width,self.height//2))

            self.enemy_manager.update(dt, self.render_list, self.player.position, self.seconds, self.current_level)
            self.fireball_manager.update(dt, self.render_list, self.seconds)
    

            collisions_epr = pygame.sprite.groupcollide(self.enemy_sprites, self.projectile_sprites, False, False, collided=pygame.sprite.collide_mask) 
            if collisions_epr:
                #print("epr")
                for enemy, projectiles in collisions_epr.items():
                        #print("Mask collision detected! epr")
                        enemy.hit()
                        if enemy.state == "dead":
                            enemy.kill()
                        for projectile in projectiles:
                            #self.player.projectiles.remove(projectile)
                            projectile.hit = True
                            projectile.kill()
            collisions_pf = pygame.sprite.spritecollide(self.player, self.fireball_sprites, False, collided=pygame.sprite.collide_mask) 
            if collisions_pf:
                for fire in collisions_pf:
                    #print("Mask collision detected! pf")
                    #self.player.alive = False
                    #self.fireball_manager.fireball_list.remove(fire)
                    fire.kill()
                    self.player.change_state('dead', True)
                    self.player.target_position = None
            collisions_pe = pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, collided=pygame.sprite.collide_mask) 
            if collisions_pe:
                #print("pe")
                #self.enemy_manager.spawn = False
                for e in collisions_pe:
                        #print("Mask collision detected! pe")
                        #self.player.alive = False
                        e.change_state('attack', True)
                        e.kill()
                        self.player.change_state('dead', True)
                        
            #sort by y                
            self.render_list.sort(key=lambda obj: obj[0])

            for _, obj in self.render_list:
                obj.draw(self.screen)
            self.render_list.clear()
            self.projectile_sprites.empty()
            # self.enemy_sprites.empty()
            # self.fireball_sprites.empty()

            if not self.player.alive:
                self.game_over()


            # start_time = time.time()  # Start timer
            # self.smoke_sim.update(dt)
            # self.smoke_sim.draw(self.screen)
            # end_time = time.time()  # End timer
            # smoke_sim_time += end_time-start_time

            # start_time = time.time()  # Start timer
            # for pe in self.particle_emitters:
            #     pe.update(dt)
            #     for p in pe.particles:
            #         p.update(dt)
            #         p.draw(self.screen)
            #         particles += 1
            # end_time = time.time()  # End timer
            # smoke_sim_time += end_time-start_time
   
       
            #particle_text = self.font.render(f"Particles: {self.smoke_sim.get_nb()}", True, (255, 255, 255))
            #particle_text2 = self.font.render(f"Particles: {particles}", True, (255, 255, 255))

            #self.screen.blit(particle_text,(0,30))
            #self.screen.blit(particle_text2,(0,30))
            particles = 0
    

            self.frames += 1
    
            pygame.display.update()
Game().run()
