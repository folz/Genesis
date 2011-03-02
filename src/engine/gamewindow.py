'''
Created on Jun 22, 2010

@author: folz
'''

import pygame
from pygame.locals import *

class GameWindow:
	'''
	A GameWindow is the actual window where Worlds are drawn.
	Sometimes it's fullscreen
	'''
	def __init__( self, size=( 800, 600 ), title="PyGame", flags=pygame.SWSURFACE, screen=None ):
		self.width, self.height = self.size = size
		self.title = title
		self.flags = flags
		self.screen = screen
		self.visible = False

	### -------- get/set methods -------- ###

	def getWidth( self ):
		return self.width

	def setWidth( self, width ):
		self.width = width
		self.size = ( self.width, self.height )
		self.recreate()

	def getHeight( self ):
		return self.height

	def setHeight( self, height ):
		self.height = height
		self.size = ( self.width, self.height )
		self.recreate()

	def getSize( self ):
		return self.size

	def setSize( self, size ):
		self.size = size
		self.width, self.height = self.size
		self.recreate()

	def getFlags( self ):
		return self.flags

	def setFlags( self, flags ):
		self.flags = flags
		self.recreate()

	def getTitle( self ):
		return self.screen.get_caption()

	def setTitle( self, title ):
		self.title = title

	### -------- methods that actually do things -------- ###

	def worldCallback( self, callback ):
		self.callback = callback

	def recreate( self ):
		if self.visible:
			pygame.display.quit()
			self.visible = False
			self.display()
		else:
			pass

	def display( self ):
		if not self.visible:
			pygame.display.init()
			pygame.display.set_caption( self.title )
			self.screen = pygame.display.set_mode( self.size, self.flags )
			self.visible = True
		else:
			pass

