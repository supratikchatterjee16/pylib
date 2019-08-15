import zlib
import hashlib
import sys
import socket
string = (1048).to_bytes(4, "little")
content = (0).to_bytes(1, "little")
#content.extend(string)
content += string
string = content
#print(int.from_bytes(string[1:], "little"))
#print(int.from_bytes(string, byteorder="little") == 0)
crc32 = zlib.crc32(string)
crc32 = crc32.to_bytes(4, byteorder="little")
#print(crc32)
#print(len(crc32))

sha256_generator = hashlib.sha256()

sha256_generator.update(string)
sha256_bytes = sha256_generator.digest()
#print(sha256_bytes)
#print(len(sha256_bytes))

#i = 0
#n = 1
#while n<64:
	#i <<= 1
	#i += 1
	#print("{}\t{}".format(n,i))
	#n += 1
	

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect(('', 9000))
socket.settimeout(10)
for i in range(10):
	socket.send(b'Hello world')
	message = socket.recv(2048)
	print(message)
socket.close()