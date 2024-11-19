from lib.rpc import RPCClient

server = RPCClient('0.0.0.0', 3200)

server.connect()

print(server.add(5, 6))
print(server.sub(5, 6))

server.disconnect()