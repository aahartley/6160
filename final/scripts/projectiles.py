import pygame
import scripts.animations as ani
import math
import scripts.utils as utils
class Projectile(pygame.sprite.Sprite):
    def __init__(self, attack_animation, pos, mouse_pos):
        super().__init__()

        #self.attack_animation = attack_animation
        #self.image, self.shadow_image = self.attack_animation.get_current_frames()
        #self.mask = pygame.mask.from_surface(self.image)
        #self.rect = self.image.get_bounding_rect()
        self.position = pos
        #self.position[1] -=30

        self.speed = 500
        self.target_position = pygame.Vector2(mouse_pos)
        self.angle = self.calculate_angle(self.position, self.target_position)
        self.real_angle = self.calc_real_angle(pos, self.target_position)
        self.sheet = attack_animation
        self.sheet = pygame.transform.rotate(self.sheet, -self.real_angle).convert_alpha()
        self.aa_rect = self.sheet.get_bounding_rect()
        self.aa_rect.centerx = self.position[0]
        self.aa_rect.centery = self.position[1]
        self.mask = pygame.mask.from_surface(self.sheet)

        #print(self.angle)
        self.direction_vector = pygame.Vector2(self.target_position - self.position)
        self.hit = False
        self.fire = False
        self.local_centroid = pygame.Vector2(self.mask.centroid())
        self.local_centroid[0] -= 10
        #self.drawing_rect = self.image.get_rect()
        self.rect = self.sheet.get_rect()
        offset_x = self.position[0] - self.local_centroid[0]
        offset_y = self.position[1] - self.local_centroid[1] 
        self.rect.x = offset_x
        self.rect.y = offset_y
    
    def update(self, dt):
        #print(direction_vector)
        if self.fire and not self.hit:
            if self.direction_vector.length() > 0:  
                direction = self.direction_vector.normalize() 
                distance_to_move = self.speed * dt  
                distance_to_target = self.position.distance_to(self.target_position)

                if distance_to_move >= distance_to_target:
                    self.position = self.target_position
                    self.hit = True
                    #self.hit = False
                    #self.target_position = None  

                else:
                    self.position += direction * distance_to_move
            #self.attack_animation.update(dt, self.angle)      
            #self.image, self.shadow_image = self.attack_animation.get_current_frames()
            #self.mask = pygame.mask.from_surface(self.image)

            #self.rect = self.image.get_bounding_rect()
            #self.rect.center = self.position
            self.aa_rect = self.sheet.get_bounding_rect()
            self.aa_rect.center = self.position
            self.mask = pygame.mask.from_surface(self.sheet)

            self.local_centroid = pygame.Vector2(self.mask.centroid())  # local space
            #self.local_centroid[0] += 10
            #self.drawing_rect = self.image.get_rect()
            self.rect = self.sheet.get_rect()

            #distance from pos to (0,0) topleft corner
            offset_x = self.position[0] - self.local_centroid[0]
            offset_y = self.position[1] - self.local_centroid[1] 

            self.rect.x = offset_x
            self.rect.y = offset_y

#might need to pos arrow to more center to curosr??
    def draw(self, screen):
        if self.fire and not self.hit:
        

            # screen.blit(self.shadow_image, self.drawing_rect)
            # screen.blit(self.image, self.drawing_rect)
            #screen.blit(self.sheet, self.drawing_rect)
            screen.blit(self.sheet, self.rect)
                
            # mask_surface = self.mask.to_surface(unsetcolor=(0, 0, 0))  # Use a color that won't show up in your game
            # mask_surface.set_colorkey((0, 0, 0))  # Set the color to be transparent
            # screen.blit(mask_surface, self.rect)
            #pygame.draw.rect(screen, (0,255,0),self.rect , 1)
            #pygame.draw.rect(screen, (0,255,0),self.drawing_rect , 1)
            #pygame.draw.circle(screen, (0, 255, 0), (self.drawing_rect.x + self.local_centroid[0], self.drawing_rect.y + self.local_centroid[1]), 3)

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

