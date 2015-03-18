## CS 3251 Computer Networks 1
## Programming Assignment 1
## Utkarsh Garg
## 902904045
## utkarsh6@gatech.edu
##
## This is the implementation of the UDP server. It can be run with the
## command: 'python udp-server.py <PORT>' . It runs and accepts data from 
## UDP clients and can handle multiple clients.The server itself 
## does not quit until forced by 'CTRL+C' or an equivalent in the command
## line.
##

import hashlib
import sys
import socket
import string
import random


### Input: None
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
	if(len(port) == 1):
		debugging = False
	else:
		debugging = True
	port = port[0]
	## set socket timeout
	socket.setdefaulttimeout(0.2)
	## create a UDP socket
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	if(debugging):
		print("CREATED UDP SOCKET")
	## set default IP as localhost.
	ip = '127.0.0.1'
	## bind with the povided IP, port
	s.bind((ip, port))
	## Run unless terminated
	while 1:
	   ## The following while loop is to compensate for packet loss
	   ## in the UDP protocol. This ensures that if the same packet
	   ## arrives again, it is not read by a subsequent function which
	   ## is expecting some other information.
	   received = False
	   while(not received):
	   	   data = ''
		   try:
		   		data, addr = s.recvfrom(1024)
		   		print "Hello Received"
		   		received = True
		   ## to handle a timeout and search for data again.
		   except socket.timeout:
		   		received = False
	   print data
	   if not data: break
	   ## generate the 64 character random string to send to client
	   challenge = generateRandomString()
	   ## send string to client
	   s.sendto(challenge, addr)
	   if(debugging):
		print("Challenge String Sent")
	   username_hash, addr = s.recvfrom(1024)
	   if(debugging):
		print("Hash Received")
	   ## This try block handes any faulty/corrupted hash that might have come.
	   try:
	   		## Decoding the hashString to obtain username and the hash.
	   		username = username_hash[:username_hash.index(':')]
	   		hashString = username_hash[username_hash.index(':')+1:]
	   		## This try block runs authentication of the decoded username.
	   		try:
		   		password = authentication[username]
		   		serverHashInput = username+password+challenge
		   		serverHash = hash(serverHashInput)
		   		serverHash = str(serverHash)
		   		## Failed Authentication.
		   		if(not serverHash == hashString):
		   			s.sendto("Authentication Failed",addr)
		   			if(debugging):
						print("Authentication failed")
		   		## Success!
		   		else:
		   			s.sendto("Welcome to our service.",addr)
		   			if(debugging):
						print("Authentication successful")
		   	## handling unregistered user.
		   	except KeyError:
		   		s.sendto("User does not exist",addr)
	   except:
	   		s.sendto("Parsing error, Faulty Client.",addr)


if __name__ == '__main__':
    main()