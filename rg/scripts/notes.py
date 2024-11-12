import pygame
from scripts.utils import lerp_2d
class Note:
    def __init__(self, beat, song):
        self.pos = [400,300]
        self.beat = beat
        self.song = song
        self.last_beat = 0
        self.flash = False
        self.dead = False
        self.ring_size = 100  # Starting size for the ring (outer circle)
        self.max_ring_size = 100  # Max size for the ring (outer circle)
        self.min_ring_size = 10  # Minimum size for the ring (outer circle)
        self.ring_color = (255, 0, 0)  # Color of the ring (red)
        self.ring_active = False  # State for the ring
    
    def update(self, dt, song_pos_ms):
        # # Calculate normalized time
        # t = (self.song.beats_shown_in_advance - (self.beat - self.song.song_pos_in_beats)) / self.song.beats_shown_in_advance

        # # if t < 0 or t > 1:
        # #     print(t)
        # t = max(0, min(1, t))  # Clamp t between 0 and 1
        # self.pos = lerp_2d(self.pos, [100,300], t)
      # Calculate the time remaining until the flash time
        time =  (self.beat * self.song.crotchet) - 0.05
        time_until_flash = time - self.song.song_pos
    
        
        # Check if it's time to flash
        if self.song.song_pos >= (time - 1) and not self.dead:
            #print(time_until_flash)

            self.ring_active = False
            # Ring shirnks over time
            self.ring_size = self.min_ring_size + (self.max_ring_size - self.min_ring_size) * (time_until_flash / 1.0)
            self.ring_size = max(self.min_ring_size, self.ring_size)  # Ensure it doesn't go below min size
            if self.song.song_pos >= time and not self.dead:
                self.flash = True
                self.ring_active = False  # Stop the ring growth
                self.ring_size = self.min_ring_size
                if self.song.song_pos >= (self.beat * self.song.crotchet) + 0.05:
                    self.flash = False
                    self.dead = True
                    self.ring_size = self.max_ring_size  # Reset the ring size after the note is hit/missed

        # if(self.song.song_pos >= (self.beat * self.song.crotchet)-0.05) and not self.dead:
        #     self.flash = True
        #     if(self.song.song_pos >= (self.beat * self.song.crotchet)+0.05) and not self.dead:
        #         self.flash = False
        #         self.dead = True

    def draw(self, screen):
        #pygame.draw.circle(screen, (255, 0, 0), (int(self.pos[0]), int(self.pos[1])), 20)
        # if self.flash:
        #     pygame.draw.circle(screen, (255, 0, 0), (int(400), int(self.pos[1])), 20)
# Draw the ring around the note if it's active
        # if self.ring_active:
        #     pygame.draw.circle(screen, self.ring_color, (int(self.pos[0]), int(self.pos[1])), int(self.ring_size), 2)

        # Always draw the note (smaller red circle)
        if not self.dead:
            pygame.draw.circle(screen, self.ring_color, (int(self.pos[0]), int(self.pos[1])), 10)  # Smaller red circle for the note
            if self.ring_active:
                pygame.draw.circle(screen, self.ring_color, (int(self.pos[0]), int(self.pos[1])), int(self.ring_size), 2)
