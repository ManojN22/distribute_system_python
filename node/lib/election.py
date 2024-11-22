from lib.rpc import RPCClient
from time import sleep, time
from threading import Thread
from random import random
import enum

class State(enum.Enum):
    SLAVE=1
    CANDIDATE=2
    LEADER=3



class Worker:
    def __init__(self, other_servers, private_ip, leader_timeout, random_timeout) :
        self.other_servers = other_servers
        self.private_ip = private_ip
        self.last_hearbeat = 0
        self.leader_ip = private_ip
        self.leader_timeout = leader_timeout
        self.random_timeout = random_timeout
        self.state = State.SLAVE
        self.term = 0
        self.voted = False
    
    def run_slave(self):
        Thread(target=self.check_heartbeat).start()
    
    def run_candidate(self):
        Thread(target=self.check_heartbeat).start()
        
    
    def check_heartbeat(self):
        while(self.state == State.SLAVE):
            current_timeout = self.leader_timeout+random()*self.random_timeout
            sleep(current_timeout)
            cur = time()
            if((cur - self.last_hearbeat)>current_timeout):
                self.state = State.CANDIDATE
                self.term+=1
                Thread(target=self.run_candidate).start()
                # print("leader failed")

    def receive_heartbeat(self, private_ip, term):
        if()
        self.last_hearbeat = time()

        return "received the beat"
    
    def heart_beat(self):
        while(True):
            sleep(0.1)
            self.ping()

    def ping(self):
        for worker in self.other_servers:
            if(self.private_ip != worker['private_ip']):
                try:
                    server = RPCClient(host=worker['private_ip'], port=worker['port'])
                    server.connect()
                    print(server.respond_hello(self.private_ip))
                    server.disconnect()
                except Exception as e:
                    print(e)

    def ask_vote(self):
        for worker in self.other_servers:
            if(self.private_ip != worker['private_ip']):
                try:
                    server = RPCClient(host=worker['private_ip'], port=worker['port'])
                    server.connect()
                    print(server.respond_hello(self.private_ip))
                    server.disconnect()
                except Exception as e:
                    print(e)
    
    def voting(self):
        if(vote==)




        
    
