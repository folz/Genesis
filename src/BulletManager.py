'''
Created on Jun 28, 2010

@author: folz
'''

import pygame, math
from pygame.locals import *
from engine import *
from engine.nicethingstohave import *

class BulletManager:
    
    def __init__(self, entity):
        self.entity = entity
        self.lastshot = pygame.time.get_ticks()
        self.bullets = []
    
    def shoot(self):
        for b in self.bullets:
            b.move()
            b.draw()
    
    def addBullet(self, location, velocity, facing="right"):
        nowshot = pygame.time.get_ticks()
        if (nowshot - self.lastshot) > 150:
            self.lastshot = nowshot
            b = BulletEntity(location, velocity, facing)
            self.bullets.append(b)
            b.setWorldCallback(self.entity.world)
            b.setBulletManagerCallback(self)
    
    def removeBullet(self, bullet):
        if bullet in self.bullets:
            self.bullets.remove(bullet)
            del bullet