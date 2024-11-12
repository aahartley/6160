import pygame
import sys
import numpy as np

from scripts.utils import load_image, load_images, load_song
#from scripts.entities import PhysicsEntity
#from scripts.particles 

class Game:
    def __init__(self):
        pygame.mixer.pre_init()
        pygame.init()
        pygame.display.set_caption("Rhythm Game")

        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.clock = pygame.time.Clock()

        self.movement = [False, False]

        self.assets = {
            "onon" : "onon.mp3"
      
        }  
        self.font = pygame.font.Font(None, 40)
        self.running = False
        self.pause = False


    def menu(self):
        menu_loop = True
        while menu_loop:
            self.screen.fill('black')
            menu_text = self.font.render("Press space to start", True, (255,255,255))
            self.screen.blit(menu_text, (self.width//2, self.height//2))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.running = True
                        menu_loop = False
            pygame.display.update()
        
        
    # # Drawing the waveform
    # def draw_waveform(self,samples):
    #     for i in range(len(samples) - 1):
    #         pygame.draw.line(self.screen, (255, 255, 255), 
    #                         (i, self.height // 2 - samples[i]), 
    #                         (i + 1, self.height // 2 - samples[i + 1]), 
    #                         1)
    
    # def draw_waveform(self,samples):
    #     for x in range(len(samples) - 1):
    #         pygame.draw.line(self.screen, (255, 255, 255), 
    #                      (x, self.height // 2 - samples[x]),  # Current point
    #                      (x + 1, self.height // 2 - samples[x + 1]),  # Next point
    #                      1)  # Line thickness

    # Drawing the waveform with min and max for each window
    def draw_waveform_min_max(self,samples):
        num_pixels = self.width  # One vertical line per pixel width

        # Split the samples into windows that correspond to each pixel on the screen
        samples_per_pixel = max(1, len(samples) // num_pixels)

        for x in range(num_pixels):
            # Get the samples for this pixel's window
            start_idx = x * samples_per_pixel
            end_idx = start_idx + samples_per_pixel
            window = samples[start_idx:end_idx]

            # Find the min and max values in this window
            min_val = np.min(window)
            max_val = np.max(window)

            # Draw a vertical line between the min and max values
            pygame.draw.line(self.screen, (255, 255, 255), 
                            (x, self.height // 2 - min_val),  # Bottom of the line
                            (x, self.height // 2 - max_val),  # Top of the line
                            1)  # Line thickness

    # Drawing the waveform with peak/trough detection
    def draw_waveform_with_threshold(self,samples):
        threshold = 0.5 * (self.height // 2)  # Threshold is 20% of the maximum possible amplitude

        num_pixels = self.width  # One vertical line per pixel width
        samples_per_pixel = max(1, len(samples) // num_pixels)

        for x in range(num_pixels):
            # Get the samples for this pixel's window
            start_idx = x * samples_per_pixel
            end_idx = start_idx + samples_per_pixel
            window = samples[start_idx:end_idx]

            # Find the min and max values in this window
            min_val = np.min(window)
            max_val = np.max(window)

            # Apply the threshold: only draw peaks and troughs above the threshold
            if max_val > threshold or min_val < -threshold:
                # Draw a line from min to max (peak or trough)
                pygame.draw.line(self.screen, (255, 255, 255), 
                                (x, self.height // 2 - min_val),  # Bottom of the line (trough)
                                (x, self.height // 2 - max_val),  # Top of the line (peak)
                                1)  # Line thickness
            else:
                # Draw a straight line if values are within the threshold
                pygame.draw.line(self.screen, (255, 255, 255), 
                                (x, self.height // 2),  # Start at the middle
                                (x, self.height // 2),  # End at the middle
                                1)

    def run(self):
        self.menu()
        frames = 0
        sound = pygame.mixer.Sound("data/songs/onon.mp3")
        raw_data = sound.get_raw()
        # # Convert raw bytes to numpy array
        # # Assuming 16-bit audio; adjust as necessary for your data
        # num_samples = len(raw_data) // 2
        # audio_samples = np.frombuffer(raw_data, dtype=np.int16)
        # # Normalize audio samples to fit within the screen height
        # max_amplitude = np.max(np.abs(audio_samples))
        # audio_samples = audio_samples / max_amplitude  # Normalize to [-1, 1]
        # audio_samples = (audio_samples * (self.height // 2)).astype(int)  # Scale to screen height

        # # Convert raw bytes to numpy array
        # # Assuming 16-bit audio; adjust if your format is different
        # audio_samples = np.frombuffer(raw_data, dtype=np.int16)

        # # Reduce the number of points to match the screen width (downsampling)
        # num_samples = len(audio_samples)
        # samples_per_pixel = num_samples // self.width  # How many audio samples per pixel
        # downsampled_samples = audio_samples[::samples_per_pixel]  # Downsample the array

        # # Normalize the samples to fit the screen height
        # max_amplitude = np.max(np.abs(downsampled_samples))  # Find max amplitude
        # downsampled_samples = downsampled_samples / max_amplitude  # Normalize to [-1, 1]
        # downsampled_samples = (downsampled_samples * (self.height // 2)).astype(int)  # Scale to screen height

        # Convert raw bytes to numpy array (assuming 16-bit audio)
        audio_samples = np.frombuffer(raw_data, dtype=np.int16)
        # Parameters
        samples_per_second = 44100  # Assuming the song is 44.1 kHz
        #samples_per_second = 10000
        window_duration = 2  # Duration of the waveform window in seconds (e.g., show 0.1 seconds)
        window_size = int(window_duration * samples_per_second)  # Number of samples to display at a time

        # Normalize samples
        max_amplitude = np.max(np.abs(audio_samples))  # Find max amplitude
        normalized_samples = audio_samples / max_amplitude  # Normalize to [-1, 1]
        scaled_samples = (normalized_samples * (self.height // 2)).astype(int)  # Scale to screen height

        load_song(self.assets["onon"])
        pygame.mixer.music.play()
        # pygame.mixer.music.rewind()
        # pygame.mixer.music.set_pos(60)
        while self.running:
            dt = self.clock.tick(60)/1000
            current_time = pygame.mixer.music.get_pos()
            song_pos_ms = current_time
            song_pos_samples = (song_pos_ms/1000) * samples_per_second
            song_pos_samples = int(song_pos_samples)
            # Get the portion of the audio data that corresponds to the current song position
            if song_pos_samples + window_size < len(scaled_samples):
                current_window = scaled_samples[song_pos_samples:song_pos_samples + window_size]
            else:
                current_window = scaled_samples[-window_size:]  # If at the end, display the last portion
            # Downsample the window to match screen width
            samples_per_pixel = max(1, len(current_window) // self.width)  # Avoid division by 0
            downsampled_window = current_window[::samples_per_pixel]
            fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 255))
            current_time_text = self.font.render(f"current_time: {current_time/1000}", True, (255, 255, 255))
            self.screen.fill('black')
            self.screen.blit(fps_text,(0,0))
            self.screen.blit(current_time_text, (500,0))
        

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_SPACE:
                        self.pause = not self.pause
                        if self.pause:
                            pygame.mixer.music.pause()
                        if not self.pause:
                            pygame.mixer.music.unpause()
                    if event.key == pygame.K_COMMA:
                        pygame.mixer.music.stop()
                        pygame.mixer.music.play()
                        # pygame.mixer.music.rewind()
                        # pygame.mixer.music.set_pos(60)
                    
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    print(mouse_pos)          

            #self.draw_waveform(audio_samples)  # Draw the waveform
            #self.draw_waveform(downsampled_samples)  # Draw the waveform
            #self.draw_waveform(downsampled_window)  # Draw the waveform
            #self.draw_waveform_min_max(current_window)
            self.draw_waveform_with_threshold(current_window)

            frames += 1
            pygame.display.update()
            #tick here?

Game().run()
