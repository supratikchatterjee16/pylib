import sys
sys.path.insert(1, "..")
import zipper

import os
import json
import zlib
import socket
import hashlib
import logging
import threading

def _crc_checksout_for(crc, content):
	crc32 = zlib.crc32(content).to_bytes(4, byteorder="little")
	if crc == crc32:
		return True
	return False

def _sha_checksout_for(checksum, content):
	sha256 = hashlib.sha256(content).digest()
	if sha256 == checksum:
		return True
	return False

class Server:
	def __init__(self, address = ('', 8000), address_type = socket.AF_INET, socket_type = socket.SOCK_STREAM, name = ""):
		#It is advised to not change the default configurations if not completely sure
		#Server information
		self.name = name
		self.address = address
		#Socket declarations
		self.socket = socket.socket(address_type, socket_type)
		self.socket.bind(address)
		#Acknowledgement type selection
		self.ACK = 0 #ACK1 : 0, ACK2 : 1, NACK1 : 2, NACK2 : 3
		#History
		self.last_address = None
		self.keeps_content = False
		self.last_content = []
		self.last_response = []
		#Current information. Essential for debugging during runtime
		self.error_low = 0  #Packet  mismatch
		self.error_high = 0 #Content mismatch
		#Logging information
		self.logging_level = 20
		
	
	def send_ACK(self, num):
		message = num.to_bytes(1, "little")
		message += self.buffer_size.to_bytes()
		self.connection.send(message)
		return
	
	def send_NACK(self, num):
		message = (num + 2).to_bytes(1, "little")
		self.connection.send(message)
		return
	
	def listen(self, buffer_size = 2048, repeat_limit = 5, accept_limit = 10, accept_max_size = 2000000):
		#Errors in this are to be handled outside
		self.socket.listen(accept_limit)
		self.buffer_size = buffer_size
		#self.socket.settimeout(timeout)
		logger = logging.getLogger("Server @ {}".format(self.address))
		logger.isEnabledFor(self.logging_level)
		logger.info(" Server {}\nListening at : {}".format(self.name, self.address))
		
		self.connection , current_address = self.socket.accept()
		logger.info("Accepted connection from {}".format(current_address))
		accepting = True
		
		#Local vars
		content = []
		return_content = []
		content_size = 0
		read = 0
		#Protocol logic
		iteration = 0
		iteration1 = 0
		iteration2 = 0
		level = 1
		while accepting:
			buff = self.connection.recv(buffer_size)
			
			#Formatting the accepted bytes
			if iteration == 0:
				header = buff[:50]
				body = buff[50:]
				
				content_size = header[:8]
				sha256sum = header[10:42]
				crc32sum = header[44:48]
			else:
				crc32sum = buff[0:4]
				body = buff[6:]
			iteration += 1
			#Protocol flow
			if _crc_checksout_for(crc32sum, body):
				if level == 1:
					content.extend(body)
					if content_size <= 0:
						if iteration < repeat_limit:
							iteration += 1
							self.send_ACK(0)
						else:
							self.send_ACK(1)
							level = 2
					else:
						read += len(body)
						if read < content_size:
							self.send_ACK(0, connection)
							iteration1 = 0
						else:
							if _sha_checksout_for(sha256sum, content):
								self.send_ACK(1, connection)
								level = 2
							else:
								logger.error("Content mismatch")
								self.send_NACK(1, connection)
								iteration2 += 1
								if iteration2 > repeat_limit:
									logger.warning("Socket being forcefully closed")
									self.connection.close()
									accepting = False
				elif level == 2:
					content_type = int.to_bytes(body[0])
					if content_type == 0:
						return_content = content
					elif content_type == 1:
						return_content = json.loads(content)
					elif content_type == 2:
						filename = str.decode(body[1:])
						local_file = open(filename,"w+")
						f.write(content)
						f.close()
						return_content = filename
					self.send_ACK(0)
					accepting = False
			else :
				logger.error("Packet Mismatch")
				self.send_NACK(0)
				iteration1 += 1
				if iteration1 >= repeat_limit:
					logger.warning("Socket being forcefully closed")
					self.connection.close()
					accepting = False
		#Creating history
		self.last_address = current_address
		
		if self.keeps_content:
			self.last_content = content
		
		return return_content
	
	def listen_threaded(self):
		return
	
class Client:
	def __init__(self, address_type = socket.AF_INET, socket_type = socket.SOCK_STREAM, name = ""):
		self.socket = socket.socket(address_type, socket_type)
		self.name = name
	
	def send(self, address, content, content_size, type = '',timeout = 10):
		self.socket.connect(address)
		sending = True
		if type == '':
			if os.path.exists(content):
				if os.path.isfile(content):
					type = content
				elif os.path.isdir(content):
					type = zipper(content)
			
		while sending:
			
	

if __name__ == "__main__":
	server = Server(('', 9000))
	server_return  = server.listen()
