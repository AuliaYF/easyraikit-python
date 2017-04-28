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

def raiblocks_bulk_send(source, bulk):
	"""Function for sending bulk transaction

    Args:
        source: The source address
        bulk: The list containing array of account & amount in mrai

    Returns:
        Returns a list of valid transaction containing its index from bulk, block and time of excecution

    """
	global wallet

	blocks = []
	for obj in bulk:
		start_time = time()
		block = rai.send({"wallet": wallet, "source": source, "destination": obj["account"], "amount": raiblocks_mrai_to_raw(obj["amount"])})
		if block is not None:
			blocks.append({
					"index": bulk.index(obj),
					"block": block["block"],
					"time_ellapsed": (time() - start_time)
				})
		sleep(5) # my server needs this xD

	return blocks
