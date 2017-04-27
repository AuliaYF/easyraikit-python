import re

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