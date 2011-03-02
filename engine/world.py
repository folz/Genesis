'''
Created on Jun 21, 2010

@author: folz
'''

import weakref
import pygame
from pygame.locals import *
from engine import misc


class World( pygame.Surface, pygame.sprite.Group ):
	'''
	A World is a Surface Group where you draw Entities. It is viewed by a Viewpoint
	'''

	def __init__( self, size ):
		self.debug = False
		pygame.Surface.__init__( self, size )
		self.convert()
		self.background = pygame.Surface( size ).convert()
		self.spritedict = {} # unused, but required for pygame.sprite.Group
		self.gravity = 0
		self.terrain = []
		self.names = {}
		self.attributes = {}
		self.delta = 0.0

	### -------- get/set methods -------- ###

	def set_background( self, background ):
		self.background = misc.load_image( background )

	def get_width( self ):
		return pygame.Surface.get_width( self )

	def get_height( self ):
		return pygame.Surface.get_height( self )

	def set_debug( self, bool ):
		self.debug = bool

	def get_entities( self ):
		return pygame.sprite.Group.sprites( self )

	def set_viewport_callback( self, viewport ):
		self.viewport = viewport

	def set_window_callback( self, window ):
		self.window = window

	def get_gravity( self ):
		return self.gravity

	def set_gravity( self, gravity ):
		self.gravity = gravity

	def get_terrain( self ):
		return self.terrain
	
	def set_entity_name(self, entity, name):
		if entity in self.get_entities():
			self.names[name] = entity
	
	def get_entity_by_name(self, name):
		return self.names[name]
	
	def get_entities_by_attribute(self, attribute):
		if self.attributes[attribute] != None:
			return self.attributes[attribute]
		else:
			return None
	### -------- methods that do things -------- ###

	def add_entity( self, object, attrs=None ):
		pygame.sprite.Group.add( self, object )
		object.set_world_callback( self )
		if attrs != None:
			if type(attrs) in [type("")]:
				attrs = [attrs]
			for attr in attrs:
				try:
					self.attributes[attr].append(object)
				except:
					self.attributes[attr] = [object]
						
	def add_terrain( self, object ):
		self.terrain.append( object )
		object.set_world_callback( self )

	def redraw( self, delta ):
		self.blit( self.background, ( 0, 0 ), self.viewport.get_size() )
		self.delta = delta
		if self.debug:
			for terrain in self.get_terrain():
				terrain.debug()
		for entity in self.sprites():
			entity.move( delta )
			if entity.is_on_screen():
				entity.draw()