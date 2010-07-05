'''
Created on Jun 30, 2010

@author: catapult
'''

import pygame, math
from pygame.locals import *
from engine import *
from engine.nicethingstohave import *

class NetworkBulletManager:
    
    def __init__(self, world):
        self.world = world
        self.bullets = []
        
    def fromNetwork(self,bullets):
        if len(bullets) == 0: return
        for b in self.bullets:
            self.removeBullet(b)
        for b in bullets:
            self.addBullet(Vector(b[0],b[1]))

#        amount = 0
#        if len(self.bullets) < len(bullets):
#            amount = len(bullets)-len(self.bullets)
#            for i in range(amount):
#                self.addBullet(bullets[i])
#        elif len(self.bullets) > len(bullets):
#            amount = len(self.bullets)-len(bullets)
#            for i in range(amount):
#                self.removeBullet(self.bullets[i])
#                
#        amount = len(bullets)-amount
#        print(amount)
#        if amount > 0:
#            for i in range(amount):
#                self.bullets[i].location = Vector(bullets[i+amount][0],bullets[i+amount][1])
    
    def draw(self):
        for b in self.bullets:
            b.draw()
    
    def addBullet(self, location):
        b = BulletEntity(location, (0,0),"right")
        self.bullets.append(b)
        b.setWorldCallback(self.world)
        b.setBulletManagerCallback(self)
        b.draw()
    
    def removeBullet(self, bullet):
        if bullet in self.bullets:
            self.bullets.remove(bullet)
            del bullet