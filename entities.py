'''
Created on Jun 24, 2010

@author: folz
'''

import math, pygame, sys
from pygame.locals import *
from engine import *




class BulletEntity( entity.Entity ):
	'''
	A Bullet is something you shoot. It is handled by a BulletManager
	'''

	MAX_SPEED_X = 100
	MAX_SPEED_Y = 100

	def __init__( self, location, velocity, facing ):
		'''
		Constructor
		'''
		entity.Entity.__init__( self, "bullet.png", location, velocity )
		if facing == "left":
			self.image = pygame.transform.flip( self.image, True, False )
		self.used = False
		self.sent = False
		self.rect = pygame.Rect( self.location.x, self.location.y, self.getWidth(), self.getHeight() )

	def setBulletManagerCallback( self, bulletmanager ):
		self.bulletmanager = bulletmanager

	def networkBullet( self ):
		p2 = self.world.getPlayer2()
		self.boundingPoly = geometry.Rect( self.location.x, self.location.y, self.getWidth(), self.getHeight() )
		mtd = p2.boundingPoly.collide( self.boundingPoly )
		if mtd != False:
			p2.takeHit()
			self.used = True


	def move( self ):
		if( self.velocity.x == 0 ):
			return

		self.networkBullet()

		if self.used:
			self.bulletmanager.removeBullet( self )
			del self
			return

		if self.velocity.x > self.MAX_SPEED_X:
			self.velocity.x = self.MAX_SPEED_X
		if self.velocity.x < -self.MAX_SPEED_X:
			self.velocity.x = -self.MAX_SPEED_X
		if self.velocity.y > self.MAX_SPEED_Y:
			self.velocity.y = self.MAX_SPEED_Y
		if self.velocity.y < -self.MAX_SPEED_Y:
			self.velocity.y = -self.MAX_SPEED_Y

		self.location.x += self.velocity.x #* (PIXELSPERVECTOR / delta)
		self.location.y += self.velocity.y #* (PIXELSPERVECTOR / delta)

		self.rect = pygame.Rect( self.location.x, self.location.y, self.getWidth(), self.getHeight() )

		if self.location.x < 0 or self.location.x > self.world.getWidth() or self.location.y < 0 or self.location.y > self.world.getHeight():
			self.bulletmanager.bullets.remove( self )

		self.checkCollisions()

	def checkCollisions( self ):
		if not self.used:
			self.boundingPoly = geometry.Rect( self.location.x, self.location.y, self.getWidth(), self.getHeight() )
			for terrain in self.world.getTerrain():
				mtd = self.boundingPoly.collide( terrain )
				if mtd != False:
					self.used = True
		if self.used:
			self.bulletmanager.removeBullet( self )
			del self

	def draw( self ):
		entity.Entity.draw( self )

class FlagEntity( entity.Entity ):

	def __init__( self, team, location=geometry.Vector( 0, 0 ), velocity=geometry.Vector( 0, 0 ) ):
		'''
		Constructor
		'''
		self.start = geometry.Vector( location[0], location[1] )
		entity.Entity.__init__( self, "flag_%s.png" % team, location, velocity )
		self.facing = "right"
		self.wasFacing = self.facing
		self.team = team
		self.captured = False
		self.capturer = None
		self.scale = 1
		self.score = 0

	def setFacing( self, newFacing ):
		self.wasFacing = self.facing
		self.facing = newFacing

	def wasCapturedBy( self, entity ):
		self.captured = True
		self.capturer = entity
		self.capturer.flag = self

	def release( self ):
		if self.capturer is not None:
			self.capturer.flag = None
			self.capturer.hasFlag = False
		self.facing = "right"
		self.captured = False
		self.capturer = None
		self.location = self.start.copy()

	def move( self, delta ):
		if self.captured and self.capturer != None:
			pass
		self.checkCollisions()

	def updateScore( self, score ):
		self.score = score

	def checkCollisions( self ):
		self.boundingPoly = geometry.Rect( self.location.x, self.location.y, self.getWidth(), self.getHeight() )
		if not self.captured:
			for player in self.world.players:
				if player.team != self.team:
					mtd = self.boundingPoly.collide( player.boundingPoly )
					if mtd != False:
						self.wasCapturedBy( player )
						player.hasFlag = True
						print( "captured" )
				else:
					mtd = self.boundingPoly.collide( player.boundingPoly )
					if mtd != False and player.hasFlag and self.captured == False:
						player.flag.release()
						self.score += 1
						print( "SCORED" )


		else:
			if self.capturer.facing == "left":
				self.location.x = self.capturer.location.x + self.capturer.getWidth() / 2
				self.location.y = self.capturer.location.y
			elif self.capturer.facing == "right":
				self.location.x = self.capturer.location.x - self.capturer.getWidth() / 2
				self.location.y = self.capturer.location.y

		self.rect = pygame.Rect( self.boundingPoly.realPoints[0][0], self.boundingPoly.realPoints[0][1], self.boundingPoly.width, self.boundingPoly.height )

	def draw( self ):
		if self.facing == "right" and self.scale == -1:
			self.image = pygame.transform.flip( self.image, True, False )
			self.scale = 1
		elif self.facing == "left" and self.scale == 1:
			self.image = pygame.transform.flip( self.image, True, False )
			self.scale = -1

		entity.Entity.draw( self )
		self.wasFacing = self.facing


'''
Created on Jun 24, 2010

@author: folz
'''

class PlayerEntity( entity.Entity ):
	'''
	classdocs
	'''

	MAXXSPEED = 10
	MAXYSPEED = 20

	def __init__( self, team, location=geometry.Vector( 0, 0 ), image="brown-soldier.png", velocity=geometry.Vector( 0, 0 ) ):
		'''
		Constructor
		'''
		entity.Entity.__init__( self, image, location, velocity )
		self.moving = False
		self.startLocation = location
		self.wasFacing = "right"
		self.facing = "right"
		self.jumping = True
		self.shooting = False
		self.gun = None
		self.team = team
		self.hasFlag = False
		self.flag = None
		self.hit = False
		self.health = 10
		self.active = 200
		self.scale = 1

	def reset( self ):
		self.moving = False
		self.wasFacing = "right"
		self.facing = "right"
		self.jumping = True
		self.shooting = False
		self.hit = False
		self.health = 10
		self.location = geometry.Vector( self.startLocation[0], self.startLocation[1] )
		self.active = 0
		self.rect = pygame.Rect( self.boundingPoly.realPoints[0][0], self.boundingPoly.realPoints[0][1], self.boundingPoly.width, self.boundingPoly.height )

	def setFacing( self, newFace ):
		self.wasFacing = self.facing
		self.facing = newFace

	def wasHit( self ):
		if self.hasFlag:
			self.hasFlag = False
			self.flag.release()
		self.health -= 1
		if self.health == 0:
			self.reset()

	def takeHit( self ):
		self.hit = True
		if self.hasFlag:
			self.hasFlag = False
			self.flag.release()
	def startJumping( self ):
		if not self.jumping:
			self.velocity += geometry.Vector( 0, -20 )
			self.jumping = True


	def addGun( self, gun ):
		self.gun = gun

	def shoot( self ):
		if not self.active == 200: return
		offset = 0
		if self.facing == "left":
			xvel = -20 + self.velocity.x * .2
			offset = -self.getWidth() - 1
		elif self.facing == "right":
			xvel = 20 + self.velocity.x * .2
			offset = self.getWidth() + 1
		self.gun.addBullet( ( self.location.x + offset, self.location.y + self.getHeight() / 2 ), ( xvel, 0 ), self.facing ) # TODO get velocity based on user mouse position

	def move( self, delta ):
		if not self.active == 200:
			self.active += 1
			return
		if abs( self.velocity.x ) > .001 or self.jumping:
			self.velocity += self.world.gravity

		if ( abs( self.velocity.x ) > .001 and not self.moving ):# and not self.jumping:
			self.velocity.x *= .5

		if self.velocity.x > self.MAXXSPEED:
			self.velocity.x = self.MAXXSPEED
		if self.velocity.x < -self.MAXXSPEED:
			self.velocity.x = -self.MAXXSPEED
		if self.velocity.y > self.MAXYSPEED:
			self.velocity.y = self.MAXYSPEED
		if self.velocity.y < -self.MAXYSPEED:
			self.velocity.y = -self.MAXYSPEED

		self.location.x += self.velocity.x #* (PIXELSPERVECTOR / delta)
		self.location.y += self.velocity.y #* (PIXELSPERVECTOR / delta)

		self.gun.shoot()

		self.checkCollisions()


	def checkCollisions( self ):
		if not self.active == 200: return
		self.boundingPoly = geometry.Rect( self.location.x, self.location.y, self.getWidth(), self.getHeight() )
		for terrain in self.world.getTerrain():
			mtd = self.boundingPoly.collide( terrain )

			if mtd != False: # if we're colliding with the terrain
				self.location += mtd # adjust our position so that we're not colliding anymore

				if self.boundingPoly.isAbove == True: # if we're above whatever we're colliding with
					self.velocity.y = 0
					self.jumping = False
				elif self.boundingPoly.isAbove == False: # if we're below whatever we're colliding with
					self.velocity.y = 0
					self.jumping = True
				elif self.boundingPoly.isAbove == None: # this shouldn't happen, but sometimes it comes back neither true nor false
					self.velocity += self.world.gravity

				elif self.boundingPoly.isLeft == True: # if we're to the left of whatever we're colliding with
					self.velocity.x = 0
				elif self.boundingPoly.isLeft == False: #if we're to the right of whatever we're colliding with
					# !! actually, disregard the below comment - we're not using it
					''' 
					okay, so technically, we're to the left of our collision. but if we try to set velocity
					this way, we'll end up setting our velocity to 0 no matter what. so instead, let's cheat and
					not bother to check left-side collisions
					'''
					self.velocity.x = 0
					pass
				elif self.boundingPoly.isLeft == None: # this shouldn't happen, but sometimes it comes back neither true nor false
					pass
			else: # we're not colliding with anything
				pass#self.jumping = True

		self.rect = pygame.Rect( self.boundingPoly.realPoints[0][0], self.boundingPoly.realPoints[0][1], self.boundingPoly.width, self.boundingPoly.height )
		self.wasVelocity = self.velocity

	def draw( self ):
		if self.facing == "right" and self.scale == -1:
			self.image = pygame.transform.flip( self.image, True, False )
			self.scale = 1
		elif self.facing == "left" and self.scale == 1:
			self.image = pygame.transform.flip( self.image, True, False )
			self.scale = -1

		entity.Entity.draw( self )
		self.wasFacing = self.facing

