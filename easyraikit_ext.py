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
	return int(math.floor(int(raw) / (10 ** 30)))

def raiblocks_mrai_to_raw(mrai):
	return int(math.floor(int(mrai) * (10 ** 30)))

def raiblocks_rai_from_raw(raw):
	return int(math.floor(int(raw) / (10 ** 25)))

def raiblocks_rai_to_raw(rai):
	return int(math.floor(int(rai) * (10 ** 25)))

def raiblocks_unlock():
	global rai
	global wallet
	global wallet_password

	valid = rai.password_enter({ "wallet": wallet, "password": wallet_password })
	if valid is not None:
		return valid["valid"]
	else:
		return "Wallet unlock failed."

def raiblocks_balance_wallet():
	global rai
	global wallet

	accounts_balances = { "accounts": {}, "sum_balance_rai": 0, "sum_pending_rai": 0, "n_accounts": 0 }
	ret2 = rai.account_list({"wallet": wallet});

	for account in ret2["accounts"]:
		ret2 = rai.account_balance({"account": account})
		accounts_balances["accounts"][account] = {
			'balance_rai': raiblocks_rai_from_raw(ret2["balance"]),
			'pending_rai': raiblocks_rai_from_raw(ret2["pending"])
		}

		accounts_balances["sum_balance_rai"] += accounts_balances["accounts"][account]["balance_rai"]
		accounts_balances["sum_pending_rai"] += accounts_balances["accounts"][account]["pending_rai"]
		accounts_balances["n_accounts"] += 1

	return accounts_balances

def raiblocks_send_wallet(destination, amount):
	global rai
	global wallet

	payment_hashes = { "accounts": {}, "status": "ok", "sum_paid_rai": 0 }
	selected_accounts = {}
	diff_amount = amount

	sum = 0
	account_list = raiblocks_balance_wallet()
	for account, balance in account_list["accounts"].items():
		if account is not None:
			if balance["balance_rai"] > 0:
				selected_accounts[account] = balance["balance_rai"]
				sum += balance["balance_rai"]
			else:
				continue

			if sum >= amount:
				break

	if sum < amount:
		payment_hashes["sum_paid_rai"] = 0
		payment_hashes["status"] = "not enough funds."
		return payment_hashes

	for selected_account, balance in selected_accounts.items():
		if selected_accounts is not None:
			if diff_amount - balance < 0:
				balance = diff_amount

			args = {
				'wallet': wallet,
				'source': selected_account,
				'destination': destination,
				'amount': raiblocks_rai_to_raw(balance)
			}

			ret = rai.send(args)

			if ret["block"] != "0000000000000000000000000000000000000000000000000000000000000000":
				payment_hashes["accounts"][selected_account] = {
					"hash": ret["block"],
					"amount_rai": balance
				}

				payment_hashes["sum_paid_rai"] += balance
				diff_amount -= balance
			else:
				payment_hashes["accounts"][selected_account] = {
					"hash": "error",
					"amount_rai": balance
				}

				payment_hashes["status"] = "error"

	return payment_hashes

def raiblocks_n_accounts(n):
	global rai
	global wallet

	accounts_created = { "accounts": [], "n": n, "n_generated": 0 }

	i = 0

	while i < n:
		ret = rai.account_create({ "wallet": wallet })

		if ret["account"] != "":
			accounts_created["n_generated"] += 1
			accounts_created["accounts"].append(ret["account"])

		i += 1

	return accounts_created
