from engine.Net import *
import pickle
import threading
import random
import socket

class Data:
    
    def __init__(self,playerX,playerY,bullets,id,hit,playerFacing,flagFace,score,flagCapured):
        self.px = playerX
        self.py = playerY
        self.pId = id
        self.bullets = bullets
        self.hit = hit
        self.pf = playerFacing
        self.ff = flagFace
        self.s = score
        self.fc = flagCapured
        
    def __repr__(self):
        return "X: "+str(self.px)+" Y: "+str(self.py)+" id: "+str(self.pId)+" bullets: "+str(self.bullets)


class Client:
    def __init__(self,stone):
        self.client = TCPClient()
     #   ip = input("The Server's IP Address: ")#[0:-1]#'137.112.104.67'#socket.gethostbyname(socket.gethostname())#'137.112.104.67'#input("IP ADDRESS: ").split('\r')[0]
      #  print((ip,9999))
        self.client.connect('192.168.56.1',9999)
        self.stone = stone
        self.running = True
        self.t = threading.Thread(None,self.update,"T"+str(random.randint(100,5000)))
        self.t.start()
        
    def kill(self):
        self.running = False
        
    def sendData(self,data):
        send = pickle.dumps(data)
        self.client.send_data(send)

    def update(self):
        while self.running:
            data = self.client.wait_for_data()
            #OR
         #   data = client.check_for_data()
            try: data = pickle.loads(data)
            except: continue
       #     print(data)
            self.stone(data)
