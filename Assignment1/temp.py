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
FPS = 60

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
        self.image = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLACK, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2 + random.randint(100, 200), SCREEN_HEIGHT // 2 + random.randint(100, 200))
        self.speed_x = BALL_SPEED
        self.speed_y = -BALL_SPEED
        self.mask = pygame.mask.from_surface(self.image)

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

        # Ball and brick collision routine
        collisions = pygame.sprite.groupcollide(balls, bricks, False, True, collided=pygame.sprite.collide_mask)
        if collisions:
            for b, hit_bricks in collisions.items():
                for br in hit_bricks:
                    if(b.rect.bottom <= br.rect.centery or b.rect.top >= br.rect.centery):
                        b.speed_y *= -1  
                        return
                    elif b.rect.centerx < br.rect.left:  
                        b.speed_x = -abs(b.speed_x)  
                        return
                    elif b.rect.centerx > br.rect.right:  
                        b.speed_x = abs(b.speed_x)  
                        return

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
def reflect_velocity(velocity, normal):
    dot_product = (velocity[0] * normal[0]) + (velocity[1] * normal[1])
    return (velocity[0] - (2 * dot_product * normal[0]), velocity[1] - (2 * dot_product * normal[1]))
# Game loop
running = True
while running:
    key = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if(not balls):
        waiting = True
        over_msg = "You Lose!"
        score_msg = "Score: " + str(hits_with_paddle)
        screen.blit(lose_font.render(over_msg, False, (0,0,0)), ((SCREEN_WIDTH // 2)-lose_font.size(over_msg)[0]//2, (SCREEN_HEIGHT //2 )-lose_font.size(over_msg)[1]//2))
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
  # Clear the screen
    screen.fill(WHITE)
        # Update sprites
    all_sprites.update()

    # Draw static score
    screen.blit(score_font.render("Score: " + str(hits_with_paddle), False, (0,0,0)), (3,3))

    # Draw sprites
    all_sprites.draw(screen)

    # Check for collisions between paddle and ball
    collisions = pygame.sprite.spritecollide(paddle, balls, False)#, collided=pygame.sprite.collide_mask) 
    if collisions:
        for b in collisions:
    
            offset = (paddle.rect.x - b.rect.x, paddle.rect.y - b.rect.y)
            negate_y =-1
            negate_x = 1
            intersection = b.mask.overlap(paddle.mask, offset)

            if(intersection):
 
                #point of the mask overlapping (not pos of sprite)    
                x = intersection[0]
                y = intersection[1]
                #get actual coords
                collision_x = b.rect.x + x
                collision_y = b.rect.y + y
        
                # gradient of the overlap area 
                dx = b.mask.overlap_area(paddle.mask, (offset[0] + 1, offset[1])) - b.mask.overlap_area(paddle.mask, (offset[0] - 1, offset[1]))
                dy = b.mask.overlap_area(paddle.mask, (offset[0], offset[1] + 1)) - b.mask.overlap_area(paddle.mask, (offset[0], offset[1] - 1))

                # collision normal
                length = (dx**2 + dy**2)**0.5
                if length != 0:
                    normal_x = negate_x*dx / length
                    normal_y = negate_y*dy / length
                else:
                    normal_x, normal_y = 0, 0
                print(str(normal_x) + " "+ str(normal_y))
                #treat top of paddle as infinite plane
                if(normal_y >= 0.8): #leeway for edges
                    print(str(b.speed_x) + " "+str(b.speed_y))
                    b.speed_y = -BALL_SPEED
                    print(str(b.speed_x) +" "+ str(b.speed_y))
                else: #if below plane than keep it outside of
                    if(normal_x < 0):
                        b.rect.right = paddle.rect.left
                        b.speed_x = -BALL_SPEED
                    if(normal_x > 0):
                        b.rect.left = paddle.rect.right
                        b.speed_x = BALL_SPEED


                # if(normal_x < 0):
                #     b.rect.x -= b.rect.width -x
                # if(normal_x > 0):
                #     b.rect.x +=  x
                # if(normal_y < 0):
                #     b.rect.y += y
                # if(normal_y > 0):
                #     b.rect.y -= b.rect.height - y
                # print(str(normal_x) + " "+ str(normal_y))
                # pygame.draw.line(screen, (255, 0, 0), (collision_x, collision_y), 
                #                 (collision_x + normal_x * 50, collision_y + normal_y * 50), 2)
                # pygame.draw.circle(screen, (0, 255, 0), (int(collision_x + normal_x * 50), int(collision_y + normal_y * 50)), 10)  # Green circle at the tip
                # Reflect the ball's velocity based on the normal
              


        


                    # # Ball's movement direction (velocity)
                    # velocity_x, velocity_y = b.speed_x, b.speed_y

                    # # Calculate distances to each side of the paddle
                    # dist_left = abs(collision_x - paddle.rect.left)
                    # dist_right = abs(collision_x - paddle.rect.right)
                    # dist_top = abs(collision_y - paddle.rect.top)
                    # dist_bottom = abs(collision_y - paddle.rect.bottom)

                    # # Determine the most likely side based on the ball's velocity
                    # if velocity_y > 0 and dist_top < dist_bottom:
                    #     # Ball moving downwards, prioritize top collision
                    #     normal = (0, -1)  # Top side normal
                    # elif velocity_y < 0 and dist_bottom < dist_top:
                    #     # Ball moving upwards, prioritize bottom collision
                    #     normal = (0, 1)   # Bottom side normal
                    # elif velocity_x > 0 and dist_left < dist_right:
                    #     # Ball moving right, prioritize left side collision
                    #     normal = (-1, 0)  # Left side normal
                    # else:
                    #     # Ball moving left, prioritize right side collision
                    #     normal = (1, 0)   # Right side normal

                    # # Reflect the ball's velocity based on the normal vector
                    # velocity = (b.speed_x, b.speed_y)
                    # new_velocity = reflect_velocity(velocity, normal)

                    # # Apply the reflected velocity
                    # b.speed_x, b.speed_y = new_velocity

                    # # Optional: Correct ball position to prevent it from getting stuck inside the paddle
                    # if normal == (0, -1):  # Top collision
                    #     b.rect.bottom = paddle.rect.top  # Position the ball above the paddle
                    # elif normal == (0, 1):  # Bottom collision
                    #     b.rect.top = paddle.rect.bottom  # Position the ball below the paddle
                    # elif normal == (-1, 0):  # Left collision
                    #     b.rect.right = paddle.rect.left  # Position the ball to the left of the paddle
                    # elif normal == (1, 0):  # Right collision
                    #     b.rect.left = paddle.rect.right  # Position the ball to the right of the paddle



                    # # Calculate the distances to each side of the rectangle
                    # dist_left = abs(collision_x - paddle.rect.left)
                    # dist_right = abs(collision_x - paddle.rect.right)
                    # dist_top = abs(collision_y - paddle.rect.top)
                    # dist_bottom = abs(collision_y - paddle.rect.bottom)

                    #         # Determine the closest side based on the minimum distance
                    # if min(dist_left, dist_right, dist_top, dist_bottom) == dist_left:
                    #     # Collision on the left side
                    #     normal = (-1, 0)  # Left normal vector
                    # elif min(dist_left, dist_right, dist_top, dist_bottom) == dist_right:
                    #     # Collision on the right side
                    #     normal = (1, 0)  # Right normal vector
                    # elif min(dist_left, dist_right, dist_top, dist_bottom) == dist_top:
                    #     # Collision on the top side
                    #     normal = (0, -1)  # Top normal vector
                    # else:
                    #     # Collision on the bottom side
                    #     normal = (0, 1)  # Bottom normal vector

                    # # Reflect the ball's velocity based on the normal vector
                    # velocity = (b.speed_x, b.speed_y)
                    # new_velocity = reflect_velocity(velocity, normal)
                    # b.speed_x, b.speed_y = new_velocity

                    # # Determine the closest side
                    # if min(dist_left, dist_right, dist_top, dist_bottom) == dist_left:
                    #     # Collision with left side
                    #     b.speed_x = -abs(b.speed_x)
                    #     b.hit = True
                    # elif min(dist_left, dist_right, dist_top, dist_bottom) == dist_right:
                    #     # Collision with right side
                    #     b.speed_x = abs(b.speed_x)
                    #     b.hit = True
                    # elif min(dist_left, dist_right, dist_top, dist_bottom) == dist_top:
                    #     # Collision with top side
                    #     b.speed_y = -abs(b.speed_y)
                    #     b.hit = True
                    # elif min(dist_left, dist_right, dist_top, dist_bottom) == dist_bottom:
                    #     # Collision with bottom side
                    #     b.speed_y = abs(b.speed_y)
                    #     b.hit = True


                    # if(y >= BALL_RADIUS):
                    #     #b.rect.bottom = paddle.rect.top
                    #     print(b.rect.bottom)
                    #     b.rect.bottom -= b.mask.get_rect()[3] - y
                    #     print(b.rect.bottom)
                    #     b.speed_y =0
                    # elif( y < BALL_RADIUS):
                    #     b.rect.top = paddle.rect.bottom
                    #     b.speed_y *= -abs(b.speed_y)


                        
                # if(b.rect.bottom <= paddle.rect.top + b.speed_y):
                #     hits_with_paddle += 1
                #     b.speed_y *= -1  
                #     b.rect.bottom = paddle.rect.top
                #     if(hits_with_paddle == 2):
                #         new_ball = Ball()
                #         balls.add(new_ball)
                #         all_sprites.add(new_ball)
        
                # elif b.rect.centerx < paddle.rect.left: 
                #     b.speed_x = -abs(b.speed_x)  
                # elif b.rect.centerx > paddle.rect.right: 
                #     b.speed_x = abs(b.speed_x)  
        
    
  


    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
# Quit the game
pygame.quit()
sys.exit()
