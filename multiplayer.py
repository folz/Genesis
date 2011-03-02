'''
Created on Jun 30, 2010

@author: folz
'''

from engine.Net import netbase
import pickle
import threading
import random
import socket

class StoneServer( netbase.TCPServer ):

	def __init__( self ):
		netbase.TCPServer.__init__( self )
		self.ip = socket.gethostbyname( socket.gethostname() )
		print( "The Server's IP is: ", self.ip )
		self.connect( self.ip, 9999 )
		self.serve_forever()

	def connect_func( self, sock, host, port ):
		print ( "Server successfully connected to %s on port %s!" % ( host, port ) )

	def client_connect_func( self, sock, host, port, address ):
		print ( "A client, (ip: %s, code: %s) connected on port %s!" % ( address[0], address[1], port ) )

	def client_disconnect_func( self, sock, host, port, address ):
		print ( "A client, (ip: %s, code: %s) disconnected from port %s!" % ( address[0], address[1], port ) )

	def handle_data( self, data ):
		self.send_data( data )

	def kill( self ):
		self.quit()

class Data:

	def __init__( self, playerX, playerY, bullets, id, hit, playerFacing, flagFace, score, flagCapured ):
		self.px = playerX
		self.py = playerY
		self.pId = id
		self.bullets = bullets
		self.hit = hit
		self.pf = playerFacing
		self.ff = flagFace
		self.s = score
		self.fc = flagCapured

	def __repr__( self ):
		return "X: " + str( self.px ) + " Y: " + str( self.py ) + " id: " + str( self.pId ) + " bullets: " + str( self.bullets )

class Client:
	def __init__( self, ip, stone ):
		self.client = netbase.TCPClient()
		#ip = input("The Server's IP Address: ")#[0:-1]#'137.112.104.67'#socket.gethostbyname(socket.gethostname())#'137.112.104.67'#input("IP ADDRESS: ").split('\r')[0]
		#print((ip,9999))
		self.ip = ip
		self.client.connect( self.ip, 9999 )
		self.stone = stone
		self.running = True
		self.t = threading.Thread( None, self.update, "T" + str( random.randint( 100, 5000 ) ) )
		self.t.start()

	def kill( self ):
		self.running = False

	def sendData( self, data ):
		send = pickle.dumps( data )
		self.client.send_data( send )

	def update( self ):
		while self.running:
			data = self.client.wait_for_data()
			#OR
			#data = client.check_for_data()
			try: data = pickle.loads( data )
			except: continue
			#print(data)
			self.stone( data )

if __name__ == "__main__":
	s = StoneServer()
