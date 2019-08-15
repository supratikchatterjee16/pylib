# Minimalist Sockets Utility

# Introduction
This is a utility that does not encrypt the data but always confirms the message being sent.
This it does by sending a couple of standard information along with every packet.

TCP sends the information of host address, initiating port, final port, does a crc for confirming the message,
followed by the sequence number, acknowledgement number, and some more subjective information, in it's packet.
It secures the packets being sent at the transport level.

We require a service at the application level that requires very less information to operate.

HTTP would have been a good alternative, but it is an overly humongous protocol for something simple to just work.

There are some inherent problems in multiple places when layering an application for easier use, in python.

So, I decided, I'll just simply create a small little protocol for handling the data using very minimal framework over TCP/IP Sockets.

So what are essentials in information sharing?

1. Reliability
2. Identifying that the entire information provided is correct.
3. Doing all the required operations at as much speed as possible

So how do I plan on doing it?

We have multiple options of doing it. 
I'll make use of the inbuilt libraries to build it.
Two libraries will be made use of predominantly.
ZLIB and HASHLIB.

Zlib will encrypt each transfer locally.
Hashlib will encrypt the entire message in it's entirety.

CRC32 is provided by Zlib
SHA256 is provided by Hashlib

This would essentially become the following:

1st Message:

Total Size \r\n
SHA256SUM \r\n
CRC32SUM \r\n
Body

Any further message:

CRC32SUM\r\n
Body

This is easy to implement as the total size will be in characters(UTF-8 coded numbers).
SHA256 is 256 bits long, or, is 256/8 = 32 bytes.
CRC32 is 32 bits, or, is 32/8 = 4 bytes

Total header size on an average would be:
Fixed : 2(Atleast for UTF-8 coded size value) + 2(\r\n) + 32(SHA256) + 2(\r\n) + 4(CRC32) + 2(\r\n)
Variable : 4 bytes more would be required.

Total header size : 44 + 4

So let's make it this way to make it faster.

Reserve a 50 bytes as a standard for headers, for the first messages. Size is limited to 8 bytes = 64 bits. 
i.e. value < 18446744073709551615 bytes. More than sufficient for extremely large data loads.
Reserve 6 bytes as a standard for headers for the subsequent messages.(CRC32 followed by 13 10)

The user will be able to add a cryptological function in between, but it is at the cost of their own processing overheads, and outside the scope of this library.

Reason for CRC32 : It allows early detection and recovery of modified packets.

What it provides?

1. Easy deploying of server and sockets for the library
2. Provides utilities for parsing JSON, 

## Algorithm
So main algorithm stands as follows.

### Server Side

1. Create a socket, bind it to a port, setting a timeout of 2 seconds(by default, changeable by the user).
2. Start listening for an incoming request, handle about 10 connections at the most at any given time(can be modified by user)
3. The first message is given an acceptable margin of 2048 bytes.
4. It accepts all of 1kB, or whatever portion of it is necessary to be accepted
5. Cut off first 50 bytes, extract CRC32, SHA256 and the file size
6. If size > 4294967295, the value size is set to 0 0 0 0
7. If size cannot be determined, the protocol, listens till a max re-read limit, which by default is 10, before closing
8. The message size of re-reads are adjustable as well. By default, it will be 2048 bytes.
9. The message size of re-reads will be transmitted back along with an ACK
10. ACK will be numbered with a size if the server is waiting for more reads.
11. In case of a CRC32/ SHA256 mismatch, a NACK1 or a NACK2 message is sent.

### Client Side

1. Initiate a connection with the remote server
2. First packet size is of 2048 Bytes, so the data to be sent is 1998 bytes(2048 - 50).
3. The socket waits and listens for an ACK, and checks if there is a size associated
4. The subsequent messages, if any, are sent using the packet sizes mentioned by the ACK
5. In case of a NACK1, the last allocated ACK size will be made use of, to transmit the last packet.
6. In case of NACK2, the entire process is reiterated from the Step 2 onwards.
7. When an ACK with no size is recieved, the transfer is assumed as complete.
8. This will be followed by an ACK, JSON or filename/file_path(size 2038 bytes)
9. The next ACK is acknowledged as a shut off signal.

## Using

The following examples should give the entirety of flow that can be used.
Server side sample : 
```python3
import sys
sys.path.insert("/path/to/your/lib")
from minimalsockets import ServerSocket
port_number = 8000 #Or some arbitary port number
server = ServerSocket(address_tuple)
server.logging = True #By default it is False
server.listen() # This is a blocking method returns message after every succesful transaction
server.threaded_listen(some_function) #Handle object/function for the threaded server
#The handle is executed after every succesful transfer and recieves the request as bytes.
#The entry point for an object being passed, is, your_class.entry(text)
#Let the server instance take care of all your problems, like a load and fire gun...
```
Client side sample : 
```python3
import sys
sys.path.insert("/path/to/your/lib")
from minimalsockets import Socket
socket = Socket()
#socket.encryption_logic = some_function #Do not add () as that will make it execute. This is completely optional
socket.send("Some message")
socket.send_json(some_json)
socket.send_file(filepath)
#An endless barrage of sends
socket.dispose()
```
