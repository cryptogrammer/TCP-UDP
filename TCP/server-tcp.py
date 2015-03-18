## CS 3251 Computer Networks 1
## Programming Assignment 1
## Utkarsh Garg
## 902904045
## utkarsh6@gatech.edu
##
## This is the implementation of the TCP server. It can be run with the
## command: 'python tcp-server.py <PORT>' . It maintains a connection 
## with TCP clients and can handle multiple clients. The server itself 
## does not quit until forced by 'CTRL+C' or an equivalent in the command
## line.
##
import hashlib
import sys
import socket
import string
import random


## Input: None
## Method: The readInput method parses the command line for a specified
## port number. In the absence of one, it reports an error and does not start. 
## return: Port number
def readInput():
	if(len(sys.argv)<2):
		print "ERROR: Port number not defined."
		sys.exit(0)
	# read the port from the command line
	port = sys.argv[1]
	if(len(sys.argv)>2):
		return [int(port), True]
	return int(port)

## Input: String to be hashed
## Method: This method creates a MD5 hash of the provided input. It uses python's
## hashlib library and returns a string using the hexdigest() method.
## return: string of MD5 hash
def hash(input):
	return hashlib.md5(input).hexdigest()

## Input: A string url or dns
## Method: This method handles the conversion of a DNS to an IP
## address using python's socket library's gethostbyname_ex() function.
## This makes sure that a connection can be made whether an IP is provided
## or a DNS is provided.
## return: resolved IP address.
def resolveDNS(dns):
	ip = socket.gethostbyname_ex(dns)
	return ip[2][0]

## Input: None
## Method: This generates a 64 character random string.
## return: 64 character string
def generateRandomString():
	x = ''.join(random.choice(string.ascii_uppercase + string.digits + string.lowercase) for k in range(64))
	return x

## Input: None
## Method: This is the main method that runs when the python script is run.
## It contains a dictionary of usernames associated with their passwords.
## It is responsible for the connection with the client and implements all
## networking functionality through python's socket library. Further documentation
## is provided within the method.
## return: None
def main():
	## username -> password mapping
	authentication = {}
	authentication['user1'] = 'password1'
	authentication['user2'] = 'password2'
	authentication['user3'] = 'password3'
	## get port from command line input
	port = readInput()
	# if(len(port) == 1):
	## 	debugging = False
	## else:
	## 	debugging = True
	## port = port[0]
	## generate a TCP socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#if(debugging):
	#	print("CREATED TCP SOCKET")
	## bind with the povided IP, port
	s.bind(('', port))
	## Start listening on specified port
	s.listen(5)
	#if(debugging):
	#	print("Listening on port " + str(port))
	## Run unless terminated
	while 1:
	   conn, addr = s.accept()
	   #if(debugging):
		#print("Connection Accepted with IP " + addr[0] + " on port " + str(addr[1]))
	   data = conn.recv(1024)
	   if not data: break
	   ## generate random 64 character string
	   challenge = generateRandomString()
	   ## send random string
	   conn.sendall(challenge)
	   #if(debugging):
		#print("CHallenge String Sent")
	   username_hash = conn.recv(1024)
	   #if(debugging):
		#print("Hash Received")
	   ## This is to make sure that no corrupted data was received
	   ## and that the data is in the expected format.
	   try:
		   username = username_hash[:username_hash.index(':')]
		   hashString = username_hash[username_hash.index(':')+1:]
		   ## This is the authentication code.
		   try:
		   		password = authentication[username]
		   		serverHashInput = username+password+challenge
		   		serverHash = hash(serverHashInput)
		   		serverHash = str(serverHash)
		   		## Incorrect username password combination
		   		if(not serverHash == hashString):
		   			conn.sendall("Authentication Failed")
		   			#if(debugging):
					#	print("Authentication failed")
		   		## Success!
		   		else:
		   			conn.sendall("Welcome to our service.")
					#if(debugging):
					#	print("Authentication Successful")
		   ## Unregistered user
		   except KeyError:
		   		conn.sendall("User does not exist")
	   except:
	   		conn.sendall("Parsing Error, Faulty Client.")
	conn.close()


if __name__ == '__main__':
    main()