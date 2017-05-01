import re
import math
from time import sleep, time
from easyraikit_config import *
from easyraikit import Rai

rai = Rai()

def raiblocks_account_validate(account):
	if isinstance(account, str):
		if ("xrb_1" in account) or ("xrb_3" in account) and (len(account) == 64):
			account = account[4:]
			char_validation = re.search("^[13456789abcdefghijkmnopqrstuwxyz]+$", account)
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

def raiblocks_unlock():
	global rai
	global wallet
	global wallet_password

	valid = rai.password_enter({"wallet": wallet, "password": wallet_password})
	if valid is not None:
		return valid["valid"]
	else:
		return "Wallet unlock failed."