from lib.rpc import RPCServer, RPCClient
# from lib.test import 
from lib.election import Worker
from lib.hello import respond_hello
import json
from netifaces import ifaddresses
from threading import Thread
from time import sleep


class Node(Worker):
    def __init__(self):
        self.setting_config()
        if self.a_ok==False:
            exit(1)
        self.server = RPCServer(host=self.private_ip, port=self.port)
        super().__init__(self.other_servers,self.private_ip)
        self.server.registerMethod(respond_hello)
    

    def run(self):
        self.server.run()

    def setting_config(self):
        self.a_ok = False
        with open('config.json', 'r') as file:
            config = json.load(file)
            addrs = ifaddresses('eth1')
            self.private_ip = addrs[2][0]['addr']
            self.other_servers = []
            for server in config['servers']:
                if(server['private_ip'] == self.private_ip):
                    self.a_ok = True
                    self._id = server['_id']
                    self.port = server['port']
                else:
                    self.other_servers.append({
                        '_id' : server['_id'],
                        'private_ip' : server['private_ip'],
                        'port' : server['port']
                    })
            
    
        
            

def main():
    node = Node()
    if node.a_ok==False:
        exit(1)
    Thread(target=node.run).start()
    sleep(4)
    Thread(target=node.heart_beat).start()
    

    

if __name__ == "__main__":
    main()



