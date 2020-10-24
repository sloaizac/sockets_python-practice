#!/usr/bin/env python

import socket

host = '127.0.0.1'
port = 8050

socket = socket.socket()

socket.connect((host, port))
print('Conecting...')

while True:
#Instanciamos una entrada de datos para que el cliente pueda enviar mensajes
	msg = 'NEW,hola.txt,100'
#Con el método send, enviamos el mensaje
	socket.send(msg.encode('ascii'))
#obj.send(mens)
	response = socket.recv(1024)
	print(response)
	if response.decode('ascii') == 'ACK':
		f = open('hola.txt', "rb")
		while True:
			bytes_read = f.read(1024)
			if not bytes_read:
				break
			print('send')
			socket.sendall(bytes_read)
		while True:
			response = socket.recv(1024)
			if response.decode('ascii') == 'OK':
				socket.close()
				print('closed')
				break
	
#Cerramos la instancia del objeto servidor

#Imprimimos la palabra Adios para cuando se cierre la conexion
