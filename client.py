#Client code

#Import socket library
import socket
import os
import constants

#Variables for connection
host = constants.SERVER_ADDRESS 
port = constants.PORT

def runClientSocket():
    #Create client socket
    clientSocket= socket.socket()

    #Connection with server. first parameter = IP address, second parameter = Connection Port
    clientSocket.connect((host, port))
    print("Connected to server")


    #Maintain connection with the server
    while True:
        #Client command 
        command = input("Enter the command you want to send >> ")
        informationToSend = ""
        if(command == constants.HELLO or command == constants.LIST_BUCKET):
            informationToSend = command
        elif(command == constants.NEW_BUCKET):
            bucketName = input("Enter the name of the new bucket >> ")
            informationToSend = command+","+bucketName
        elif(command == constants.DELETE_BUCKET):
            bucketName = input("Enter the name of the bucket to delete >> ")
            informationToSend = command+","+bucketName
        elif(command == constants.UPLOAD_FILE):
            filePath = input("Enter the path where the file is >> ")
            fileName = input("Enter the name of the file to upload >> ")
            bucketName = input("Enter the name of the bucket where the file will be uploaded >> ")
            informationToSend = command+","+filePath+","+fileName+","+bucketName
        elif(command == constants.LIST_FILE):
            bucketName = input("Enter the bucket name to list the files >> ")
            informationToSend = command+","+bucketName
        elif(command == constants.DOWNLOAD_FILE):
            fileName = input("Enter the name of the file to download >> ")
            bucketName = input("Enter the bucket name to download the file >> ")
            informationToSend = command+","+fileName+","+bucketName
        elif(command == constants.DELETE_FILE):
            fileName = input("Enter the name of the file to delete >> ")
            bucketName = input("Enter the bucket name to delete the file >> ")
            informationToSend = command+","+fileName+","+bucketName
        elif(command == constants.EXIT):
            break
        else:
            print("Non-existent command, try again")
        #Send message
        clientSocket.send(bytes(informationToSend, constants.ENCODING_FORMAT))
        #Server response
        response = clientSocket.recv(constants.BUFFER_SIZE)
        print(response.decode())
    #Close connection to the server
    clientSocket.close()
    print("Connection closed")

#Iniatialize client socket
runClientSocket()
