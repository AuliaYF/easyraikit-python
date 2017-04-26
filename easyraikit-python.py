import json
import requests
import configparser
from time import sleep

config = configparser.ConfigParser()
config.read('config.cfg')
server = config.get('main', 'server')
wallet = config.get('main', 'wallet')

class Rai:
	def __getattr__(self, name, *args):
		def function (*args):
			request = {}
			request['action'] = name
			if args:
				for key, value in args[0].items():
					request[key] = value
			try:
				r = requests.post(server, data = json.dumps(request)).json()

				if 'error' not in r:
					return(r)
				else:
					print(r['error'])
					return(r['error'])
			except:
				sleep(0.5)
				r = requests.post('', data = json.dumps(request)).json()

				if 'error' not in r:
					return(r)
				else:
					print(r['error'])
					return(r['error'])

		return function

rai = Rai()
block_count = rai.block_count()
print("Block Count: {:,} ({:,})".format(int(block_count['count']), int(block_count['unchecked'])))