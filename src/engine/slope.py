'''
Created on Jun 24, 2010

@author: folz
'''

import pygame
from pygame.locals import *
from engine import *

class Slope(Line):
    '''
    A Slope is a Line that you can collide with
    '''

    def __init__(self, points):
        Line.__init__(self, points, (0, 0))
    
    def __repr__(self):
        return "Slope (%d, %d); (%d, %d)" % (self.realPoints[0][0], self.realPoints[0][1], self.realPoints[1][0], self.realPoints[1][1])
    
    def debug(self):
        pygame.draw.line(self.world, (255, 255, 255), self.realPoints[0], self.realPoints[1])
    
    def setWorldCallback(self, world):
        self.world = world