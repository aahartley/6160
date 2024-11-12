import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Rhythm Game")
clock = pygame.time.Clock()

pygame.mixer.init()

pygame.mixer.music.load("onon.mp3")  
pygame.mixer.music.play()

# Define the BPM and beat interval
BPM = 174
beat_interval = 60 / BPM  # Time between beats in seconds

# Example notes (in milliseconds)
notes = [1000, 2000, 3000, 4000, 5000]  # Times in milliseconds
score = 0

# Function to spawn notes
def spawn_notes(notes, current_time):
    for note_time in notes:
        if note_time - 100 <= current_time <= note_time:  # Spawn 500 ms before
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(400, 50, 50, 50))

# Function to check if the player hits the note
def check_hit(current_time, notes):
    global score
    for note_time in notes:
        if abs(current_time - note_time) < 100:  # 100 ms window for a hit
            print("Hit!")
            score += 1
            notes.remove(note_time)
            return True
    return False

# Function to check player input
def check_input(current_time, notes):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        is_hit = check_hit(current_time, notes)
        draw_feedback(is_hit)

# Function to draw feedback
def draw_feedback(is_hit):
    if is_hit:
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(300, 300, 200, 50))  # Green feedback
    else:
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(300, 300, 200, 50))  # Red feedback

# Main game loop
running = True
start_time = pygame.time.get_ticks()  # Get the start time in milliseconds
score_font = pygame.font.Font(None, 40)

while running:
    screen.fill((0, 0, 0))  # Clear the screen

    # Get the current time in milliseconds
    current_time = pygame.mixer.music.get_pos()

    # Spawn notes
    spawn_notes(notes, current_time)

    # Check for player input
    check_input(current_time, notes)

    screen.blit(score_font.render("Score: " + str(score), False, (255,255,255)), (3,3))

    # Update the display
    pygame.display.flip()

    # Check for quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(60)  # Limit the frame rate to 60 FPS

pygame.quit()
sys.exit()