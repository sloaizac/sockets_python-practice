#!/usr/bin/env python


import socket
#import tqdm
import os
	

def checkStatus(options):
	
	if options[0] == 'NEW':
		createFile(options[1], options[2])
	elif options[0] == 'LIST':
		getFileList()
		


def createFile(filename, filesize):
	
	ACK=('ACK')
	client.send(ACK.encode('ascii'))
	
	filename = os.path.basename(filename)
	filesize = int(filesize)
	#progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
	
	f =  open(os.getcwd() + '/test_db/' + filename, "wb")
	while True:
		bytes_read = client.recv(BUFFER_SIZE)
		if not bytes_read:    
			break
		print('recived bites')
		f.write(bytes_read)
		#progress.update(len(bytes_read))
	
	f.close()
	ACK=('OK')
	client.send(ACK.encode('ascii'))
	client.close()
	server.close()
	
def getFileList():
	
	fileList = os.listdir(os.getcwd() + '/test')
	strList = ','.join([str(e) for e in fileList])

	
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

BUFFER_SIZE = 1024

server.bind(('127.0.0.1', 8050))

#Aceptamos conexiones entrantes con el metodo listen. Por parámetro las conexiones simutáneas.
server.listen(1)

#Instanciamos un objeto cli (socket cliente) para recibir datos
client, addr = server.accept()

while True:

#Recibimos el mensaje, con el metodo recv recibimos datos. Por parametro la cantidad de bytes para recibir
	request = client.recv(BUFFER_SIZE).decode('ascii')
	options =  request.split(',')
	print('received desde IP: '+ str(addr[0]) + ' port: ' + str(addr[1]))
	print(options)
	checkStatus(options)

