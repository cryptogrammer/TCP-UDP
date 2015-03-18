# Sample outputs

UDP

SITUATION: NORMAL

Server

Command: python server-udp.py 8889 -d

Output:

CREATED UDP SOCKET
Hello Received
Hello
Challenge String Sent
Hash Received
Authentication successful



Client:

Command: python letmein-udp.py 127.0.0.1:8889 user1 password1 -d

Output:

Socket created
Received Challenge String
Sending Authentication Request to server 127.0.0.1 on port 8889
'Welcome to our service.'


SITUATION: Wrong Password

Server: Still running

Output:

Hello Received
Hello
Challenge String Sent
Hash Received
Authentication failed

Client:

Command: python letmein-udp.py 127.0.0.1:8889 user1 password -d

Output:

Socket created
Received Challenge String
Sending Authentication Request to server 127.0.0.1 on port 8889
'Authentication Failed'


SITUATION: NONEXISTANT USER

Server: Still running

Output:
Hello Received
Hello
Challenge String Sent
Hash Received

Client:

Command: python letmein-udp.py 127.0.0.1:8889 user password -d


Output:

Socket created
Received Challenge String
Sending Authentication Request to server 127.0.0.1 on port 8889
'User does not exist'


SITUATION: PORT NOT SPECIFIED FOR CLIENT

Server:

Command: python server-udp.py 8456 -d

Output:

CREATED UDP SOCKET
Hello Received
Hello
Challenge String Sent
Hash Received
Authentication successful

Client:

Command: python letmein-udp.py 127.0.0.1 user1 password1 -d


Output:

Socket created
Received Challenge String
Sending Authentication Request to server 127.0.0.1 on port 8456
'Welcome to our service.'



TCP

SITUATION: NORMAL

Server

Command: python server-tcp.py 8456 -d

Output:

CREATED TCP SOCKET
Listening on port 8456
Connection Accepted with IP 127.0.0.1 on port 58492
CHallenge String Sent
Hash Received
Authentication Successful




Client:

Command: python letmein-tcp.py 127.0.0.1:8456 user1 password1 -d

Output:

Socket created
Connection Established
Received Challenge String
Sending Authentication Request to server 127.0.0.1 on port 8456
'Welcome to our service.'


SITUATION: Wrong Password

Server: Still running

Output:

Connection Accepted with IP 127.0.0.1 on port 58493
CHallenge String Sent
Hash Received
Authentication failed

Client:

Command: python letmein-tcp.py 127.0.0.1 user1 password -d

Output:

Socket created
Connection Established
Received Challenge String
Sending Authentication Request to server 127.0.0.1 on port 8456
'Authentication Failed'


SITUATION: NONEXISTANT USER

Server: Still running

Output:
Connection Accepted with IP 127.0.0.1 on port 58494
CHallenge String Sent
Hash Received

Client:

Command: python letmein-tcp.py 127.0.0.1 user password -d

Output:

Socket created
Connection Established
Received Challenge String
Sending Authentication Request to server 127.0.0.1 on port 8456
'User does not exist'

SITUATION: PORT NOT SPECIFIED FOR CLIENT

Server

Command: python server-tcp.py 8456 -d

Output:

CREATED TCP SOCKET
Listening on port 8456
Connection Accepted with IP 127.0.0.1 on port 58492
CHallenge String Sent
Hash Received
Authentication Successful


Client:

Command: python letmein-tcp.py 127.0.0.1 user1 password1 -d

Output:

Socket created
Connection Established
Received Challenge String
Sending Authentication Request to server 127.0.0.1 on port 8456
'Welcome to our service.'


