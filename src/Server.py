from engine.Net import *
class ServerHandler(TCPServer):
    def __init__(self):
        TCPServer.__init__(self)
    def handle_data(self,data):
        #process (perhaps)
        self.send_data(data)#something)
        
    def connect_func(self,sock,host,port):
        print ("Server successfully connected to %s on port %s!" % (host,port))
    def client_connect_func(self,sock,host,port,address):
        print ("A client, (ip: %s, code: %s) connected on port %s!" % (address[0],address[1],port))
    def client_disconnect_func(self,sock,host,port,address):
        print ("A client, (ip: %s, code: %s) disconnected from port %s!" % (address[0],address[1],port))
        
def main():
    ip = '137.112.104.67'#input("IP ADDRESS: ").split('\r')[0]
    server = ServerHandler()
    server.connect(ip,5484)
    server.serve_forever()
    server.quit()

if __name__ == '__main__': main()
