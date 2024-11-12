import pygame
import random
from scripts.utils import load_image, load_images, scale_image
import math


class Particle:
    def __init__(self, pos, vel, color, radius, img):
        self.pos = pos
        self.vel = vel
        self.color = color
        self.alpha = 255
        self.alpha_rate = 3
        self.radius = radius
        self.alive = True
        self.time = 0
        self.size = 0.1
        self.og_img = img
        self.img = scale_image(img, self.size)
        self.damping = 0.99
    
    def update(self, dt):
        if self.alive:
            self.size += 0.05 * dt
            self.alpha -= self.alpha_rate
            if(self.alpha < 0):
                self.alpha = 0
                self.alive = False

            self.alpha_rate -= 50 * dt
            if self.alpha_rate < 50 * dt:
                self.alpha_rate = 50 *dt
            self.img = scale_image(self.og_img, self.size)
            self.img.set_alpha(self.alpha)

            self.vel[0] += random.choice((-10+self.time*-30,10+self.time*30)) * dt
            self.vel[1] += random.choice((-8, -5)) * dt * self.damping
            self.pos[0] += (self.vel[0] * dt)
            self.pos[1] += (self.vel[1] * dt)

            self.time += dt
            if self.time >= 20 :
                self.alive = False
        
    def draw(self, screen):
        if self.alive:
            #pygame.draw.circle(screen, self.color, self.pos, self.radius)
            screen.blit(self.img, self.img.get_rect(center = self.pos))


class ParticleEmitter:
    def __init__(self, pos, rate, max, img):
        self.particles = []
        self.pos = pos
        self.rate = rate
        self.max = max
        self.img = img
        self.alive = True
        self.time = 0

    def update(self, dt):
        self.time += dt
        rate_per_frame = int(self.rate * self.time)
        if(rate_per_frame > 0):
            rate_check = (self.max - len(self.particles)) - rate_per_frame
            if rate_check >= 0:
                self.emit(rate = rate_per_frame)
            else:
                self.emit(rate = self.max - len(self.particles))
            self.time -= rate_per_frame / self.rate
        

    def emit(self, rate):
        for i in range(rate):
            v_x = random.randint(-1, 1)
            v_y = random.randint(-5, -1)

            r_x = random.randint(1,4)
            r_y = random.randint(1,4)
            self.particles.append(Particle([self.pos[0] + r_x, self.pos[1] - r_y], [0 ,-40 + v_y] , [0,0,255], 2, self.img))

class BasicParticle:
    def __init__(self, pos, vel, color, radius):
        self.pos = pos[:]  
        self.vel = vel[:]  
        self.color = color
        self.radius = radius


    def update(self, dt):
        self.vel[0] += 50 * dt 
        self.vel[1] += 0 *dt
        self.pos[0] += self.vel[0] * dt  
        self.pos[1] += self.vel[1] * dt


        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), self.radius)
        

# class BasicParticle:
#     def __init__(self, initial_pos, vel, color, radius, circle_radius):
#         self.initial_pos = initial_pos[:]  # Store the initial position
#         self.pos = initial_pos[:]  # Current position, starts at initial position
#         self.vel = vel[:]  # Velocity of the particle
#         self.color = color
#         self.radius = radius
#         self.angle = 0  # Initial angle for circular motion
#         self.circle_radius = circle_radius  # Radius of the circular path

#     def update(self, dt):
#         # Move the particle to the right based on velocity
#         self.vel[0] += 50*dt
#         self.pos[0] += self.vel[0] * dt  # Horizontal movement

#         # Update angle for circular motion
#         self.angle += 5 * dt  # Increase angle for circular motion
#         if self.angle > 2 * math.pi:  # Keep angle within 0 to 2*pi radians
#             self.angle -= 2 * math.pi

#         # Calculate the center of the circular motion
#         center_x = self.pos[0]  # Center moves with the particle's x position
#         center_y = self.initial_pos[1]  # Keep the initial y position for circular motion

#         # Update the position using circular motion equations
#         # The particle's position is offset from the center
#         self.pos[0] = center_x + (self.circle_radius * math.cos(self.angle))  # Particle's new x position
#         self.pos[1] = center_y + (self.circle_radius * math.sin(self.angle))  # Particle's new y position

#         # Print position for debugging
#         #print(f"Position: {self.pos}")

#     def draw(self, screen):
#         # Draw the particle as a circle
#         pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), self.radius)







# class BasicParticle:
#     def __init__(self, pos, vel, color, radius, radius_of_circle):
#         self.pos = pos[:]  # Position
#         self.vel = vel[:]  # Velocity
#         self.color = color
#         self.radius = radius
#         self.angle = 0  # Initial angle for circular motion
#         self.radius_of_circle = radius_of_circle  # Radius of the circle to rotate around

#     def update(self, dt):
#         # Update horizontal movement
#         self.vel[0] += 50 * dt  # Add horizontal acceleration
#         self.pos[0] += self.vel[0] * dt  # Update x position based on velocity

#         # Update angle for circular motion
#         self.angle += 5 * dt  # Increase angle (speed of rotation)
#         if self.angle > 2 * math.pi:  # Keep angle within 0 to 2*pi radians
#             self.angle -= 2 * math.pi

#         # Calculate new y position using circular motion
#         self.pos[1] = self.radius_of_circle * math.sin(self.angle) +360  # Circular motion

#         # Optionally print the position to check
#         print(f"Position: {self.pos}")
        
#     def draw(self, screen):
#         # Draw the particle as a circle
#         pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), self.radius)


# class BasicParticle:
#     def __init__(self, pos, vel, color, radius):
#         self.pos = pos[:]  # Make a copy to avoid mutability issues
#         self.initial_pos = pos[:]  # Store initial position
#         self.vel = vel[:]
#         self.color = color
#         self.radius = radius
#         self.angle =0
  
#     def update(self, dt):
#         # Move particle to the right (horizontal movement)
#         self.vel[0] += 50 * dt
#         self.vel[1] += 0 * dt

#         self.angle+=5*dt
#         if self.angle > 359:
#             self.angle=0
#         self.pos[0] = (self.pos[0]*math.cos(self.angle) - self.pos[1]*math.sin(self.angle))*dt 
#         self.pos[1] = (self.pos[1]*math.cos(self.angle) + self.pos[0]*math.sin(self.angle))*dt
#         self.pos[0] += (self.vel[0] * dt)
#         self.pos[1] += (self.vel[1] * dt)
#         print(self.pos)
#         # Calculate oscillation for vertical movement (simulating x-axis rotation)
#         # oscillation_amplitude = 5  # Max vertical displacement
#         # oscillation_speed = 20  # Speed of the oscillation (higher values make it faster)

#         # # Update the angle for the sinusoidal movement
#         # self.angle += oscillation_speed * dt
#         # self.pos[1] = self.initial_pos[1] + oscillation_amplitude * math.sin(self.angle)
        
#     def draw(self, screen):
#         pygame.draw.circle(screen, self.color, self.pos, self.radius)

