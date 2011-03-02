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
		self.players = []
		self.terrain = []
		self.delta = 0.0
		self.player2 = None

	### -------- get/set methods -------- ###

	def setPlayer2( self, p2 ):
		self.player2 = p2

	def getPlayer2( self ):
		return self.player2

	def setBackground( self, background ):
		self.background = misc.load_image( background )

	def getWidth( self ):
		return pygame.Surface.get_width( self )

	def getHeight( self ):
		return pygame.Surface.get_height( self )

	def setDebug( self, bool ):
		self.debug = bool

	def getEntities( self ):
		return pygame.Surface.sprites( self )

	def setViewportCallback( self, viewport ):
		self.viewport = viewport

	def setWindowCallback( self, window ):
		self.window = window

	def getGravity( self ):
		return self.gravity

	def setGravity( self, gravity ):
		self.gravity = gravity

	def getTerrain( self ):
		return self.terrain

	### -------- methods that do things -------- ###

	def addEntity( self, object ):
		pygame.sprite.Group.add( self, object )
		if hasattr( object, "gun" ):
			self.players.append( object )
		object.setWorldCallback( self )

	def addTerrain( self, object ):
		self.terrain.append( object )
		object.setWorldCallback( self )

	def redraw( self, delta ):
		self.blit( self.background, ( 0, 0 ), self.viewport.getSize() )
		self.delta = delta
		if self.debug:
			for terrain in self.getTerrain():
				terrain.debug()
		for entity in self.sprites():
			entity.move( delta )
			if entity.isOnScreen():
				entity.draw()

