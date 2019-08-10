import os
import sys
import json
import socket

class DashboardClient:
	def __init__(self):
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect(('',9090))
			sock.send(str.encode("{\"action\" : \"is_alive\"}"))
			tokens = sock.recv(4918)
			message = tokens.decode()
			if message != "yes":
				raise Exception("Mismatch of test value")
			sock.close()
		except Exception as e:
			#print("Attempting start on Dashboard")
			#path = os.path.abspath(dashboard.__file__)
			#path = path[:path.rfind('/')]
			#path = path + '/dashboard_daemon.sh'
			#print(path)
			#subprocess.run([path, os.path.abspath(dashboard.__file__)])
			#sleep(5)
			print("The dashboard framework is down. Start it up manually.\nExecute the following")
			path = os.path.realpath(__file__)
			path = path[:path.rfind('/')]
			path1 = path+"/dashboard_daemon.sh"
			path2 = path+"/dashboard.py"
			print("sh {} {}".format(path1, path2))
			#print(e)
			sys.exit(1)
		self.silent = False
	
	
	def dispatch(self, js_obj):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		message = json.dumps(js_obj)
		try:
			sock.connect(('',9090))
			#print('Sending {} message\n'.format(message))
			string = str.encode(message)
			sock.send(string)
			if not self.silent:
				tokens = sock.recv(4918)
				message = tokens.decode()
				print(message)
		except Exception as e:
			print(e)
		finally:
			sock.close()
	
	def clear(self, **kwargs):
		clear_message = {"action" : "clear"}
		if "rows" in kwargs.keys() and "cols" in kwargs.keys():
			clear_message["rows"] = kwargs["rows"]
			clear_message["cols"] = kwargs["cols"]
		self.dispatch(clear_message)
	
	def add_trace(self, **kwargs):
		add_message = {}
		add_message["action"] = "add_trace"
		if "row" in kwargs.keys() and "col" in kwargs.keys():
			add_message["row"] = kwargs["row"]
			add_message["col"] = kwargs["col"]
		else:
			add_message["row"] = 1
			add_message["col"] = 1
		
		value = {}
		value["x"] = kwargs["x"]
		value["y"] = kwargs["y"]
		value["type"] = kwargs["type"]
		value["name"] = kwargs["name"]
		if "mode" in kwargs.keys():
			value["mode"] = kwargs["mode"]
		if "opacity" in kwargs.keys():
			value["opacity"] = kwargs["opacity"]
		add_message["value"] = value
		self.dispatch(add_message)
	
	def make_subplot(self, **kwargs):
		make_message = {"action" : "make_subplots"}
		for i in kwargs.keys():
			make_message[i] = kwargs.get(i)
		self.dispatch(make_message)
	
	def update(self, **kwargs):
		update_message = {"action" : "update_basics"}
		for i in kwargs.keys():
			update_message[i] = kwargs.get(i)
		self.dispatch(update_message)
	