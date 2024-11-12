import pygame
import numpy as np

from scripts.utils import load_song
from scripts.notes import Note
class Song:
    def __init__(self, song_name, bpm, offset):
        self.song_name = song_name
        self.bpm = bpm
        self.song_pos_in_beats = 0 #starts at 0 not 1
        self.crotchet = 60 / self.bpm #beat in sec
        self.song_pos = 0
        self.offset = offset
        self.offset_in_beats = self.offset * self.bpm/ 60
        self.notes = np.arange(5, 1001, 1).tolist()#list(range(5, 1001,.25))#[1, 2, 3, 4]  # Times in beats
        #self.notes = list([5, 9.25, 13.5, 17.25, 21.25, 24.25])#list(range(5, 1001,.25))#[1, 2, 3, 4]  # Times in beats
        self.active_notes = []
        self.next_index = 0
        self.beats_shown_in_advance = 3
        self.last_beat = 0

    def update(self):
        self.song_pos = (pygame.mixer.music.get_pos()/1000) - self.offset #check for neg
        self.song_pos_in_beats = self.song_pos / self.crotchet
        #print(f"Song Position (seconds): {self.song_pos}, Song Position in Beats: {self.song_pos_in_beats}")

        #spawn note
        if self.next_index < len(self.notes) and self.notes[self.next_index] < self.song_pos_in_beats + self.beats_shown_in_advance:
            #print("Adding note at beat:", self.notes[self.next_index])  # Debug print
            self.active_notes.append(Note(self.notes[self.next_index], self))
            self.next_index += 1

    def play(self):
        pygame.mixer.music.play()
    def stop(self):
        pygame.mixer.music.stop()
    def pause(self):
        pygame.mixer.music.pause()
    def unpause(self):
        pygame.mixer.music.unpause()
    def load(self):
        load_song(self.song_name)
    def unload(self):
        pygame.mixer.music.unload()
    

class SongManager:
    def __init__(self):
        self.songs = []
    def addSong(self, song):
        self.songs.append(song)