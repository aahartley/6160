import pygame
import random
import sys
# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BRICK_WIDTH = 80
BRICK_HEIGHT = 30
BALL_RADIUS = 10
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BALL_SPEED = 2
PADDLE_SPEED = 10
BRICK_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
TEXT_SPACE = 50
FPS =60

# Counter for hits with paddle
hits_with_paddle = 0
score_font = pygame.font.Font(None, 40)
lose_font = pygame.font.Font(None, 80)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Assignment2 -Austin Hartley")

clock = pygame.time.Clock()


# Ball class
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2),pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLACK, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2 + random.randint(100, 200), SCREEN_HEIGHT // 2 + random.randint(100, 200))
        self.speed_x = BALL_SPEED
        self.speed_y = -BALL_SPEED
        self.mask = pygame.mask.from_surface(self.image)
        self.radius = BALL_RADIUS

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Bounce off walls
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed_x *= -1
        if self.rect.top < 0:
            self.speed_y *= -1

        # Ball missed paddle (remove ball if it goes out of bounds)
        if self.rect.top > SCREEN_HEIGHT:
            #self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # Reset the ball position
            self.kill()

        #ball to ball coll
        ball_colls = pygame.sprite.spritecollide(self, balls, False, collided=pygame.sprite.collide_circle)
        if ball_colls:
            for b in ball_colls:
                if(self != b):
                    if(self.rect.x <= b.rect.x):
                        self.speed_x = -BALL_SPEED
                        b.speed_x = BALL_SPEED
                    else:
                        self.speed_x = BALL_SPEED
                        b.speed_x = -BALL_SPEED
                    if(self.rect.y <= b.rect.y):
                        self.speed_y = BALL_SPEED
                        b.speed_y = -BALL_SPEED
                    else:
                        self.speed_y = -BALL_SPEED
                        b.speed_y = BALL_SPEED

        #ball to brick collisions
        br_colls = pygame.sprite.spritecollide(self, bricks, False)#, collided=pygame.sprite.collide_mask) 
        if br_colls:
            for br in br_colls:
                #more accurate to account for circle
                offset = (br.rect.x - self.rect.x, br.rect.y - self.rect.y)
                # gradient of the overlap area 
                dx = self.mask.overlap_area(br.mask, (offset[0] + 1, offset[1])) - self.mask.overlap_area(br.mask, (offset[0] - 1, offset[1]))
                dy = self.mask.overlap_area(br.mask, (offset[0], offset[1] + 1)) - self.mask.overlap_area(br.mask, (offset[0], offset[1] - 1))
                #dy neg (br moving down decreases overlap)(ball y is > br y)
                #dx neg (br moving left increases overlap)(ball x is > br x)
                if(dx != 0 or dy != 0):
                    br.kill()
                    # collision normal
                    length = (dx**2 + dy**2)**0.5
                    if length != 0:
                        normal_x = dx / length
                        normal_y = -1*dy / length #since up and down is reversed
                    else:
                        normal_x, normal_y = 0, 0

                    #treat top and bot of br as infinite plane
                    if(normal_y >= 0.8): #leeway for edges
                        self.speed_y = -BALL_SPEED
                    elif(normal_y <= -0.8):
                        self.speed_y = BALL_SPEED
                    else: #if in between 
                        if(normal_x < 0):
                            self.rect.right = br.rect.left
                            self.speed_x = -BALL_SPEED
                        elif(normal_x > 0):
                            self.rect.left = br.rect.right
                            self.speed_x = BALL_SPEED


# Paddle class
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20)
        self.speed = PADDLE_SPEED
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Collisions
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH     


# Brick class
class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

# Create sprite groups
all_sprites = pygame.sprite.Group()
bricks = pygame.sprite.Group()
balls = pygame.sprite.Group()

# Create bricks
for row in range(5):
    for col in range(10):
        brick = Brick(col * (BRICK_WIDTH + 2), TEXT_SPACE + row * (BRICK_HEIGHT + 2), random.choice(BRICK_COLORS))
        bricks.add(brick)
        all_sprites.add(brick)

# Create paddle
paddle = Paddle()
all_sprites.add(paddle)

# Create ball
ball = Ball()
all_sprites.add(ball)
balls.add(ball)


# Display initial score (static)
screen.blit(score_font.render("Score: " + str(hits_with_paddle), False, (0,0,0)), (3,3))

# Game loop
running = True
waiting = False
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False     
            
    if(not balls):
        waiting = True
        while waiting:
            over_msg = "You Lose!"
            score_msg = "Score: " + str(hits_with_paddle)
            screen.blit(lose_font.render(over_msg, False, (0,0,0)), ((SCREEN_WIDTH // 2)-lose_font.size(over_msg)[0]//2, (SCREEN_HEIGHT //2 )-lose_font.size(over_msg)[1]//2))
            screen.blit(score_font.render(score_msg, False, (0,0,0)),((SCREEN_WIDTH // 2)-score_font.size(score_msg)[0]//2, lose_font.get_height()//2+(SCREEN_HEIGHT //2 )+score_font.size(score_msg)[1]//2))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        waiting = False
    if(not bricks):
        waiting = True
        win_msg = "You Win!"
        score_msg = "Score: " + str(hits_with_paddle)
        screen.blit(lose_font.render(win_msg, False, (0,0,0)), ((SCREEN_WIDTH // 2)-lose_font.size(win_msg)[0]//2, (SCREEN_HEIGHT //2 )-lose_font.size(win_msg)[1]//2))
        screen.blit(score_font.render(score_msg, False, (0,0,0)),((SCREEN_WIDTH // 2)-score_font.size(score_msg)[0]//2, lose_font.get_height()//2+(SCREEN_HEIGHT //2 )+score_font.size(score_msg)[1]//2))
        pygame.display.flip()
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        waiting = False 
                        running = False

    # Check for collisions between paddle and ball AABB
    collisions = pygame.sprite.spritecollide(paddle, balls, False)#, collided=pygame.sprite.collide_mask) 
    if collisions:
        for b in collisions:
            #more accurate to account for circle
            offset = (paddle.rect.x - b.rect.x, paddle.rect.y - b.rect.y)
            # gradient of the overlap area 
            dx = b.mask.overlap_area(paddle.mask, (offset[0] + 1, offset[1])) - b.mask.overlap_area(paddle.mask, (offset[0] - 1, offset[1]))
            dy = b.mask.overlap_area(paddle.mask, (offset[0], offset[1] + 1)) - b.mask.overlap_area(paddle.mask, (offset[0], offset[1] - 1))
            #print(f"dx: {dx}, dy: {dy}")  
            #dy neg (paddle moving down decreases overlap)(ball y is > paddle y)
            #dx neg (paddle moving left increases overlap)(ball x is > paddle x)
            if(dx != 0 or dy != 0):
                # collision normal
                length = (dx**2 + dy**2)**0.5
                if length != 0:
                    normal_x = dx / length
                    normal_y = -1*dy / length #since up and down is reversed
                else:
                    normal_x, normal_y = 0, 0

                #treat top of paddle as infinite plane
                if(normal_y >= 0.8): #leeway for edges
                    b.speed_y = -BALL_SPEED
                    hits_with_paddle += 1
                    if(hits_with_paddle % 2 == 0): #every 2nd hit
                        new_ball = Ball()
                        balls.add(new_ball)
                        all_sprites.add(new_ball)
                elif(normal_y <= -0.8):
                     b.speed_y = BALL_SPEED
                else: #if below plane than keep it outside of the padddle
                    if(normal_x < 0):
                        b.rect.right = paddle.rect.left
                        b.speed_x = -BALL_SPEED
                    elif(normal_x > 0):
                        b.rect.left = paddle.rect.right
                        b.speed_x = BALL_SPEED




    # Clear the screen
    screen.fill(WHITE)
    # Update sprites
    all_sprites.update()

    # Draw static score
    screen.blit(score_font.render("Score: " + str(hits_with_paddle), False, (0,0,0)), (3,3))

    # Draw sprites
    all_sprites.draw(screen)
 
    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit the game
pygame.quit()
sys.exit()
