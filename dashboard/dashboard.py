
import plotly
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as graph

import dash
from dash.dependencies import Input
from dash.dependencies import Output

import dash_core_components as dcc
import dash_html_components as dhc

import os
import sys
import json
import socket
import threading

class DashboardDisplayServer:
	def __init__(self, **kwargs):
		self.title = "Dashboard Application"
		self.description = ""
		self.port = 8080
		if "port" in kwargs.keys():
			self.port = 8080
		self.app = dash.Dash(self.title, assets_external_path="./assets")
		self.graph_basics = {"rows" : 2, "cols" : 2, "height" : 700, "width" : 1200, "title_text" : "sample graph"}
		self.graph = make_subplots(rows = 1, cols = 1)
		self.graph = graph.Figure()
		#self.graph.append_trace({'x' : [0], 'y' : [0], 'name' : 'x y'}, row = 1, col = 1)
		self.app.layout = dhc.Div([
							dcc.Graph(id="graph", figure = self.graph, style={"margin-top" : "60pt"}),
							dhc.H3(id="desc", children=self.description),
							dhc.H1(id="title", children=self.title, style={"display" :"block", "position" :"fixed", "top" :"0","left" :"0"}),
							dhc.Button('Refresh', id="graph-update", style={"position" : "fixed","right" : "20pt","top": "20pt"})
						],
			style = {"text-align":"center"}
		)
		
		@self.app.callback(Output('graph', 'figure'), [Input('graph-update', 'n_clicks')])
		def update_graph(interval):
			#print("Graph updated")
			figure = self.graph
			figure.update_layout(height = self.graph_basics["height"], width = self.graph_basics["width"], title_text = self.graph_basics["title_text"])
			#print(str(figure))
			return figure
	
	def clear_graph(self, js):
		self.graph = graph.Figure()
		return "cleared"
	
	def update_basics(self, js):
		if "rows" in js.keys():
			self.graph_basics["rows"] = js["rows"]
		if "cols" in js.keys():
			self.graph_basics["cols"] = js["cols"]
		if "height" in js.keys():
			self.graph_basics["height"] = js["height"]
		if "width" in js.keys():
			self.graph_basics["width"] = js["width"]
		if "title" in js.keys():
			self.graph_basics["title_text"] = js["title"]
		return "updated"
	
	def make_subplots(self, js):
		if "rows" in js.keys() and "cols" in js.keys():
			self.update_basics(js)
		self.graph = make_subplots(rows = self.graph_basics["rows"], cols = self.graph_basics["cols"])
		return "subplots made"
	
	def add_trace(self, js_obj):
		try:
			self.graph.append_trace(js_obj["value"], row = js_obj["row"], col = js_obj["col"])
			#print("add_trace implemented")
		except Exception as e:
			return str(e)
		return "added trace"
	
	def get_server(self):
		return self.app.server
	
	def start(self):
		print('Displaying at port http://localhost:{}/'.format(self.port))
		return self.app.run_server(port = self.port, threaded = True, debug = False)
	
	def is_live(self, js):
		return "yes"
	
	#Complete the function below
	def act_on(self, js_obj):
		switcher = {
			"clear" : self.clear_graph,
			"update_basics" : self.update_basics,
			"make_subplots" : self.make_subplots,
			"add_trace" : self.add_trace,
			"is_alive" : self.is_live
		}
		action = switcher.get(js_obj["action"])
		#print("Action to be performed : {}".format(js_obj["action"]))
		return action(js_obj)

def dashboard_async_listener(**kwargs):
	port = kwargs["port"]
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('',port))
	s.listen(10)
	print('\nListening at port localhost:{}/'.format(port))
	while True:
		conn, addr = s.accept()
		try:
			tokens = conn.recv(2097152)
			message = tokens.decode()
			if message == "exit":
				sys.exit(0)
			obj = json.loads(message)
			print('{} {}'.format(addr, obj["action"]))
			res = kwargs["display"].act_on(obj)
			conn.send(str.encode(res))
		except Exception as e:
			print('ListenerException : ',e)
		finally:
			conn.close()
	print('Listening server closed')

class DashManager:
	def __init__(self):
		self.display_server = DashboardDisplayServer(port = 9000)
		self.display = threading.Thread(target = self.display_server.start)
		#self.display.setDaemon(True)
		
		listener_kwargs = {"display" : self.display_server, "port" : 9090}
		self.listener = threading.Thread(target = dashboard_async_listener, kwargs=listener_kwargs)
		#self.listener.setDaemon(True)
	
	def start(self, **kwargs):
		self.display.start()
		self.listener.start()
		print('\nDashboard started.')
	
	def join(self):
		self.listener.join()
		self.display.join()
		print('Terminated all')

def start_dashboard():
	man = DashManager()
	man.start()
	man.join()
	return man

start_dashboard()