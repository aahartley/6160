import pygame
from scripts.utils import load_image, load_images, sprite_frame_dict, load_sprite_sheet, load_tiles
import math

class Tile:
    def __init__(self, width, height):
        self.tiles = load_tiles("tiles/Overworld-Large/Thick/Overworld-Terrain1-Thick256x144.png",6, 3, 256, 144, (0,0,0))
        self.tiles2 = load_tiles("tiles/Overworld-Large/Flat/Overworld - Water - Flat 256x128.png",6, 3, 256, 128, (255,0,255))

        self.screen_width = width
        self.screen_height = height
        self.tile_width = 256
        self.tile_height = 144
        self.tile_width2 = 256
        self.tile_height2 = 128
        self.water_offset = 0
        self.water_tile = self.tiles2[0]  
        self.z_height = 10
        # self.tile_map = [ 
        #     [2, 2, 2, 2, 2, 2, 2, 2],
        #     [2, 2, 0, 2, 2, 0, 2, 2],
        #     [2, 0, 2, 2, 2, 2, 0, 2],
        #     [2, 2, 2, 2, 0, 2, 2, 2],
        #     [2, 2, 2, 0, 2, 2, 2, 2],
        #     [2, 0, 2, 2, 2, 2, 0, 2],
        #     [2, 2, 0, 2, 2, 0, 2, 2],
        #     [2, 2, 2, 2, 2, 2, 2, 2],
        # ]
        self.tile_map = [ 
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 0, 2, 2, 0, 2, 2, 2, 2],
            [2, 0, 2, 2, 2, 2, 0, 2, 2, 2],
            [2, 2, 2, 2, 0, 2, 2, 2, 0, 2],
            [2, 2, 2, 0, 2, 2, 2, 2, 2, 2],
            [2, 0, 2, 2, 2, 2, 0, 2, 2, 2],
            [2, 2, 0, 2, 2, 0, 2, 2, 2, 2],
            [2, 0, 2, 0, 2, 2, 2, 2, 2, 2],
            [2, 0, 2, 2, 2, 0, 2, 2, 0, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],

        ]
    def find_corners(self):
        x_start = self.screen_width//2 - self.tile_width//2
        y_start = -self.tile_height//2 - self.tile_height
        #y_start = 0
        extra= 5  #5
        extra = 0
        offset = 8  #8
        # Adjust these offsets based on your requirements
        shift_x = self.tile_width // 2 
        shift_y = self.tile_height // 2 - offset 

        # Find the corners of the diamond
        # Top-left corner
        top_left_x = x_start + (0 - 0) * (self.tile_width // 2) + shift_x
        top_left_y = y_start + (0 + 0) * (self.tile_height // 2 - offset) + shift_y

        # Top-right corner (last tile in the first row)
        top_right_x = x_start + (len(self.tile_map[0]) - 1 - 0) * (self.tile_width // 2) + shift_x
        top_right_y = y_start + (0 + (len(self.tile_map[0]) - 1)) * (self.tile_height // 2 - offset) + shift_y

        # Bottom-left corner (first tile in the last row)
        bottom_left_x = x_start + (0 - (len(self.tile_map) - 1)) * (self.tile_width // 2) + shift_x
        bottom_left_y = y_start + ((len(self.tile_map) - 1) + 0) * (self.tile_height // 2 - offset) + shift_y

        # Bottom-right corner (last tile in the last row)
        bottom_right_x = x_start + ((len(self.tile_map[0]) - 1) - (len(self.tile_map) - 1)) * (self.tile_width // 2) + shift_x
        bottom_right_y = y_start + ((len(self.tile_map) - 1) + (len(self.tile_map) - 1)) * (self.tile_height // 2 - offset) + shift_y
        return (top_left_x,top_left_y), (top_right_x,top_right_y), (bottom_left_x, bottom_left_y), (bottom_right_x, bottom_right_y)

    def draw(self, screen):
        x_start = self.screen_width//2 - self.tile_width//2
        y_start = -self.tile_height//2 - self.tile_height
        #y_start = 0
        extra= 5  #5
        extra = 0
        offset = 8  #8
        # for j in range(0,self.screen_height//self.tile_height+extra):
        #     for i in range(0,self.screen_width//self.tile_width+extra):
        #         x_screen = x_start+(i-j)*(self.tile_width//2)
        #         y_screen = y_start + (i+j)*(self.tile_height//2-offset)
        #         screen.blit(self.tiles[1], (x_screen, y_screen))
        #         #pygame.draw.circle(screen, (255, 0, 0), (x_screen,y_screen), 3) 

        for j, row in enumerate(self.tile_map):
            for i, tile_id in enumerate(row):
                x_screen = x_start+(i-j)*(self.tile_width//2)
                y_screen = y_start + (i+j)*(self.tile_height//2-offset)
                screen.blit(self.tiles[tile_id], (x_screen, y_screen))
                #pygame.draw.rect(screen, (255,0,0), (i*self.tile_width, j*self.tile_height, self.tile_width, self.tile_height), 1)
  
        # Top-left fill
        for j in range(-5, len(self.tile_map)//2 + 5):  
            for i in range(-5, 0):  
                x_screen = x_start + (i - j) * (self.tile_width2 // 2)
                y_screen = y_start + (i + j) * (self.tile_height2 // 2 - self.water_offset) + self.z_height
                screen.blit(self.water_tile, (x_screen, y_screen))


        # Top-right fill
        for j in range(-5, len(self.tile_map)//2 -5):
            for i in range(0, len(self.tile_map[0])+5 ):
                x_screen = x_start + (i - j) * (self.tile_width2 // 2)
                y_screen = y_start + (i + j) * (self.tile_height2 // 2 - self.water_offset) + self.z_height
                screen.blit(self.water_tile, (x_screen, y_screen))


        # Bottom-left fill
        for j in range(len(self.tile_map), len(self.tile_map) + 5):
            for i in range(-5, len(self.tile_map[0])//2 + 5):
                x_screen = x_start + (i - j) * (self.tile_width2 // 2)
                y_screen = y_start + (i + j) * (self.tile_height2 // 2 - self.water_offset) + self.z_height
                screen.blit(self.water_tile, (x_screen, y_screen))
                #pygame.draw.circle(screen, (255, 0, 0), (x_screen,y_screen), 3) 


        # Bottom-right fill
        for j in range(len(self.tile_map)//2 -5, len(self.tile_map) + 5):
            for i in range(len(self.tile_map[0]), len(self.tile_map[0]) + 5):
                x_screen = x_start + (i - j) * (self.tile_width2 // 2)
                y_screen = y_start + (i + j) * (self.tile_height2 // 2 - self.water_offset) + self.z_height
                screen.blit(self.water_tile, (x_screen, y_screen))
                
        

        # # Draw lines through the corners
        # pygame.draw.line(screen, (255, 0, 0), (top_left_x, top_left_y), (top_right_x, top_right_y), 2)  # Top edge
        # pygame.draw.line(screen, (255, 0, 0), (bottom_left_x, bottom_left_y), (bottom_right_x, bottom_right_y), 2)  # Bottom edge
        # pygame.draw.line(screen, (255, 0, 0), (top_left_x, top_left_y), (bottom_left_x, bottom_left_y), 2)  # Left edge
        # pygame.draw.line(screen, (255, 0, 0), (top_right_x, top_right_y), (bottom_right_x, bottom_right_y), 2)  # Right edge