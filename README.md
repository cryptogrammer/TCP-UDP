Files:

	README.txt: Contains description of protocols and instructions on running the code.

	Folder TCP: contains the TCP implementations
	TCP/letmein-tcp.py: Contains the client side implementation of the TCP protocol.
	TCP/server-tcp.py: Contains the server side implementation of the TCP protocol.

	Folder UDP: Contains the UDP implementation files.
	UDP/letmein-udp.py: Contains the client side implementation of the UDP protocol.
	TCP/server-tcp.py: Contains the server side implementation of the UDP protocol.

	Sample.txt: Contains command line code and subsequent output for both client and server for UDP and TCP.

Instructions for compiling and running code:

For both protocols, 3 users have been stored

Username: Password
user1: password1
user2: password2
user3: password3



	TCP

	letmein-tcp.py is the client side implementation of the TCP protocol. It can be run from the command line using the following command:
		python letmein-tcp.py <IP/DNS>:<PORT NUMBER OPTIONAL> <USERNAME> <PASSWORD> <OPTIONAL -d FLAG>
		An example would be: 'python letmein-tcp.py 127.0.0.1:8889 user1 password1 -d' for running the client on localhost port 8889.
		The command can also be missing a port number and can have a DNS instead of an IP. The -d flag i.e. the debug flag will print out in the terminal, what is happening with the code at the current moment.

	server-tcp.py is the server side implementation of the TCP protocol. It can be run from the command line with the following command:
		python server-tcp.py <PORT NUMBER>
		OR
		python server-tcp.py <PORT NUMBER> <OPTIONAL -d FLAG>
		As before, the -d flag prints out messages indicating what is happening when.


	UDP

	letmein-udp.py is the client side implementation of the UDP protocol. It can be run from the command line using the following command:
		python letmein-udp.py <IP/DNS>:<PORT NUMBER OPTIONAL> <USERNAME> <PASSWORD> <OPTIONAL -d FLAG>
		An example would be: 'python letmein-udp.py 127.0.0.1:8889 user1 password1 -d' for running the client on localhost port 8889.
		The command can also be missing a port number and can have a DNS instead of an IP. The -d flag i.e. the debug flag will print out in the terminal, what is happening with the code at the current moment.

	server-udp.py is the server side implementation of the UDP protocol. It can be run from the command line with the following command:
		python server-udp.py <PORT NUMBER>
		OR
		python server-udp.py <PORT NUMBER> <OPTIONAL -d FLAG>
		As before, the -d flag prints out messages indicating what is happening when.


NOTE: IF PORT NUMBER IS NOT SPECIFIED ON THE CLIENT SIDE, THE SERVER SIDE NEEDS TO BE RUN WITH THE DEFAULT PORT NUMBER 

All code was written and run on a Mac OSX and that is my preffered testing platform.

DESCRIPTION OF PROTOCOLS:

TCP:

Server is initialized on a certain port on a certain host.
Server creates a TCP socket, binds to the port and starts listening for incoming data (As a data stream).
Client is initialized on any server/local machine with the same port as the server side program, with a username and password as input.
Client creates a TCP socket and sends a connection request to the server.(As a data stream)
Server resceives the connection request and generates a random 64 character string.
Server sends this randomly generated string to client.
The client concatenates the string with the username and passsword and creates a MD5 hash.
It then concatenates the username on this hash and sends it to the server.
The server, using the username, tries to retrieve a stored password.
If the user does not exist, it returns a message saying 'User does not exist.
Otherwise, it uses the password and creates the same hash.
If the hash matches, the user is authenticated, otherwise, the user is denied access.
The appropriate message is sent back to the user and the the client connection is terminated while the server program keeps on running.


UDP:

Server is initialized on a certain port on a certain host.
Server creates a UDP socket, and binds to the port(As a datagram socket).
Client is initialized on any server/local machine with the same port as the server side program, with a username and password as input.
Client creates a UDP socket and sends a connection request to the server.(As a datagram, in the form a message, which the server responds to in the next step.)
Server resceives the connection request and generates a random 64 character string.
Server sends this randomly generated string to client.
The client concatenates the string with the username and passsword and creates a MD5 hash.
It then concatenates the username on this hash and sends it to the server.
The server, using the username, tries to retrieve a stored password.
If the user does not exist, it returns a message saying 'User does not exist.
Otherwise, it uses the password and creates the same hash.
If the hash matches, the user is authenticated, otherwise, the user is denied access.
The appropriate message is sent back to the user; the server program keeps on running.
During the protocol, the client sends data requests upto 5 times after a socket timeout of 0.2s. If after 5 times no data is receved, the client program is terminated.
