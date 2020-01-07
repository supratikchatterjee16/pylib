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

## Algorithm

Client Socket:

1. Initiates connection with given address
2. Calculate size(int Bytes) of message and sha256 checksum for the content
3.	Attach size after the 4 byte crc32 code, as a 24 byte size header.
	The first message is always 2048 bytes long if not specified otherwise by the user(yes you can change it)
	There are 20 reserved bytes for the transfer.
	Following this, the next messages, do not contain anything, but a 4 byte long crc32 code, as a header.
	Failing to read a content size results in a critical failure.
	Just as a note, longest value that can be held by 20 bytes(or 160 bits) is : 1461501637330902918203684832716283019655932542975
	i.e. No one should have any problem, as an more than that can be broken and transferred, using the functions provided.
3. The steps repeat till completion of the entire message, break only if no size is recieved with ACK
4. Repeat every token that has had an NAK
5. After transfer of the entire message, the sha256sum is sent alongwith a crc32 code.

Server socket:

1. Bind a socket
2. Start listening at it
3. Accept a connection
4. Verify crc32sum
5. Get size of content
6. Decide iterations for the content(future provisions for making this component a bit 'smarter')
7.	Read for the number of iterations, sending an ACK<accepting byte size> for every succesful recieves
	For each unsuccesful recieve, an NAK is sent.
	The ACK and NAK are 1 and 0 respectively. There are other codes as well. They belong to a different class
8. After reading the number of required iterations, verify with the sha256sum
9. Send Final ACK if it checks out (3) and NAK if it is in error(2)
10. Finally format it to the required format, and return control to a controlling element.