#!/usr/bin/env python


import socket
import os
import constants
import shutil
	

def checkStatus(options):
	if options[0] == constants.NEW_BUCKET:
		createBucket(options[1])
	elif options[0] == constants.UPLOAD_FILE:
		createFile(options[1], options[2])
	elif options[0] == constants.LIST_FILE:
		getFileList(options[1])
	elif options[0] == constants.DELETE_FILE:
		deleteFile(options[1], options[2])
	elif options[0] == constants.DOWNLOAD_FILE:
		downloadFile(options[1], options[2])
	elif options[0] == constants.DELETE_BUCKET:
		deleteBucket(options[1])
	elif options[0] == constants.LIST_BUCKET or options[0] == constants.HELLO:
		getBucketList()

def downloadFile(filename, bucketName):
	f = open(os.path.join(test_db, bucketName, filename), "rb")
	while True:
		bytes_read = f.read(constants.BUFFER_SIZE)

		if not bytes_read:
			print('vacio')
			break
		print('send')
		client.sendall(bytes_read)
	client.send('EOF'.encode('ascii'))
	while True:
		response = client.recv(constants.BUFFER_SIZE)
		if response.decode('ascii') == 'OK':
			break

def deleteFile(filename, bucketName):
	os.remove(os.path.join(test_db, bucketName, filename))
	client.send('file deleted successfully'.encode('ascii'))

def deleteBucket(bucketName):
	shutil.rmtree(os.path.join(test_db, bucketName))
	client.send('bucket deleted successfully'.encode('ascii'))

def createFile(filename, bucketName):
	client.send('ACK'.encode('ascii'))
	f = open(os.path.join(test_db, bucketName, filename), "wb")
	while True:
		bytes_read = client.recv(constants.BUFFER_SIZE)
		if bytes_read.decode('ascii') == 'EOF':
			print('vacio')
			break
		print('recived bites')
		f.write(bytes_read)
	f.close()
	print('recived-completed')
	client.send('OK'.encode('ascii'))
	
def getFileList(bucketName):
	fileList = os.listdir(os.path.join(test_db, bucketName))
	strList = '\n * '.join([str(e) for e in fileList])
	client.send(strList.encode('ascii'))

def getBucketList():
	fileList = os.listdir(test_db)
	strList = '\n * '.join([str(e) for e in fileList])
	client.send(strList.encode('ascii'))

def createBucket(bucketName):
	newBucket = os.path.join(test_db, bucketName)
	if not os.path.exists(newBucket):
		os.makedirs(newBucket)
		client.send('new bucket created'.encode('ascii'))
	else:
		client.send('bucket name already exist'.encode('ascii'))

	
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


server.bind((constants.SERVER_ADDRESS, constants.PORT))

server.listen(1)

client, addr = server.accept()

test_db = os.path.join(os.getcwd(), 'test_db')
if not os.path.exists(test_db):
	os.makedirs(test_db)

while True:
	request = client.recv(constants.BUFFER_SIZE).decode('ascii')
	options = request.split(',')
	print('received from IP: ' + str(addr[0]) + ' port: ' + str(addr[1]))
	print("OPTIONS_LOG: " + str(options))
	checkStatus(options)

