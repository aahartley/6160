import pygame
import random

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)

# Particle class for teleportation smoke/poof effect
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(10, 20)
        self.color = (random.randint(100, 150), 0, random.randint(100, 150))  # Purple smoke
        self.lifetime = random.randint(20, 40)
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1

    def render(self, surface):
        if self.lifetime > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)

# Nightcrawler class
class Nightcrawler:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.Surface((40, 60))
        self.image.fill((0, 0, 255))  # Blue for the character
        self.visible = True
        self.particles = []
        self.teleporting = False
        self.destination = (x, y)

    def teleport(self, new_x, new_y):
        self.teleporting = True
        self.destination = (new_x, new_y)

    def update(self):
        if self.teleporting:
            # Create teleportation particles (disappear)
            for _ in range(10):
                self.particles.append(Particle(self.x + 20, self.y + 30))

            # Make the character invisible for a short time
            self.visible = False

            # Teleport after a few frames
            if len(self.particles) > 30:
                self.x, self.y = self.destination
                self.visible = True
                self.teleporting = False

            # Create particles at the destination (reappear)
            for _ in range(10):
                self.particles.append(Particle(self.x + 20, self.y + 30))

        # Update particle system
        self.particles = [p for p in self.particles if p.lifetime > 0]
        for p in self.particles:
            p.update()

    def render(self, surface):
        if self.visible:
            surface.blit(self.image, (self.x, self.y))
        for p in self.particles:
            p.render(surface)

# Create Nightcrawler character
nightcrawler = Nightcrawler(400, 300)
def render_trail(surface, start_pos, end_pos):
    pygame.draw.line(surface, (150, 0, 150), start_pos, end_pos, 5)  # Purple trail

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Teleport when space bar is pressed
                new_x = random.randint(100, 700)
                new_y = random.randint(100, 500)
                nightcrawler.teleport(new_x, new_y)

    # Update
    nightcrawler.update()

    # Render
    screen.fill((0, 0, 0))
    nightcrawler.render(screen)
    render_trail(screen, (nightcrawler.x,nightcrawler.y), (nightcrawler.destination))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
