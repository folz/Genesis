'''
Created on Jun 21, 2010

@author: folz
'''

import pygame, math
from pygame.locals import *
from engine import geometry

class Viewport:
	'''
	A Viewport draws a smaller portion of a World on a GameWindow
	'''

	def __init__( self, window, world ):
		'''
		Constructor
		'''
		self.window = window
		self.world = world
		self.following = None

		self.world.set_viewport_callback( self )

		self.vpRenderOffset = ( 0, 0 )

		self.xCoord = 0
		self.yCoord = 0
		self.minHorzScrollBounds = 0
		self.maxHorzScrollBounds = self.world.get_width() - self.window.get_width()
		self.minVertScrollBounds = 0
		self.maxVertScrollBounds = self.world.get_height() - self.window.get_height()
		self.velocity = geometry.Vector( 0, 0 )

		if not pygame.font.get_init():
			pygame.font.init()
		self.helveticaFnt = pygame.font.SysFont( "Helvetica", 16, True, False )

	### -------- get/set methods -------- ###

	def get_x_coord( self ):
		return self.xCoord

	def get_y_coord( self ):
		return self.yCoord

	def get_velocity( self ):
		return self.velocity

	def set_velocity( self, speed ):
		self.velocity = speed

	def get_horizontal_scroll_speed( self ):
		return self.velocity.x

	def set_horizontal_scroll_speed( self, speed ):
		self.velocity.x = speed

	def get_vertical_scroll_speed( self ):
		return self.velocity.y

	def set_vertical_scroll_speed( self, speed ):
		self.velocity.y = speed

	def get_size( self ):
		return ( self.xCoord, self.yCoord, self.xCoord + self.window.get_width(), self.yCoord + self.window.get_height() )

	### -------- methods that do things -------- ###

	def follow( self, entity ):
		self.following = entity

	def update( self ):
		if self.following is None:
			self.xCoord += self.velocity.x
			self.yCoord += self.velocity.y
		else:
		#	if self.following.facing = "left":
		#		pass
		#	elif self.following.facing = "right":
		#		pass

			self.xCoord = int( self.following.location.x - self.window.get_width() / 2 )
			self.yCoord = int( self.following.location.y - self.window.get_height() / 2 )

		if self.xCoord < self.minHorzScrollBounds:
			self.xCoord = self.minHorzScrollBounds
		if self.xCoord > self.maxHorzScrollBounds:
			self.xCoord = self.maxHorzScrollBounds
		if self.yCoord < self.minVertScrollBounds:
			self.yCoord = self.minVertScrollBounds
		if self.yCoord > self.maxVertScrollBounds:
			self.yCoord = self.maxVertScrollBounds


	def render( self, delta ):
		self.update()

		pygame.Surface.fill( self.world, ( ( 0, 0, 0 ) ), pygame.Rect( self.xCoord, self.yCoord, self.xCoord + self.window.get_width(), self.yCoord + self.window.get_height() ) )
		buffer = pygame.Surface( self.world.get_size() )

		self.world.redraw( delta )

		buffer.blit( self.world, ( 0, 0 ), pygame.Rect( ( self.xCoord, self.yCoord ), ( self.xCoord + self.window.get_width(), self.yCoord + self.window.get_height() ) ) )

		self.window.screen.blit( buffer, self.vpRenderOffset )
		# self.window.screen.blit(self.helveticaFnt.render('(' + str(self.xCoord) + ", " + str(self.yCoord) + ")", True, (255, 255, 255)), (0, 0))
		# pygame.display.flip()
