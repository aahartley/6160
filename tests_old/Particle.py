import pygame
class Particle:
    def __init__(self, pos, vel, color, radius):
        self.pos = pos
        self.vel = vel
        self.color = color
        self.radius = radius
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, self.radius)


class ParticleEmitter:
    def __init__(self, pos):
        self.pos = pos
    def emit(self):
        print("test")