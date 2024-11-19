import pygame
import scripts.utils as utils
import math
import scripts.animations as ani
import random
class EnemyManager:
    def __init__(self, group, width, height, corners):
        self.enemy_list = []
        self.group = group
        self.width = width
        self.height = height
        self.corners = corners
        self.animations = {
            'idle': ani.Animation(utils.enemy_paths[0], utils.enemy_shadow_paths[0], utils.sprite_frame_dict(5, 4, 256, 256), 30, False,0),
            'walk': ani.Animation(utils.enemy_paths[1], utils.enemy_shadow_paths[1], utils.sprite_frame_dict(5, 4, 256, 256), 60, False, 0),
            'attack': ani.Animation(utils.enemy_paths[2],utils.enemy_shadow_paths[2], utils.sprite_frame_dict(5, 4, 256, 256), 100, False, 0),
            'dead' : ani.Animation(utils.enemy_paths[3], utils.enemy_shadow_paths[3], utils.sprite_frame_dict(4, 6, 256, 256), 30, False, 0)
        }
        self.last_spawn_time = -1 
        self.level_info = {
            1: {"health":1, "speed":100},
            2: {"health":2, "speed":125},
            3: {"health":3, "speed":150},

        }
        self.spawn = True
    
    def reset(self):
        self.group.empty()
        self.enemy_list.clear()
        self.last_spawn_time = -1


    def fresh_animation(self):
        return {key: animation.copy() for key, animation in self.animations.items()}

    def update(self,dt, render_list, p_position, secs, current_level):  
        if int(secs) % 1 == 0 and int(secs) != 0 and int(secs) != self.last_spawn_time:
            if self.spawn: 
                self.add_enemy(current_level)
                self.last_spawn_time = int(secs)  

        self.enemy_list = [e for e in self.enemy_list if e.alive]

        for e in self.enemy_list:
            e.update(dt, p_position)
            render_list.append((e.aa_rect.topleft[1] + e.aa_rect.height,e))

    def add_enemy(self, current_level ):
        edges = [
            (self.corners[0], self.corners[1]),  
            (self.corners[1], self.corners[3]),  
            (self.corners[2], self.corners[3]),  
            (self.corners[0], self.corners[2])   
        ]
        edge = random.choice(edges)

        t = random.random()
        x = int(edge[0][0] * (1 - t) + edge[1][0] * t)
        y = int(edge[0][1] * (1 - t) + edge[1][1] * t)
        enemy = Enemy([x, y], self.fresh_animation(), self.level_info, current_level)
        self.enemy_list.append(enemy)
        self.group.add(enemy)

class Enemy(pygame.sprite.Sprite):
 
    def __init__(self, position, animations, level_info, level):
        super().__init__()

        self.animations = animations
        self.current_animation = self.animations['idle']
        self.image, self.shadow_image = self.current_animation.get_current_frames()
        self.position = pygame.Vector2(position) 
        self.speed = level_info[level]["speed"]
        self.target_position = None
        self.state = 'idle'     
        self.angle = 0
        self.real_angle = 90
        self.rect = self.image.get_rect()
        self.aa_rect = self.image.get_bounding_rect()
        self.aa_rect.centerx = self.position[0]
        self.aa_rect.centery = self.position[1]   
        self.mask = pygame.mask.from_surface(self.image)
    
        self.local_centroid = pygame.Vector2(self.mask.centroid())
        self.alive = True
        self.last_draw = False
        self.health = level_info[level]["health"]
        self.chase = True


    def change_state(self, state, reset):
        if reset and self.state != state and self.state != 'dead':
            self.animations[self.state].reset()
        if self.state != 'dead':
            self.state = state
            self.current_animation = self.animations[self.state]    

    def update(self, dt, target_position):
        if self.alive and self.chase:
            self.target_position = target_position
            if self.state == 'dead':
                if self.current_animation.check_loop():
                    self.current_animation.active = False
                    self.last_draw = True
            elif self.state == 'attack':
                if self.current_animation.check_loop():
                    self.change_state('idle', True)
                    self.chase = False

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

            self.mask = pygame.mask.from_surface(self.image)
            self.aa_rect = self.image.get_bounding_rect()
            self.aa_rect.center = self.position
            self.local_centroid = pygame.Vector2(self.mask.centroid())  # local space
            self.local_centroid[1] += 10
            self.rect = self.image.get_rect()
            #distance from pos to (0,0) topleft corner
            offset_x = self.position[0] - self.local_centroid[0]
            offset_y = self.position[1] - self.local_centroid[1]

            self.rect.x = offset_x
            self.rect.y = offset_y
            

    def draw(self, screen):
        if self.alive:
            screen.blit(self.shadow_image, self.rect)
            screen.blit(self.image, self.rect)
            if self.last_draw:
                self.alive = False
            # mask_surface = self.mask.to_surface(unsetcolor=(0, 0, 0))  # Use a color that won't show up in your game
            # mask_surface.set_colorkey((0, 0, 0))  # Set the color to be transparent
            # screen.blit(mask_surface, self.rect)

            #pygame.draw.line(screen, (0, 255, 0), p.position, p.target_position)

            # pygame.draw.circle(screen, (255, 0, 0), self.position, 3) 
            #pygame.draw.circle(screen, (0, 255, 0), (self.drawing_rect.x + self.local_centroid[0], self.drawing_rect.y + self.local_centroid[1]-30), 3)


    
    def hit(self):
        self.health = self.health -1
        if self.health <= 0:
            self.change_state('dead', True)



    def handle_event(self, event):
        pass

 
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

