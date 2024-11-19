def add(a, b):
    return a+b

def sub(a, b):
    return a-b

from lib.rpc import RPCServer

server = RPCServer(port=3200)

server.registerMethod(add)
server.registerMethod(sub)

server.run()