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
	
	def __init__(self, window, world):
		'''
		Constructor
		'''
		self.window = window
		self.world = world
		self.following = None
		
		self.world.setViewportCallback(self)
		
		self.vpRenderOffset = (0, 0)
		
		self.xCoord = 0
		self.yCoord = 0
		self.minHorzScrollBounds = 0
		self.maxHorzScrollBounds = self.world.getWidth() - self.window.getWidth()
		self.minVertScrollBounds = 0
		self.maxVertScrollBounds = self.world.getHeight() - self.window.getHeight()
		self.velocity = geometry.Vector(0, 0)
		
		if not pygame.font.get_init():
			pygame.font.init()
		self.helveticaFnt = pygame.font.SysFont("Helvetica", 16, True, False)
	
	### -------- get/set methods -------- ###
	
	def getXCoord(self):
		return self.xCoord
	
	def getYCoord(self):
		return self.yCoord
	
	def getVelocity(self):
		return self.velocity
	
	def setVelocity(self, speed):
		self.velocity = speed
		
	def getHorzScrollSpeed(self):
		return self.velocity.x
	
	def setHorzScrollSpeed(self, speed):
		self.velocity.x = speed
	
	def getVertScrollSpeed(self):
		return self.velocity.y
	
	def setVertScrollSpeed(self, speed):
		self.velocity.y = speed
	
	def getSize(self):
		return (self.xCoord, self.yCoord, self.xCoord + self.window.getWidth(), self.yCoord + self.window.getHeight())
	
	### -------- methods that do things -------- ###
	
	def follow(self, entity):
		self.following = entity
	
	def update(self):
		if self.following is None:
			self.xCoord += self.velocity.x
			self.yCoord += self.velocity.y
		else:
		#	if self.following.facing = "left":
		#		pass
		#	elif self.following.facing = "right":
		#		pass
			
			self.xCoord = int(self.following.location.x - self.window.getWidth() / 2)
			self.yCoord = int(self.following.location.y - self.window.getHeight() / 2)
		
		if self.xCoord < self.minHorzScrollBounds:
			self.xCoord = self.minHorzScrollBounds
		if self.xCoord > self.maxHorzScrollBounds:
			self.xCoord = self.maxHorzScrollBounds
		if self.yCoord < self.minVertScrollBounds:
			self.yCoord = self.minVertScrollBounds
		if self.yCoord > self.maxVertScrollBounds:
			self.yCoord = self.maxVertScrollBounds
	
	
	def render(self, delta):
		self.update()
		
		pygame.Surface.fill(self.world, ((0, 0, 0)), pygame.Rect(self.xCoord, self.yCoord, self.xCoord + self.window.getWidth(), self.yCoord + self.window.getHeight()))
		buffer = pygame.Surface(self.world.get_size())

		self.world.redraw(delta)
		
		buffer.blit(self.world, (0, 0), pygame.Rect((self.xCoord, self.yCoord), (self.xCoord + self.window.getWidth(), self.yCoord + self.window.getHeight())))
			
		self.window.screen.blit(buffer, self.vpRenderOffset)
		# self.window.screen.blit(self.helveticaFnt.render('(' + str(self.xCoord) + ", " + str(self.yCoord) + ")", True, (255, 255, 255)), (0, 0))
		# pygame.display.flip()
