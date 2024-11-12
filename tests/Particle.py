class Particle:
    def __init__(self, pos, vel, color, radius):
        self.pos = pos
        self.vel = vel
        self.color = color
        self.radius = radius
        self.distance = [0,0]
        self.rigid = True


class ParticleEmitter:
    def __init__(self, pos):
        self.pos = pos
    def emit(self):
        print("test")