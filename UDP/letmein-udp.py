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
## It is responsible for all data exchange between the client and the server.
## It generates a hash and sends it to the server for authentication. Further
## documentation is provided in the method.
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
	port = int(port)
	## sets timeout value for port
	socket.setdefaulttimeout(0.2)
	## Initializes a UDP socket
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	if(debuggingEnabled):
		print("Socket created")
	## To detect packet loss
	delivered = False
	## Max transmissions in case of poor connection/ packet loss
	UDPNUMATTEMPTSLIMIT = 5 # max number of tries for timeout
	count = 0
	## Iteration in case of packet loss
	while(not delivered  and count < UDPNUMATTEMPTSLIMIT):
		try:
			s.sendto('Hello',(ip, port))
			challenge, addr = s.recvfrom(1024)
			## Check whether a response was received.
			if(not challenge == None):
				delivered = True
			else:
				delivered = False
		except socket.timeout:
			count = count+1
			delivered = False
	## If total iterations reached => No data received => terminate.
	if(count == 5):
	   	sys.exit(0)
	if(debuggingEnabled):
		print("Received Challenge String")
	count = 0
	delivered = False
	hashinput = username+password+challenge
	temp = hash(hashinput)
	data = str(temp)
	data = username + ":" + data
	while(not delivered  and count < UDPNUMATTEMPTSLIMIT):
		try:
			s.sendto(data,addr)
			if(debuggingEnabled):
				print("Sending Authentication Request to server " + str(ip) + " on port " + str(port))
			result, addr = s.recvfrom(1024)
			if(not result == None):
				delivered = True
			else:
				delivered = False
		except socket.timeout:
			count = count + 1
			delivered = False
	if(count == 5):
		sys.exit(0)
	s.close()
	print repr(result)

## Input: String to be hashed
## Method: This method creates a MD5 hash of the provided input. It uses python's
## hashlib library and returns a string using the hexdigest() method.
## return: string of MD5 hash
def hash(input):
	return hashlib.md5(input).hexdigest()

if __name__ == '__main__':
    main()
