from lib.rpc import RPCClient

class Elections:
    def __init__(self, other_servers, private_ip) :
        self.other_servers = other_servers
        self.private_ip = private_ip

        
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
