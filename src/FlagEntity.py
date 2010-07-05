'''
Created on Jun 24, 2010

@author: folz
'''

import math
import pygame
from pygame.locals import *
from engine import *
from engine.nicethingstohave import *

class FlagEntity(Entity):
    
    def __init__(self, team, location = geometry.Vector(0, 0), velocity = Vector(0, 0)):
        '''
        Constructor
        '''
        self.start = geometry.Vector(location[0],location[1])
        entity.Entity.__init__(self, "flag_%s.png" % team, location, velocity)
        self.facing = "right"
        self.wasFacing = self.facing
        self.team = team
        self.captured = False
        self.capturer = None
        self.scale = 1
        self.score = 0
        
    def setFacing(self,newFacing):
        self.wasFacing = self.facing
        self.facing = newFacing
    
    def wasCapturedBy(self, entity):
        self.captured = True
        self.capturer = entity
        self.capturer.flag = self
        
    def release(self):
        if self.capturer is not None:
            self.capturer.flag = None
            self.capturer.hasFlag = False
        self.facing = "right"
        self.captured = False
        self.capturer = None
        self.location = self.start.copy()
    
    def move(self, delta):
        if self.captured and self.capturer != None:
            pass
        self.checkCollisions()
        
    def updateScore(self,score):
        self.score = score
    
    def checkCollisions(self):
        self.boundingPoly = geometry.Rect(self.location.x, self.location.y, self.getWidth(), self.getHeight())
        if not self.captured:
            for player in self.world.players:
                if player.team != self.team:
                    mtd = self.boundingPoly.collide(player.boundingPoly)
                    if mtd != False:
                        self.wasCapturedBy(player)
                        player.hasFlag = True
                        print("captured")
                else:
                    mtd = self.boundingPoly.collide(player.boundingPoly)
                    if mtd != False and player.hasFlag and self.captured == False:
                        player.flag.release()
                        self.score += 1
                        print("SCORED")
                        
                        
        else:
            if self.capturer.facing == "left":
                self.location.x = self.capturer.location.x + self.capturer.getWidth() / 2
                self.location.y = self.capturer.location.y
            elif self.capturer.facing == "right":
                self.location.x = self.capturer.location.x - self.capturer.getWidth() / 2
                self.location.y = self.capturer.location.y
        
        self.rect = pygame.Rect(self.boundingPoly.realPoints[0][0],self.boundingPoly.realPoints[0][1],self.boundingPoly.width,self.boundingPoly.height)
        
    def draw(self):
        if self.facing == "right" and self.scale == -1:
            self.image = pygame.transform.flip(self.image, True, False)
            self.scale = 1
        elif self.facing == "left" and self.scale == 1:
            self.image = pygame.transform.flip(self.image, True, False)
            self.scale = -1
        
        Entity.draw(self)
        self.wasFacing = self.facing
