## CS 3251 Computer Networks 1
## Programming Assignment 1
## Utkarsh Garg
## 902904045
## utkarsh6@gatech.edu
##
## This is the implementation of the UDP client. It can be run with the
## command: 'python letmein-udp.py <HOST IP OR DNS>:<PORT> <Username> <Password>' . It will work
## both with DNS and IP address and with or witout a specified port. 
## The program sends the UDP server a test message 'hello World' to recieve back
## a randomly generated string. It then creates a MD5 hash with the username password and the
## string and sends it to the server which then runs an authentication and replies with an
## message.
##
import hashlib
import sys
import socket
import re

## Input: A string url or dns
## Method: This method handles the conversion of a DNS to an IP
## address using python's socket library's gethostbyname_ex() function.
## This makes sure that a connection can be made whether an IP is provided
## or a DNS is provided.
## return: resolved IP address.
def resolveDNS(dns):
	try:
		ip = socket.gethostbyname_ex(dns)
		return ip[2][0]
	## Handles the error where the provided input is not a valid DNS
	except socket.gaierror:
		print "DNS cannot be resolved"
		sys.exit(0)

## Input: None
## Method: The readInput method parses the command line for specified IP/DNS
## port number, username and password.It will work both with DNS and IP address
## and with or witout a specified port. It has several checks to ensure the integrity
## of the information provided, further documented in the method. 
## return: [IP, Port, Username, Password]
def readInput():
	## When insufficient argumanes are provided
	if(len(sys.argv)<4):
		print "Incomplete command line input. Try again."
		sys.exit(0)
	ipHost = sys.argv[1]
	## Determines whether provided host is an IP or a DNS
	try:
		x = int(ipHost[0:2])
		## Determines whether or not a port has been specified
		try:
			x = ipHost.index(':')
			ip = ipHost[:ipHost.index(':')]
			## Checks whether the provided IP is valid or not.
			p = re.compile('^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
			if(not p.match(ip)):
				print("Incorrect IP address. Please check input.")
				sys.exit(0)
			## Checks the Validity of the port
			p = re.compile('^[0-9]{2,4}$')
			port = ipHost[ipHost.index(':')+1:]
			if(not p.match(port)):
				print("Invalid Port. Please check input.")
				sys.exit(0)
		except ValueError:
			ip = ipHost
			p = re.compile('^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
			if(not p.match(ip)):
				print("Incorrect IP address. Please check input.")
				sys.exit(0)
			## specified a default port.
			port = 8456
	## When a DNS is provided instead.
	except ValueError:
		try:
			x = ipHost.index(':')
			ip = resolveDNS(ipHost[:ipHost.index(':')])
			port = ipHost[ipHost.index(':')+1:]
			p = re.compile('^[0-9]{2,4}$')
			if(not p.match(port)):
				print("Invalid Port. Please check input.")
				sys.exit(0)
		except ValueError:
			ip = resolveDNS(ipHost)
			port = 8456

	username = sys.argv[2]
	password = sys.argv[3]
	if(len(sys.argv) == 4):
		return [ip, port, username, password]
	elif(len(sys.argv) == 5):
		if(sys.argv[4] == '-d'):
			return [ip, port, username, password, True]
		else:
			return [ip, port, username, password]


## Input: None
## Method: This is the main method that runs when the python script is run.
## It is responsible for establishing a connection with the server and also
## for all data exchange between the client and the server. It generates a hash
## and sends it to the server for authentication. Further documentation is
## provided in the method.
## return: None
def main():
	input = readInput()
	debuggingEnabled = False
	ip = input[0]
	port = input[1]
	username = input[2]
	password = input[3]
	## Checks for debugging flag
	if(len(input)==5):
		debuggingEnabled = True
	## Creates a TCP socket with data streaming
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	if(debuggingEnabled):
		print("Socket created")
	port = int(port)
	## Connects to the server
	try:
		s.connect((ip, port))
	except:
		print "Incorrect port specified"
		sys.exit(0)
	if(debuggingEnabled):
		print("Connection Established")
	## Sends an initial message to receive a random string
	s.sendall('Hello')
	challenge = s.recv(1024)
	if(debuggingEnabled):
		print("Received Challenge String")
	hashinput = username+password+challenge
	temp = hash(hashinput)
	data = str(temp)
	data = username + ":" + data
	## Sends hashed data to server for user authentication.
	s.sendall(data)
	if(debuggingEnabled):
		print("Sending Authentication Request to server " + str(ip) + " on port " + str(port))
	## Resulting access grantied/denied/error reported.
	result = s.recv(1024)
	s.close()
	print repr(result)

## Input: String to be hashed
## Method: This method creates a MD5 hash of the provided input. It uses python's
## hashlib library and returns a string using the hexdigest() method.
## return: string of MD5 hash
def hash(input):
	return hashlib.md5(input).hexdigest()



## Input: IP Address, Port Number
## Method: Creates a socket connection to initialize TCP Communication
## Return: connection
def connect(ip, port):
	a = None
	try:
		a = socket.create_connection((ip, port))
	except:
		print("Could not connect to provided host. Please check the input")
	if(a != None):
		return a
	return "ERROR"




if __name__ == '__main__':
    main()
