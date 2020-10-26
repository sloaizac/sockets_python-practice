#!/usr/bin/env python


import socket
import os
import constants
import shutil
import sys

def init():
	while True:
		request = client.recv(constants.BUFFER_SIZE).decode('ascii')
		options = request.split(',')
		print('received from IP: ' + str(addr[0]) + ' port: ' + str(addr[1]))
		checkStatus(options)
	

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
	if os.path.exists(os.path.join(test_db, bucketName, filename)):
		client.send('EXIST'.encode('ascii'))
	else:
		client.send('ACK'.encode('ascii'))
		f = open(os.path.join(test_db, bucketName, filename), "wb")
		while True:
			bytes_read = client.recv(constants.BUFFER_SIZE)
			if bytes_read.decode('ascii') == 'EOF':
				break
			print('received bites')
			f.write(bytes_read)
		f.close()
		print('received-completed')
		client.send('OK'.encode('ascii'))
	
def getFileList(bucketName):
	fileList = os.listdir(os.path.join(test_db, bucketName))
	strList = '\n'.join([str(e) for e in fileList])
	client.send(strList.encode('ascii'))

def getBucketList():
	fileList = os.listdir(test_db)
	strList = '\n'.join([str(e) for e in fileList])
	client.send(strList.encode('ascii'))

def createBucket(bucketName):
	newBucket = os.path.join(test_db, bucketName)
	if not os.path.exists(newBucket):
		os.makedirs(newBucket)
		client.send('new bucket created'.encode('ascii'))
	else:
		client.send('Bucket name already exist'.encode('ascii'))

	
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


server.bind((constants.SERVER_ADDRESS, constants.PORT))

server.listen(10)

try:
	test_db = sys.argv[1]
except:
	test_db = input("Enter buckets path >> ")

if not os.path.exists(test_db):
	os.makedirs(test_db)

client, addr = server.accept()

init()

