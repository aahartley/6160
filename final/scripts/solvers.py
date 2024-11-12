import pygame
import random
class SmokeSolver:
    def __init__(self, state):
        self.state = state
        self.forces = []
        self.total_force = pygame.math.Vector2(0,0)
        self.damping =0.99

    def add_Force(self, f):
        self.forces.append(f)    
    
    def solve(self, dt):
        for f in self.forces:
            self.total_force += f
        for i in range(self.state.get_nb()):
            if self.state.lives[i] == True:
                #self.state.velocities[i] += self.total_force * dt
                self.state.velocities[i][0] += random.choice((-10+self.state.ages[i]*-30,10+self.state.ages[i]*30)) * dt
                self.state.velocities[i][1] += random.choice((-8, -5)) * dt * self.damping
                self.state.positions[i] += self.state.velocities[i] * dt
        

