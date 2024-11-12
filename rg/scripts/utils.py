import os
import pygame

BASE_IMG_PATH = 'data/images/'
BASE_SONG_PATH = 'data/songs/'

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0,0,0))
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images

def load_song(path):
    pygame.mixer.music.load(BASE_SONG_PATH + path)

def lerp_2d(a, b, t):
    """
    Linearly interpolates between two 2D vectors a and b by a factor of t.

    :param a: Tuple or list representing the starting 2D vector (a_x, a_y).
    :param b: Tuple or list representing the ending 2D vector (b_x, b_y).
    :param t: The interpolation factor (should be between 0 and 1).
    :return: The interpolated 2D vector as a tuple (x, y).
    """
    x = a[0] + t * (b[0] - a[0])
    y = a[1] + t * (b[1] - a[1])
    return [x, y]

