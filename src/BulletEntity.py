'''
Created on Jun 24, 2010

@author: folz
'''

import pygame
from pygame.locals import *
from engine import *
from engine.nicethingstohave import *

MAXXSPEED = 100
MAXYSPEED = 100

class BulletEntity(Entity):
    '''
    A Bullet is something you shoot. It is handled by a BulletManager
    '''
    
    def __init__(self, location, velocity, facing):
        '''
        Constructor
        '''
        Entity.__init__(self, "bullet.png", location, velocity)
        if facing == "left":
            self.image = pygame.transform.flip(self.image, True, False)
        self.used = False
        self.sent = False
        self.rect = pygame.Rect(self.location.x, self.location.y, self.getWidth(), self.getHeight())
    
    def setBulletManagerCallback(self, bulletmanager):
        self.bulletmanager = bulletmanager
        
    def networkBullet(self):
        p2 = self.world.getPlayer2()
        self.boundingPoly = geometry.Rect(self.location.x,self.location.y,self.getWidth(),self.getHeight())
        mtd = p2.boundingPoly.collide(self.boundingPoly)
        if mtd != False:
            p2.takeHit()
            self.used = True
        
    
    def move(self):
        if(self.velocity.x == 0):
            return
        
        self.networkBullet()
        
        if self.used:
            self.bulletmanager.removeBullet(self)
            del self
            return
        
        if self.velocity.x > MAXXSPEED:
            self.velocity.x = MAXXSPEED
        if self.velocity.x < -MAXXSPEED:
            self.velocity.x = -MAXXSPEED
        if self.velocity.y > MAXYSPEED:
            self.velocity.y = MAXYSPEED
        if self.velocity.y < -MAXYSPEED:
            self.velocity.y = -MAXYSPEED

        self.location.x += self.velocity.x #* (PIXELSPERVECTOR / delta)
        self.location.y += self.velocity.y #* (PIXELSPERVECTOR / delta)
        
        self.rect = pygame.Rect(self.location.x, self.location.y, self.getWidth(), self.getHeight())
        
        if self.location.x < 0 or self.location.x > self.world.getWidth() or self.location.y < 0 or self.location.y > self.world.getHeight():
            self.bulletmanager.bullets.remove(self)
                    
        self.checkCollisions()
    
    def checkCollisions(self):
        if not self.used:
            self.boundingPoly = geometry.Rect(self.location.x,self.location.y,self.getWidth(),self.getHeight())
            for terrain in self.world.getTerrain():
                mtd = self.boundingPoly.collide(terrain)
                if mtd != False:
                    self.used = True
        if self.used:
            self.bulletmanager.removeBullet(self)
            del self
    
    def draw(self):
        Entity.draw(self)