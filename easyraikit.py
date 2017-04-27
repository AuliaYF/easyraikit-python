import re
import math
import json
import requests
import configparser
from time import sleep

config = configparser.ConfigParser()
config.read('config.cfg')
server = config.get('main', 'server')
wallet = config.get('main', 'wallet')
wallet_password = config.get('main', 'wallet_password')

def raiblocks_account_validate(account):
	if isinstance(account, str):
		if ('xrb_1' in account) or ('xrb_3' in account) and (len(account) == 64):
			account = account[4:]
			char_validation = re.search('^[13456789abcdefghijkmnopqrstuwxyz]+$', account)
			if char_validation is not None:
				return True
			else:
				return False
		else:
			return False
	else:
		return False

def raiblocks_mrai_from_raw(raw):
	return int(math.floor(raw / (10 ** 30)))

def raiblocks_mrai_to_raw(mrai):
	return int(math.floor(mrai * (10 ** 30)))

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
					return None
			except:
				sleep(0.5)
				r = requests.post('', data = json.dumps(request)).json()

				if 'error' not in r:
					return(r)
				else:
					print(r['error'])
					return None

		return function
