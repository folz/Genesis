'''
Created on Jun 21, 2010

@author: folz
'''

import pygame, math
from pygame.locals import *
from engine import geometry
from engine import misc

class Entity( pygame.sprite.Sprite ):
	'''
	An entity represents any element that appears in a World
	'''
	def __init__( self, image=None,
				location=geometry.Vector( 0, 0 ),
				velocity=geometry.Vector( 0, 0 ) ):

		pygame.sprite.Sprite.__init__( self )

		if isinstance( image, pygame.Surface ):
			self.image = image
		else:
			self.image = misc.load_image( image )

		if isinstance( location, geometry.Vector ):
			self.location = location
		else:
			self.location = geometry.Vector( location[0], location[-1] )

		if isinstance( velocity, geometry.Vector ):
			self.velocity = velocity
		else:
			self.velocity = geometry.Vector( velocity[0], velocity[-1] )

		if image is not None:
			self.rect = self.image.get_rect()
		self.boundingPoly = geometry.Rect( self.rect.x, self.rect.y, self.get_width(), self.get_height() )

	def __repr__( self ):
		return "Entity %s at (%d, %d) on %s with vector %s" % ( self.image, self.location.x, self.location.y, self.world, self.velocity )

	def set_world_callback( self, world ):
		self.world = world

	def move( self, delta ):
		'''
		This should be overwritten by subclasses
		'''
		pass

	def get_width( self ):
		return self.image.get_width()

	def get_height( self ):
		return self.image.get_height()

	def get_size( self ):
		return self.get_width(), self.get_height()

	def get_bounding_poly( self ):
		return self.boundingPoly

	def set_bounding_poly( self, poly ):
		self.boundingPoly = poly

	def is_on_screen( self ):
		return self.location.x + self.get_width() >= self.world.viewport.get_x_coord() and self.location.x <= self.world.viewport.get_x_coord() + self.world.get_width() and self.location.y + self.get_height() >= self.world.viewport.get_y_coord() and self.location.y <= self.world.viewport.get_y_coord() + self.world.get_height()

	def draw( self ):
		self.world.blit( self.image, self.rect )
