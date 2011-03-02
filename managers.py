'''
Created on Jun 28, 2010

@author: folz
'''

import pygame, math
from pygame.locals import *
from engine import *
from engine.misc import *
from entities import *

class BulletManager:

	def __init__( self, entity ):
		self.entity = entity
		self.lastshot = pygame.time.get_ticks()
		self.bullets = []

	def shoot( self ):
		for b in self.bullets:
			b.move()
			b.draw()

	def addBullet( self, location, velocity, facing="right" ):
		nowshot = pygame.time.get_ticks()
		if ( nowshot - self.lastshot ) > 150:
			self.lastshot = nowshot
			b = BulletEntity( location, velocity, facing )
			self.bullets.append( b )
			b.setWorldCallback( self.entity.world )
			b.setBulletManagerCallback( self )

	def removeBullet( self, bullet ):
		if bullet in self.bullets:
			self.bullets.remove( bullet )
			del bullet

'''
Created on Jun 30, 2010

@author: catapult
'''

import pygame, math
from pygame.locals import *
from engine import *
from engine.misc import *

class NetworkBulletManager:

	def __init__( self, world ):
		self.world = world
		self.bullets = []

	def fromNetwork( self, bullets ):
		if len( bullets ) == 0: return
		for b in self.bullets:
			self.removeBullet( b )
		for b in bullets:
			self.addBullet( geometry.Vector( b[0], b[1] ) )

#		amount = 0
#		if len(self.bullets) < len(bullets):
#			amount = len(bullets)-len(self.bullets)
#			for i in range(amount):
#				self.addBullet(bullets[i])
#		elif len(self.bullets) > len(bullets):
#			amount = len(self.bullets)-len(bullets)
#			for i in range(amount):
#				self.removeBullet(self.bullets[i])
#				
#		amount = len(bullets)-amount
#		print(amount)
#		if amount > 0:
#			for i in range(amount):
#				self.bullets[i].location = Vector(bullets[i+amount][0],bullets[i+amount][1])

	def draw( self ):
		for b in self.bullets:
			b.draw()

	def addBullet( self, location ):
		b = BulletEntity( location, ( 0, 0 ), "right" )
		self.bullets.append( b )
		b.setWorldCallback( self.world )
		b.setBulletManagerCallback( self )
		b.draw()

	def removeBullet( self, bullet ):
		if bullet in self.bullets:
			self.bullets.remove( bullet )
			del bullet
