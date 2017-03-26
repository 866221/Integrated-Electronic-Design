from socket import *
import Read_Socket as Read

def createServer():
	serverSocket = socket(AF_INET, SOCK_STREAM)
	serverSocket.bind(('localhost', 12350))
	serverSocket.listen(5)
	while(True):
		(client, address) = serverSocket.accept()
		if client != None:
			print 'Found Client!'
			Read.start()
			output = Read.Read()
			client.send(output)
			client.close()

createServer()
