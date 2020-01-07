hello = 99090
hello = hello.to_bytes(20,"little")
hello = b'\1\0'+hello
print(hello)
#import zlib
#import hashlib
#import sys
#import socket
#string = (1048).to_bytes(4, "little")
#content = (0).to_bytes(1, "little")
#content.extend(string)
#content += string
#string = content
#print(int.from_bytes(string[1:], "little"))
#print(int.from_bytes(string, byteorder="little") == 0)
#crc32 = zlib.crc32(string)
#crc32 = crc32.to_bytes(4, byteorder="little")
#print(crc32)
#print(len(crc32))

#sha256_generator = hashlib.sha256()

#sha256_generator.update(string)
#sha256_bytes = sha256_generator.digest()
#print(sha256_bytes)
#print(len(sha256_bytes))

#i = 0
#n = 1
#nob = 10
#byte_size = 8
#while n <= nob * byte_size:
	#i <<= 1
	#i += 1
	#print("{}\t{}".format(n,i))
	#n += 1
#for multiple in (0, 1000000000000, 1000):
	#print("{}\t{}".format(multiple, i))
	#i /= 1000

#socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#socket.connect(('', 9000))
#socket.settimeout(10)
#for i in range(10):
	#socket.send(b'Hello world')
	#message = socket.recv(2048)
	#print(message)
#socket.close()
#import os
#import math
#print(os.stat('./README.md').st_size)
#print(os.stat('./README.md').st_size / 8)
#print(math.ceil(os.stat('./README.md').st_size/8))

#import os
#import sys
#import time
#import socket
#import threading
#a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#b = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#a.bind(('', 8080))
#def x():
	#a.listen(10)
	#conn, addr = a.accept()
	#message = conn.recv(2048)
	#print("Recieved : {}".format(len(message)))
	##print(message)
	#conn.close()
#thread1 = threading.Thread(target = x)
#thread1.start()
#time.sleep(1)
#b.connect(('', 8080))
#message = bytearray(os.urandom(10000000))
#print("Sending : {}".format(len(message)))
##print("Message : {}".format(message))
#b.send(message)
#b.close()
#thread1.join()
