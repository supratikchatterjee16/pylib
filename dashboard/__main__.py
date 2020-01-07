from __init__ import DashManager

def start_dashboard():
	man = DashManager()
	man.start()
	man.join()
	return man

start_dashboard()