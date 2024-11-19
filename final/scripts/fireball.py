import pygame 
import random
import noise
import math


class FireballManager:
    def __init__(self, group, img, corners):
        self.fireball_surface = FireballSurface(img)
        self.group = group
        self.fireball_list = []
        self.corners = corners
        # for i in range(0):
        #     fireball = Fireball(self.fireball_surface.surface, [1500, random.randint(0,900)])
        #     self.fireball_list.append(fireball)
        #     self.group.add(self.fireball_list[-1])
        self.last_spawn_time = -1 
        self.spawn_interval = 0.5
        self.spawned_this_interval = False  
    
    def reset(self):
        self.group.empty()
        self.fireball_list.clear()
        self.last_spawn_time = -1 
        self.spawn_interval = 0.5
        self.spawned_this_interval = False  

    def add_fireball(self):
        edges = [
            ((0, 0), (1600, 0)),  # Top edge
            ((1600, 0), (1600, 900)),  # Right edge
            ((1600, 900), (0, 900)),  # Bottom edge
            ((0, 900), (0, 0))   # Left edge
        ]

        inward_normals = [
            pygame.Vector2(0, 1),   # Top edge (points down)
            pygame.Vector2(-1, 0),  # Right edge (points left)
            pygame.Vector2(0, -1),  # Bottom edge (points up)
            pygame.Vector2(1, 0)    # Left edge (points right)
        ]

        index = random.randint(0, 3)
        edge = edges[index]
        normal = inward_normals[index]

        t = random.random()  
        x = int(edge[0][0] * (1 - t) + edge[1][0] * t)
        y = int(edge[0][1] * (1 - t) + edge[1][1] * t)

        fireball = Fireball(self.fireball_surface.surface, [x, y], normal)
        self.fireball_list.append(fireball)
        self.group.add(fireball)

    def update(self,dt, render_list, secs):
        self.fireball_surface.update(dt)

        time_since_last_spawn = secs - self.last_spawn_time

        if time_since_last_spawn >= self.spawn_interval:
            self.spawned_this_interval = False
            self.last_spawn_time = secs  # Update the last spawn time

        if time_since_last_spawn < self.spawn_interval and not self.spawned_this_interval:
            self.add_fireball()
            self.spawned_this_interval = True 

        self.fireball_list = [fb for fb in self.fireball_list if fb.alive]

        for fire in self.fireball_list:
                fire.update(dt)
                render_list.append((fire.fireball_pos[1],fire))


class FireballSurface:
    def __init__(self, image):
        self.image = image
        self.noise_scale = 0.2
        self.noise_offset_x = random.randint(0, 1000)
        self.noise_offset_y = random.randint(0, 1000) #prob delte
        self.noise_animation_speed = 25  

        self.FIRE_GRADIENT = [
            (120, 40, 0),     # Dark red
            (255, 69, 0),     # Orange red
            (255, 140, 0),    # Orange
            (255, 255, 0),    # Yellow
            (255, 255, 200)   # Bright yellow 
        ]
        self.time = 0
        self.surface = pygame.Surface((self.image.width, self.image.height), pygame.SRCALPHA).convert_alpha()
        self.original_colors = []
        # self.w = 0
        # self.widths = []
        # self.h = 0
        # for y in range(self.image.height):
        #     row_good = False
        #     for x in range(self.image.width):
        #          color = self.image.get_at((x, y))
        #          if color[3] !=255:
        #             self.original_colors.append(color)
        #             self.w += 1
        #             row_good = True
        #     self.widths.append(self.w)
        #     self.w = 0
        #     if row_good:
        #         self.h += 1
        # self.w = max(self.widths)
        for y in range(self.image.height):
            for x in range(self.image.width):
                color = self.image.get_at((x, y))
                self.original_colors.append(color)
    
    def get_fire_color(self, value):
        index = int(value * (len(self.FIRE_GRADIENT) - 1))
        return self.FIRE_GRADIENT[index]

    def update(self, dt):
        width, height = self.image.get_size()
        #print(width, height, self.w, self.h)
        for y in range(height):
            for x in range(width):
                nx = self.noise_offset_x + x * self.noise_scale
                ny = self.noise_offset_y + y * self.noise_scale
                animated_value = noise.pnoise2(nx+-self.time * self.noise_animation_speed, ny)

                # -1 to 1 to 0 to 1
                normalized_value = (animated_value + 1) / 2

                fire_color = self.get_fire_color(normalized_value)

                #original_color = self.image.get_at((x, y))
                #original_color = self.original_colors[y*self.w + x]
                original_color = self.original_colors[y*width + x]
                new_color = (
                    min(255, (original_color.r + fire_color[0]) // 2),
                    min(255, (original_color.g + fire_color[1]) // 2),
                    min(255, (original_color.b + fire_color[2]) // 2),
                    original_color.a  
                )
                if(x < 10) or original_color[3] == 255: #32
                    self.surface.set_at((x,y),original_color)
                else:
                    self.surface.set_at((x, y), new_color)
        self.time += dt
        if self.time > 100:
            self.time = 0
       




class Fireball(pygame.sprite.Sprite):
    def __init__(self, surface, pos, direction):
        super().__init__()

        self.surface = surface
        self.fireball_pos = pygame.Vector2(pos)
        self.fireball_radius = 0
        self.fireball_speed = 400
        self.direction = pygame.Vector2(direction)  # Unit vector of the direction

        #self.draw_surface = pygame.transform.smoothscale(self.surface,(80,40)).convert_alpha()
        self.angle = self.calculate_angle(self.direction)
        self.draw_surface = pygame.transform.rotate(
            pygame.transform.smoothscale(self.surface, (80, 40)).convert_alpha(),
            -self.angle +180  # Negative because pygame's rotation is clockwise
        )
        self.rect = self.draw_surface.get_bounding_rect()
        self.rect.center = self.fireball_pos
        self.mask = pygame.mask.from_surface(self.draw_surface)
        self.alive = True
        self.time = 0
    def calculate_angle(self, direction):
        angle = math.degrees(math.atan2(direction.y, direction.x))  
        return angle
    def update(self, dt):
        if self.alive:
            self.time += dt
            if(self.time > 5):
                self.alive = False
            self.fireball_pos += self.direction * self.fireball_speed * dt
            # if self.fireball_pos[0] <= 0:
            #     self.fireball_pos[0] = 1600
                #self.fireball_speed =0
            #self.draw_surface = pygame.transform.smoothscale(self.surface,(80,40)).convert_alpha()
            self.draw_surface = pygame.transform.rotate(
                pygame.transform.smoothscale(self.surface, (80, 40)).convert_alpha(),
                -self.angle +180  # Negative because pygame's rotation is clockwise
            )
            self.rect = self.draw_surface.get_bounding_rect()
            self.rect.center = self.fireball_pos
            self.mask = pygame.mask.from_surface(self.draw_surface)
    def draw(self, screen):
        if self.alive:
            screen.blit(self.draw_surface, self.rect)
        #screen.blit(self.mask.to_surface(), self.rect)
        # r = self.draw_surface.get_rect()
        # r.topleft = self.fireball_pos
        #pygame.draw.rect(screen, (0,0,255), self.rect,1)
        #screen.blit(self.surface, (self.fireball_pos[0] - self.fireball_radius, self.fireball_pos[1] - self.fireball_radius))
        #screen.blit(self.image, self.fireball_pos)
        # mask_surface = self.mask.to_surface(unsetcolor=(0, 0, 0))
        # mask_surface.set_colorkey((0, 0, 0))
        # screen.blit(mask_surface, self.rect) 