import os
import pygame


player_paths = ["x320p_Spritesheets/Idle_Bow/Idle_Bow_Body_", "x320p_Spritesheets/WalkForward_Bow/WalkForward_Bow_Body_",
                             "x320p_Spritesheets/Attack_Bow/Attack_Bow_Body_", "x320p_Spritesheets/Death_Bow/Death_Bow_Body_"]
player_shadow_paths = ["x320p_Spritesheets/Idle_Bow/Idle_Bow_Shadow_", "x320p_Spritesheets/WalkForward_Bow/WalkForward_Bow_Shadow_", 
                                    "x320p_Spritesheets/Attack_Bow/Attack_Bow_Shadow_","x320p_Spritesheets/Death_Bow/Death_Bow_Shadow_"]

                                    
enemy_paths = ["Skin2_x256_Spritesheets/x256_Spritesheets/Idle/Idle Body ","Skin2_x256_Spritesheets/x256_Spritesheets/Walk/Walk Body ",
                "Skin2_x256_Spritesheets/x256_Spritesheets/Attack1/Attack1 Body ", "Skin2_x256_Spritesheets/x256_Spritesheets/Death1/Death1 Body "]
enemy_shadow_paths = ["Skin2_x256_Spritesheets/x256_Spritesheets/Idle/Idle Shadow ","Skin2_x256_Spritesheets/x256_Spritesheets/Walk/Walk Shadow ",
            "Skin2_x256_Spritesheets/x256_Spritesheets/Attack1/Attack1 Shadow ","Skin2_x256_Spritesheets/x256_Spritesheets/Death1/Death1 Shadow "]
prop_paths = ["Props/1024x1024/Arrow_Far/Arrow_Far_"]
BASE_IMG_PATH = 'data/images/'

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    return img

def load_sprite_sheet(path, scale, factor):
    angles = [0, 22, 45, 67, 90, 112, 135, 157, 180, 202, 225, 247, 270, 292, 315, 337]
    sheets = {}
    for angle in angles:
        formatted_angle = f"{angle:03d}"
        sheets[angle] = load_image(path + f"{formatted_angle}.png").convert_alpha()
        if scale:
            sheets[angle] = scale_image(sheets[angle], factor)
    return sheets

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name).convert_alpha())
    return images

def scale_image(img, factor):
    w, h = img.get_width() * factor, img.get_height() * factor
    return pygame.transform.scale(img, (int(w), int(h))).convert_alpha()

def sprite_frame_dict(rows, cols, width, height):
    frame_set = {}
    for j in range(rows):
        for i in range(cols):
            x = i % cols * width
            y = j % rows * height
            frame_set[j*cols + i] =  (x, y, width,  height)
    return frame_set

def load_tiles(path, rows, cols, width, height, color_key):
    tiles = {}
    for j in range(rows):
        for i in range(cols):
            tiles[j*cols+i] = load_image(path)
            tiles[j*cols+i].set_colorkey(color_key)
            tiles[j*cols+i].set_clip(width*i,height*j,width,height)
            tiles[j*cols+i]=tiles[j*cols+i].subsurface(tiles[j*cols+i].get_clip()).convert_alpha()

    return tiles
