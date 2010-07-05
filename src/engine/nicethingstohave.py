'''
Created on Jun 21, 2010

@author: folz
'''

import pygame
from pygame.locals import *
from engine import *
import os

PIXELSPERVECTOR = 100

def load_image(name):
    '''
    Load image from its location and return it
    @param name: the string location of the image
    '''
    name = os.path.join("data", name)
    try:
        image = pygame.image.load(name)
        if image.get_alpha is None:
            image = image.convert
        else:
            image = image.convert_alpha()
    except pygame.error as message:
        print("Cannot load image %s" % name)
        raise SystemExit(message)
    return image

def load_sound(name):
    '''
    Load sound from its location and return it
    @param name: the string location of the sound
    '''
    name = os.path.join("data", name)
    try:
        sound = pygame.mixer.Sound(name)
    except pygame.error as message:
        print("Cannot load sound %s" % name)
        raise SystemExit(message)
    return sound
