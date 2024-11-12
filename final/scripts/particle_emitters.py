import random
import pygame
class ParticleEmitter:
    def __init__(self, pos, emit_type):
        self.pos = pos
        self.emit_type = emit_type

    def emit(self, P, V ,C):
        if(self.emit_type == 'random'):
            self.emit_random(P,V,C)

    def emit_random(self, P, V, C):
        v_x = random.randint(-1, 1)
        v_y = random.randint(-5, -1)
        V.update(v_x, v_y + -40)

        # r_x = random.randint(300,400)
        # r_y = random.randint(300,500)
        r_x = random.randint(1,4)
        r_y = random.randint(1,4)
        P.update(self.pos[0] + r_x, self.pos[1] - r_y)

        C[:] = [0,0,255,255]         