import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverAddress = ('localhost', 55555)
sock.connect(serverAddress)
sock.sendall("SENSOR")
sock.close()