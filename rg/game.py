import pygame
import sys
import numpy as np

from scripts.utils import load_image, load_images, load_song
from scripts.notes import Note
from scripts.songs import SongManager, Song


class Game:
    def __init__(self):
        pygame.mixer.pre_init()
        pygame.init()
        pygame.display.set_caption("Rhythm Game")

        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.clock = pygame.time.Clock()

        self.manager = SongManager()
        self.manager.addSong(Song("metro4.mp3", 40, -1.4))
        self.manager.addSong(Song("metro.mp3",100,-0.491))
        self.font = pygame.font.Font(None, 40)
        self.running = False
        self.pause = False

        self.hit_window = 0.5
        self.hit_line_x = 100
        self.distance_to_hit = self.width - self.hit_line_x
        self.current_song = None
        self.msg = self.font.render("", True, (255, 255, 255))

    def menu(self):
        menu_loop = True
        while menu_loop:
            self.screen.fill('black')
            menu_msg = "Press space to start"
            menu_text = self.font.render(menu_msg, True, (255,255,255))
            self.screen.blit(menu_text, ((self.width//2)-self.font.size(menu_msg)[0]//2, (self.height//2)- self.font.size(menu_msg)[1]//2))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.running = True
                        menu_loop = False
            pygame.display.update()


         # Function to check if the player hit a note
    def check_note_hit(self,song_pos_ms, key_press):
        for note in self.current_song.active_notes:
            if note.flash:
                # time_difference = abs(self.current_song.song_pos - (note.beat * self.current_song.crotchet))
                # if time_difference <= self.hit_window:
                self.msg = self.font.render("you hit ", True, (255, 255, 255))
                note.flash = False
                note.dead = True
                #print(time_difference)
                #self.current_song.active_notes.remove(note)  # Remove the note once it's hit
                return True
            #note.flash = False
        return False

            


    def run(self):
        self.menu()
        frames = 0
        #sound = pygame.mixer.Sound("data/songs/onon.mp3")
        #raw_data = sound.get_raw()
        self.current_song = self.manager.songs[1]
        self.current_song.load()
        self.current_song.play()
        # pygame.mixer.music.rewind()
        # pygame.mixer.music.set_pos(60)


        while self.running:
            dt = self.clock.tick(60)/1000
            self.current_song.update()
          
            fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 255))
            current_time_text = self.font.render(f"current_time: {self.current_song.song_pos}", True, (255, 255, 255))
            self.screen.fill('black')
            self.screen.blit(fps_text,(0,0))
            self.screen.blit(current_time_text, (500,0))

            pygame.draw.line(self.screen, (0, 255, 0), (self.hit_line_x, 0), (self.hit_line_x, self.height), 5)
        

             # Update and draw active notes
            for note in self.current_song.active_notes:
                note.update(dt, self.current_song.song_pos)
                note.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.pause = not self.pause
                        if self.pause:
                            self.current_song.pause()
                        if not self.pause:
                            self.current_song.unpause()
                    if event.key == pygame.K_COMMA:
                        self.current_song.stop()
                        self.current_song.play()
                        # pygame.mixer.music.rewind()
                        # pygame.mixer.music.set_pos(60)
                    if event.key == pygame.K_DOWN:  # Space bar as the hit key
                        if not self.check_note_hit(self.current_song.song_pos, event.key):
                            self.msg = self.font.render("you missed ", True, (255, 255, 255))
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    print(mouse_pos)          

            self.screen.blit(self.msg, (400,30))


     

            #  # Remove notes that move off the left side of the screen
            # self.current_song.active_notes = [note for note in self.current_song.active_notes if note.pos[0] > 50]

            frames += 1
            if(frames >= 1):
                tester =1
            pygame.display.update()
            #tick here?

Game().run()
