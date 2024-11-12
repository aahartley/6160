import scripts.states as states
import scripts.solvers as solvers
import scripts.particle_emitters as pe
import pygame
import math
from scripts.utils import load_image, load_images, scale_image
class SmokeSim:
    def __init__(self, state, solver):
        self.state = state
        self.solver = solver
        self.run = True
        self.emitters = []
        self.image = load_image("particles/smoke.png")
        self.time = 0
        self.rate = 100 
        self.max = 1000

    def add_emitter(self, emitter):
        self.emitters.append(emitter)

    def change_emitter_rate(self, index, rate):
        self.emitters[index].rate = rate

    def get_nb(self):
        return self.state.get_nb()
    
    def get_active_nb(self):
        return self.state.get_active_nb()

    def add_particles(self, e_rate):
        count = e_rate
        for e in self.emitters:
            if count > 0:
                for i in range(e_rate):
                    P = pygame.math.Vector2()
                    V = pygame.math.Vector2()
                    C = []
                    e.emit(P, V, C)
                    self.state.add_particle(P, V, C, self.image)
                    count -= 1
       

    def update(self, dt):
        self.time += dt
        rate_per_frame = int(self.rate * self.time)
        if(rate_per_frame > 0):
            rate_check = (self.max - len(self.state.positions)) - rate_per_frame
            if rate_check >= 0:
                e_rate = rate_per_frame
            else:
                e_rate = self.max - len(self.state.positions)
            self.time -= rate_per_frame / self.rate
        self.add_particles(e_rate)
        self.solver.solve(dt)
        self.state.update_state(dt)

    def draw(self, screen):
        for i in range(self.get_nb()):
            if(self.state.lives[i] == True):
                #pygame.draw.circle(screen, self.state.colors[i], self.state.positions[i], self.state.radi[i] )
                screen.blit(self.state.surfaces[i], self.state.surfaces[i].get_rect(center=self.state.positions[i]))

def create_smoke_sim():
    state = states.SmokeState()
    solver = solvers.SmokeSolver(state)
    #solver.add_Force(pygame.math.Vector2(0,-10))
    return SmokeSim(state, solver)

