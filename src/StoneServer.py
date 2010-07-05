'''
Created on Jun 30, 2010

@author: folz
'''

from engine.Net import *
import socket

class StoneServer(TCPServer):
    
    def __init__(self):
        TCPServer.__init__(self)
        self.ip = socket.gethostbyname(socket.gethostname())
        print("The Server's IP is: ",self.ip)
        self.connect(self.ip,9999)
        self.serve_forever()
        
    def connect_func(self,sock,host,port):
        print ("Server successfully connected to %s on port %s!" % (host,port))
        
    def client_connect_func(self,sock,host,port,address):
        print ("A client, (ip: %s, code: %s) connected on port %s!" % (address[0],address[1],port))
    def client_disconnect_func(self,sock,host,port,address):
        print ("A client, (ip: %s, code: %s) disconnected from port %s!" % (address[0],address[1],port))
        
    def handle_data(self,data):
        self.send_data(data)
        
    def kill(self):
        self.quit()
        
s = StoneServer()
