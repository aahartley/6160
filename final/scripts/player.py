import pygame
import scripts.utils as utils
import math
import scripts.animations as ani
import scripts.projectiles as proj
class Character(pygame.sprite.Sprite):
    
 
    def __init__(self, position, scale):
        super().__init__()

        self.animations = {
            'idle': ani.Animation(utils.player_paths[0], utils.player_shadow_paths[0], utils.sprite_frame_dict(4, 4, 320, 320), 30, False, 0),
            'walk': ani.Animation(utils.player_paths[1], utils.player_shadow_paths[1], utils.sprite_frame_dict(4, 6, 320, 320), 60, False, 0),
            'attack': ani.Animation(utils.player_paths[2],utils.player_shadow_paths[2], utils.sprite_frame_dict(4, 6, 320, 320), 100, False, 0),#100
            'dead': ani.Animation(utils.player_paths[3], utils.player_shadow_paths[3], utils.sprite_frame_dict(5, 6, 320, 320), 30, False, 0),

        }
        self.attack_animations = {
            #'basic_arrow_attack': ani.Animation(utils.prop_paths[0], utils.prop_paths[0],utils.sprite_frame_dict(1,1,1024,1024), 60, True, 0.20),
            'basic_arrow_attack': utils.scale_image(utils.load_image("Props/1024x1024/Arrow_Far/Arrow_Far_000.png"), 0.2)

        }
        self.projectiles = []
        self.current_animation = self.animations['idle']
        self.image, self.shadow_image = self.current_animation.get_current_frames()
        self.position = pygame.Vector2(position) 
        self.speed = 300
        self.target_position = None
        self.right_click_held = False
        self.state = 'idle'     
        self.angle = 0
        self.real_angle = 90
        self.rect = self.image.get_rect()
        self.aa_rect = self.image.get_bounding_rect()
        # self.rect.centerx = position[0]
        # self.rect.centery = position[1]
        self.aa_rect.centerx = self.position[0]
        self.aa_rect.centery = self.position[1]    
        self.mask = pygame.mask.from_surface(self.image)
        self.local_centroid = pygame.Vector2(self.mask.centroid())
        self.alive = True
        self.last_draw = False

        self.speed_time = 0
        self.boost = False
        self.boost_cd = 0
        self.b_cd = False

        self.flash_cd = 0
        self.f_cd = False

    def change_state(self, state, reset):
        if reset and self.state != state and self.state != 'dead':
            self.animations[self.state].reset()
        if self.state != 'dead':
            self.state = state
            self.current_animation = self.animations[self.state]

    def update(self, dt):
        for p in self.projectiles:
            p.update(dt)
        self.projectiles = [p for p in self.projectiles if not p.hit]
        if(self.boost):
            self.speed_time += dt
            if(self.speed_time > 5):
                self.speed_time = 0
                self.boost = False
                self.speed = 300
                self.b_cd = True
        if(self.b_cd):
            self.boost_cd += dt
            if(self.boost_cd >= 5):
                self.b_cd = False
                self.boost_cd = 0
        if(self.f_cd):
            self.flash_cd += dt
            if(self.flash_cd >= 5):
                self.f_cd = False
                self.flash_cd = 0

        if self.state == 'dead':
            if self.current_animation.check_loop():
                self.current_animation.active = False
                #self.change_state('idle', True)
                self.last_draw = True

        elif self.state == 'attack':
            if(self.current_animation.frame >=15):
                if len(self.projectiles) > 0:
                    self.projectiles[-1].fire = True
            if self.current_animation.check_loop():
                self.change_state('idle', True)

        elif self.target_position:
                direction_vector = pygame.Vector2(self.target_position - self.position)
                #print(direction_vector)
                if direction_vector.length() > 0: 
                    self.angle = self.calculate_angle(self.position, self.target_position)
                    direction = direction_vector.normalize()  
                    distance_to_move = self.speed * dt 
                    distance_to_target = self.position.distance_to(self.target_position)

            
                    if distance_to_move >= distance_to_target:
                        self.position = self.target_position 
                        self.target_position = None 
                        self.change_state('idle', True)

                    else:
                        self.position += direction * distance_to_move 
                        self.change_state('walk', False)
                        
        self.current_animation.update( dt, self.angle)       
        self.image, self.shadow_image = self.current_animation.get_current_frames()

        self.aa_rect = self.image.get_bounding_rect()
        self.aa_rect.center = self.position
        self.mask = pygame.mask.from_surface(self.image)
        #print(self.mask.get_size())
        self.local_centroid = pygame.Vector2(self.mask.centroid())  # local space
        self.local_centroid[1] += 10
        self.drawing_rect = self.image.get_rect()
        #distance from pos to (0,0) topleft corner
        offset_x = self.position[0] - self.local_centroid[0]
        offset_y = self.position[1] - self.local_centroid[1]

        self.rect.x = offset_x
        self.rect.y = offset_y
     

    def draw(self, screen):
        for p in self.projectiles: #put this in render list???
            p.draw(screen)
       

        screen.blit(self.shadow_image, self.rect)
        screen.blit(self.image, self.rect)
        if self.last_draw:
            self.alive = False
        # mask_surface = self.mask.to_surface(unsetcolor=(0, 0, 0))  
        # mask_surface.set_colorkey((0, 0, 0))  
        # screen.blit(mask_surface, self.rect)

        #pygame.draw.line(screen, (0, 255, 0), p.position, p.target_position)

        # pygame.draw.circle(screen, (255, 0, 0), self.position, 3) 
        #pygame.draw.circle(screen, (0, 255, 0), (self.drawing_rect.x + self.local_centroid[0], self.drawing_rect.y + self.local_centroid[1]-30), 3)


    
    def reset(self):
        self.change_state("idle", True)
        self.speed = 300
        self.position = pygame.Vector2(800, 450)
        self.speed_time = 0
        self.boost = False
        self.boost_cd = 0
        self.b_cd = False

        self.flash_cd = 0
        self.f_cd = False
        self.alive = True
        self.last_draw = False
        self.target_position = None
        self.right_click_held = False
        self.state = 'idle'     
        self.angle = 0
        self.real_angle = 90
        self.rect = self.image.get_rect()
        self.aa_rect = self.image.get_bounding_rect()
        # self.rect.centerx = position[0]
        # self.rect.centery = position[1]
        self.aa_rect.centerx = self.position[0]
        self.aa_rect.centery = self.position[1]    
        self.mask = pygame.mask.from_surface(self.image)
        self.local_centroid = pygame.Vector2(self.mask.centroid())
        self.projectiles.clear()

    def handle_event(self, event):
        if self.alive:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    mouse_pos = pygame.mouse.get_pos()
                    self.target_position = pygame.Vector2(mouse_pos)
                    self.right_click_held = True  

            elif event.type == pygame.MOUSEMOTION and self.right_click_held:
                mouse_pos = pygame.mouse.get_pos()
                self.target_position = pygame.Vector2(mouse_pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    self.right_click_held = False
            

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                        self.change_state('idle', True)
                        self.target_position = None
                if event.key == pygame.K_a:
                        if self.state != 'attack':
                            mouse_pos = pygame.mouse.get_pos()
                            self.angle = self.calculate_angle(pygame.Vector2(self.aa_rect.center), mouse_pos)
                            self.real_angle = self.calc_real_angle(pygame.Vector2(self.aa_rect.center), mouse_pos)
                            #print(self.angle)
                            #print(self.real_angle)
                           
                            #self.projectiles.append(proj.Projectile(self.attack_animations['basic_arrow_attack'].copy(), pygame.Vector2(self.rect.center), mouse_pos, self.bow_world))
                            test = pygame.Vector2((self.rect.x + self.local_centroid[0], self.rect.y + self.local_centroid[1]-30))
                            self.projectiles.append(proj.Projectile(self.attack_animations['basic_arrow_attack'].copy(), pygame.Vector2(test), mouse_pos))

                        self.change_state('attack', False)
                        self.target_position = None
                if event.key == pygame.K_f:
                    if not self.f_cd:
                        self.f_cd = True
                        mouse_pos = pygame.mouse.get_pos()
                        target = pygame.Vector2(mouse_pos)
                        dist =  self.position.distance_to(target)

                        if dist > 300:
                            direction = (target - self.position).normalize()  
                            if direction.length() > 0: 
                                target = self.position + direction * 300  

                        self.position = target
                if event.key == pygame.K_d:
                    if not self.boost and not self.b_cd:
                        self.boost = True
                        self.speed *= 1.5
               
 
    def calculate_angle(self, position, target_position):
            direction_vector = target_position - position
            radians = math.atan2(direction_vector.y, direction_vector.x)  
            angle = math.degrees(radians) % 360  
            angle = (angle+90) % 360
            return angle


    def calc_real_angle(self, position, target_position):
        direction_vector = target_position - position
        radians = math.atan2(-direction_vector.y, direction_vector.x)
        angle = (90- math.degrees(radians) ) % 360 
        return angle

