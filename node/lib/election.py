from lib.rpc import RPCClient
from time import sleep, time
from threading import Thread, Lock
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
        self.lock = Lock()
    
    def run_slave(self):
        print("RUNNING SLAVE: ", self.term)
        Thread(target=self.check_heartbeat).start()
    
    def run_candidate(self):
        print("RUNNING CANDIDATE: ", self.term)
        Thread(target=self.ask_vote).start()

    def run_leader(self):
        print("RUNNING LEADER: ", self.term)
        Thread(target=self.heart_beat).start()
        
    
    def check_heartbeat(self):
        while(self.state == State.SLAVE):
            current_timeout = self.leader_timeout+random()*self.random_timeout
            sleep(current_timeout)
            cur = time()
            if((cur - self.last_hearbeat)>current_timeout):
                self.lock.acquire()
                self.state = State.CANDIDATE
                self.term+=1
                self.lock.release()
                self.run_candidate()
                print("leader failed")
    
    def heart_beat(self):
        while(self.state == State.LEADER):
            sleep(0.4)
            self.ping()

    def ping(self):
        for worker in self.other_servers:
            if(self.private_ip != worker['private_ip']):
                try:
                    server = RPCClient(host=worker['private_ip'], port=worker['port'])
                    server.connect()
                    server.receive_heartbeat(self.private_ip, self.term)
                    server.disconnect()
                except:
                    i=0
                # except Exception as e:
                    # print(e)

    def ask_vote(self):
        for worker in self.other_servers:
            votes = 1
            total_votes = 1
            if(self.private_ip != worker['private_ip']):
                try:
                    server = RPCClient(host=worker['private_ip'], port=worker['port'])
                    server.connect()
                    if(server.receive_voting(self.term)):
                        votes+=1
                    total_votes+=1
                    server.disconnect()
                except:
                    i=0
                # except Exception as e:
                    # print(e)
        if(votes>total_votes/2):
            self.lock.acquire()
            print("LEADER ELECTED")
            self.state = State.LEADER
            self.run_leader()
            self.lock.release()

    def receive_voting(self, term):
        if(term>self.term):
            self.term = term
            return True
        return False
        
    def receive_heartbeat(self, leader_ip, term):
        if(term > self.term):
            self.term = term
            self.leader_ip = leader_ip    
            self.state = State.SLAVE  
            self.run_slave()  
        self.last_hearbeat = time()

        return "received the beat"




        
    
