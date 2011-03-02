'''
Created on Jun 23, 2010

@author: folz
'''

import pygame, math
from pygame.locals import *
from engine import *
from engine.misc import *

import multiplayer
import managers
import entities

id = int ( input ( "id? " ) )
player2 = None

def useData( data ):
	global player2, id#,networkBullets
	if not player2: return
	if data is None: return
	if data.pId != id:
		#print(data)
		player2.location = geometry.Vector( data.px, data.py )
		player2.setFacing( data.pf )
		if id == 2:
			flag.setFacing( data.ff )
			flag2.updateScore( data.s )
			if data.fc: flag.wasCapturedBy( player2 )
			elif not data.fc: flag.release()
		else:
			flag2.setFacing( data.ff )
			flag.updateScore( data.s )
			if data.fc: flag2.wasCapturedBy( player2 )
			elif not data.fc: flag2.release()
		#networkBullets.fromNetwork(data.bullets)
		for b in data.bullets:
			player2.gun.addBullet( ( b[0], b[1] ), ( b[2], b[3] ) )
		if data.hit: player.wasHit()

svrip = input ( "server ip? " )
client = multiplayer.Client( svrip, useData )

# set the dimensions of the display window
SIZE = WIDTH, HEIGHT = 640, 480

# create the window and display it
window = gamewindow.GameWindow( SIZE )
window.setTitle( "Weathered Stone" )
window.setFlags( pygame.HWSURFACE | pygame.DOUBLEBUF )# | pygame.FULLSCREEN)
window.display()

pygame.font.init()
helveticaFnt = pygame.font.SysFont( "Myriad Pro", 16, True, False )


clock = pygame.time.Clock()
keys = {pygame.K_ESCAPE : False, pygame.K_LEFT : False, pygame.K_RIGHT : False, pygame.K_z : False, pygame.K_x : False}


#load the tile data
#tiles = [pygame.image.load('data\\block%d.png' % n).convert() for n in range(4)]
#tileWidth, tileHeight = tiles[0].get_size()

# get the value of every char c in every string s in the map file
#tileData = [[int(c) for c in s[0:-1]] for s in open(os.path.join("data", "map.gen")).readlines()]

# create the world that everything will be rendered in
# because of parallax scrolling, make sure the world is 4/5 the background



# create the world we'll be rendering entities on
#world = World((len(tileData[0]) * tileWidth, len(tileData) * tileHeight))
world = world.World( ( 2000, 2000 ) )
world.setBackground( "giantbg.png" )
world.setGravity( geometry.Vector( 0, 1 ) )
world.debug = True

global networkBullets
networkBullets = managers.NetworkBulletManager( world )


def createBlock( x, y, w, h ):

	p = geometry.Terrain( [( x, y ), ( x + w, y ), ( x + w, y + h ), ( x, y + h )], world )
	world.addTerrain( p )

def makeTerrain():
	leftWall = geometry.Slope( [( 0, 0 ), ( 0, 2000 )] )
	world.addTerrain( leftWall )
	rightWall = geometry.Slope( [( 2000, 0 ), ( 2000, 2000 )] )
	world.addTerrain( rightWall )
	topWall = geometry.Slope( [( 0, 0 ), ( 2000, 0 )] )
	world.addTerrain( topWall )
	bottomWall = createBlock( 0, 2000, 2000, 50 )
	#world.addTerrain(bottomWall)

	#top level
	p = geometry.Terrain( [( 1350, 350 ), ( 1500, 350 ), ( 1500, 250 )], world )
	world.addTerrain( p )
	p = geometry.Terrain( [( 700, 200 ), ( 1050, 350 ), ( 1050, 400 ), ( 700, 250 )], world )
	world.addTerrain( p )

	createBlock( 1700, 1900, 100, 100 )
	createBlock( 1900, 1800, 100, 100 )
	createBlock( 1500, 1800, 500, 20 )
	createBlock( 0, 200, 300, 60 )
	createBlock( 200, 0, 50, 80 )
	createBlock( 300, 150, 50, 50 )
	createBlock( 300, 200, 400, 50 )
	createBlock( 1050, 350, 850, 50 )
	createBlock( 1500, 250, 100, 100 )
	createBlock( 1800, 200, 150, 50 )
	createBlock( 1200, 125, 150, 50 )

	#second
	createBlock( 800, 500, 1300, 50 )
	createBlock( 800, 450, 75, 75 )
	createBlock( 0, 500, 600, 50 )
	createBlock( 700, 650, 100, 50 )

	createBlock( 0, 800, 1600, 60 )
	createBlock( 1700, 800, 400, 60 )
	createBlock( 400, 740, 50, 60 )
	createBlock( 600, 600, 100, 50 )
	createBlock( 1800, 750, 50, 50 )
	createBlock( 200, 700, 100, 50 )
	createBlock( 400, 750, 50, 50 )
	createBlock( 1800, 700, 100, 50 )
	createBlock( 1200, 700, 75, 40 )
	createBlock( 1000, 750, 50, 50 )
	createBlock( 850, 740, 100, 40 )
	createBlock( 150, 375, 200, 50 )

	createBlock( 0, 920, 250, 50 )
	createBlock( 300, 920, 400, 50 )
	createBlock( 780, 920, 1000, 50 )
	createBlock( 500, 890, 20, 30 )

	createBlock( 50, 1050, 1950, 30 )
	createBlock( 300, 1030, 20, 20 )
	createBlock( 600, 1020, 30, 30 )
	createBlock( 1200, 1030, 20, 50 )

	createBlock( 0, 1150, 500, 20 )
	createBlock( 550, 1150, 1500, 20 )
	createBlock( 300, 1130, 30, 20 )
	createBlock( 800, 1120, 50, 30 )
	createBlock( 1400, 1120, 20, 30 )

	createBlock( 0, 1300, 1950, 20 )
	createBlock( 200, 1220, 100, 20 )
	createBlock( 100, 1270, 30, 30 )
	createBlock( 500, 1220, 250, 20 )
	createBlock( 800, 1260, 40, 40 )
	createBlock( 1200, 1270, 30, 30 )
	createBlock( 1600, 1220, 60, 10 )

	createBlock( 0, 1500, 750, 20 )
	createBlock( 800, 1500, 1200, 20 )
	createBlock( 200, 1400, 120, 15 )
	createBlock( 470, 1420, 100, 15 )
	createBlock( 750, 1410, 86, 15 )
	createBlock( 1200, 1400, 130, 15 )
	createBlock( 1600, 1400, 80, 15 )
	createBlock( 100, 1450, 50, 50 )
	createBlock( 350, 1460, 40, 40 )
	createBlock( 940, 1480, 20, 20 )
	createBlock( 1300, 1450, 50, 50 )
	createBlock( 1700, 1470, 30, 30 )
	createBlock( 1800, 1400, 200, 20 )

	createBlock( 0, 1750, 300, 20 )
	createBlock( 350, 1750, 1000, 20 )
	createBlock( 1400, 1750, 600, 20 )
	createBlock( 200, 1730, 20, 20 )
	createBlock( 600, 1680, 150, 20 )
	createBlock( 1200, 1700, 50, 50 )
	createBlock( 1600, 1650, 100, 20 )
	createBlock( 1800, 1720, 30, 30 )
	createBlock( 750, 1600, 200, 20 )

	createBlock( 0, 1850, 600, 20 )
	createBlock( 300, 1840, 20, 20 )




# create the viewport that will view the world
viewport = viewport.Viewport( window, world )

# create a player character
if id == 1: player = entities.PlayerEntity( "blue", ( 1940, 1940 ) )
else: player = entities.PlayerEntity( "red", ( 100, 100 ) )
world.addEntity( player )
player.addGun( managers.BulletManager( player ) )

flag = entities.FlagEntity( "red", ( 50, 175 ) )
flag2 = entities.FlagEntity( "blue", ( 1950, 1975 ) )
world.addEntity( flag )
world.addEntity( flag2 )

polygons = ()

viewport.follow( player )

running = True
scrollX = 4
scrollY = 4

delta = 0.0

def handle_keys( keyEvent ):
	key = keyEvent.key

	if keyEvent.type == pygame.KEYDOWN:
		keys[key] = True

	if keyEvent.type == pygame.KEYUP:
		keys[key] = False

def handle_events():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			global running
			running = False
			client.kill()

		elif event.type in ( pygame.KEYDOWN, pygame.KEYUP ):
			handle_keys( event )

if id == 2: player2 = entities.PlayerEntity( "blue", ( 1940, 1940 ), "green-soldier.png" )
else: player2 = entities.PlayerEntity( "red", ( 100, 100 ), "green-soldier.png" )
world.addEntity( player2 )
world.setPlayer2( player2 )
player2.addGun( managers.BulletManager( player2 ) )



def sendData():
	global client, id, player2
	bullets = player.gun.bullets
	bs = []
	for b in bullets:
		if not b.sent:
			b.sent = True
			bs.append( ( b.location.x, b.location.y, b.velocity.x, b.velocity.y ) )

	flagFace = ""
	if id == 1:
		flagFace = flag.facing
		score = flag2.score
		cap = flag.captured
	else:
		flagFace = flag2.facing
		score = flag.score
		cap = flag2.captured
	data = multiplayer.Data( player.location.x, player.location.y, bs, id, player2.hit, player.facing, flagFace, score, cap )
	client.sendData( data )
	player2.hit = False

def doLogic():
	player.moving = False

	if keys[pygame.K_ESCAPE]:
		pygame.event.post( pygame.event.Event( pygame.QUIT ) )

	if keys[pygame.K_LEFT]:
		player.moving = True
		player.facing = "left"
		if player.wasFacing == "right":
			player.velocity.x = 0
		player.velocity.x += -.6

	if keys[pygame.K_RIGHT]:
		player.moving = True
		player.facing = "right"
		if player.wasFacing == "left":
			player.velocity.x = 0
		player.velocity.x += .6

	if keys[pygame.K_z]:
		player.startJumping()

	if keys[pygame.K_x]:
		player.shoot()
		keys[pygame.K_x] = False

	global delta
	player.move( delta )

makeTerrain()

#pygame.mixer.music.load('data\\genesis.mp3')
#pygame.mixer.

while running:
	global delta, networkBullets
	delta = clock.tick( 30 ) #FPS
	handle_events()
	doLogic()
	sendData()
	viewport.render( delta )
	networkBullets.draw()
	window.screen.blit( helveticaFnt.render( "Blue Team Score: " + str( flag2.score ), True, ( 0, 0, 255 ), ( 0, 0, 0 ) ), ( 0, 0 ) )
	window.screen.blit( helveticaFnt.render( "Red Team Score: " + str( flag.score ), True, ( 255, 0, 0 ), ( 0, 0, 0 ) ), ( 0, 18 ) )
	pygame.display.flip()

