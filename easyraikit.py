import json
import requests
from time import sleep
from easyraikit_config import *

class Rai:
	def __getattr__(self, name, *args):
		def function (*args):
			global server

			if server:
				request = {}
				request["action"] = name
				if args:
					for key, value in args[0].items():
						request[key] = value
				try:
					r = requests.post(server, data = json.dumps(request)).json()

					if "error" not in r:
						return(r)
					else:
						print(r["error"])
						return None
				except:
					sleep(0.5)
					r = requests.post(", data = json.dumps(request)).json()

					if "error" not in r:
						return(r)
					else:
						print(r["error"])
						return None
			else:
				print("Wrong server configuration.")

		return function
