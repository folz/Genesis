'''
Created on Jun 24, 2010

@author: folz
'''

import pygame
from pygame.locals import *
from engine import *

class Terrain(Polygon):
    '''
    A Terrain is a Polygon that you can collide with
    '''

    def __init__(self, points,world):
        Polygon.__init__(self, points, (0, 0))
        self.world = world
        self.location = Vector(points[0][0], points[0][1])
        self.width = abs(points[0][0]-points[1][0])
        self.height = abs(points[0][1]-points[2][1])
        
    def debug(self):
        if not self.isOnScreen(): return
        pygame.draw.polygon(self.world, (255, 255, 255), self.realPoints)
    
    def setWorldCallback(self, world):
        self.world = world
        
    def isOnScreen(self):
        return self.location.x + self.width >= self.world.viewport.getXCoord() and self.location.x <= self.world.viewport.getXCoord() + self.world.getWidth() and self.location.y + self.height >= self.world.viewport.getYCoord() and self.location.y <= self.world.viewport.getYCoord() + self.world.getHeight()
    
        