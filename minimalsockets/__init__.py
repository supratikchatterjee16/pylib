import sys
sys.path.insert(1, "..")
import zipper

import os
import json
import zlib
import socket
import hashlib
import logging
from multiprocessing import Pool, Process

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
		
		#Object declarations
		#Server information
		self.name = name
		self.address = address
		#Socket information
		self.socket = socket.socket(address_type, socket_type)
		self.socket.bind(address)
		
		#History
		self.enable_history = False #Enable storing IPs, content, responses, as per policy
		self.history_policy = {"ip" : False, "content" : False, "response" : False, "function" : None, "file" : open("history_log.txt", "a+") }
		
		#Security
		self.enable_security #Enable security logging. Stores number of hops, losses and time, for each accept.
		self.security_policy = {"ip" : True, "hop" : True, "packet loss" : True, "content loss" : True, "function" : None, "file" : open("security_log.txt", "a+")}
		
		#Current information. Essential for debugging during runtime
		self.enable_logging = False
		self.logger_policy = {"logging_level" : logging.ERROR, "format" = '%(name)s %(threadName)s %(asctime)s %(message)s', "file" : open("error_log.txt","a+")}
		self.set_logger()
	
	def set_logger_enabled(self, flag = True):
		self.enable_logger = flag
		self.set_logger_policy()
		return
	
	def set_logger_policy(self, logging_policy = {}):
		for i in logging_policy.keys():
			if i in self.logger_policy:
				self.logger_policy[i] = logging_policy[i]
		
		self.error = logging.Logger(self.name+" error")
		self.error.setLevel(self.logger_policy["logging_level"])
		handler = logging.StreamHandler(self.logger_policy["file"])
		handler.setFormatter(logging.Formatter(self.logger_policy["format"]))
		self.error.addHandler(handler)
		return
	
	def set_history_enabled(self, flag = True):
		self.enable_history = flag
		self.set_history_policy()
		return
	
	def set_history_policy(self, history_policy = {}):
		for i in history_policy.keys():
			if i in self.history_policy:
				self.history_policy[i] = history_policy[i]
		
		self.history = logging.Logger()
		self.history.setLevel(logging.INFO)
		handler = logging.StreamHandler(self.history_policy["file"])
		handler.setFormatter(logging.Formatter(self.history_policy["format"]))
		self.logger.addHandler(handler)
		return
	
	def set_security_enabled(self, flag = True):
		self.enable_security = flag
		self.set_security_policy()
		return
	
	def set_security_policy(self, security_policy = {}):
		for i in security_policy.keys():
			if i in self.security_policy:
				self.security_policy[i] = security_policy[i]
		
		self.security = logging.Logger()
		self.security.setLevel(logging.INFO)
		handler = logging.StreamHandler(self.security_policy["file"])
		handler.setFormatter(logging.Formatter(self.security_policy["format"]))
		self.logger.addHandler(handler)
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
		content_size = 0
		pos = 0
		read = 0
		#Protocol logic
		iteration = 0
		required_iterations = 0
		while accepting:
			buff = self.connection.recv(buffer_size)
			#Formatting the accepted bytes
			crc = buff[:5]
			buff = buff[5:]
			if _crc_checksout_for(crc, buff):
				if iteration == 0:
					content_size = int.from_bytes(buff[:21], "little")
					buff = buff[21:]
					required_iterations = (content_size / (buffer_size - 4)) - 20
					#while required_iterations > 100 and buffer_size < 100000:#Open this when required
						#buffer_size += 1024
						#required_iterations = (content_size / (buffer_size - 4)) - 20
				if content_size == 0:
					self.connection.send(b'\0\1')
					self.connection.close()
					self.check(0, "No content size")
					return None
				message = b'\1\0'+buffer_size.to_bytes(10, "little")
				self.connection.send(message)
				content.append(buff)
			else:
				self.check(0, "")
				self.connection.send(b'\0\0')#Signal that a less severe NAK has occured
			#Protocol flow
			iteration += 1
			if iteration >= required_iterations:
				accepting = False
		
		#Finish up sequence
		buff = self.connection.recv(buffer_size)
		crc = buff[:5]
		buff = buff[5:]
		if not _crc_checksout_for(buff):
			self.check(0, "Last check failure")
			self.connection()
		
		return return_content
	
	def listen_threaded(self):
		return
	
class Client:
	def __init__(self, address_type = socket.AF_INET, socket_type = socket.SOCK_STREAM, name = ""):
		self.socket = socket.socket(address_type, socket_type)
		self.name = name
		self.logger = logging.Logger(name = "Client "+name)
	
	def set_logger(self, logging_level = logging.ERROR, format = '%(name)s %(threadName)s %(asctime)s %(message)s', logfile = sys.stdout):
		logger = logging.Logger(name = "Zipper")
		self.logger.setLevel(logging_level)
		handler = logging.StreamHandler(logfile)
		handler.setFormatter(logging.Formatter(format))
		self.logger.addHandler(handler)
		return
	
	def transmit(self, content, address, size, type, timeout = 20):
		self.socket.connect(address)
		self.socket.settimeout(timeout)
		
		sha256 = 
		transmitting = True
		iteration = 0
		while transmitting:
			if iteration == 0:
				crc32 = zlib.crc32(part).to_bytes(4, byteorder="little")
		return True
	
	def send(content, address, timeout = 20):
		return transmit(content, address, timeout, )
	

if __name__ == "__main__":
	server = Server(('', 9000))
	server_return  = server.listen()
