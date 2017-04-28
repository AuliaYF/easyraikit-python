from time import sleep, time
from easyraikit_ext import *

print("--- RaiBlocks RPC Library for Python ---")
unlocked = raiblocks_unlock()

if unlocked == "1":
	bulk = [
		{
			"account": "xrb_3o7iocfcx1gcpa4q33ze56jmgicgct15kz4b4feu8mwxr43ju3t8cu668nei",
			"amount": 1
		},
		{
			"account": "xrb_3o7iocfcx1gcpa4q33ze56jmgicgct15kz4b4feu8mwxr43ju3t8cu668nei",
			"amount": 1
		},
		{
			"account": "xrb_3o7iocfcx1gcpa4q33ze56jmgicgct15kz4b4feu8mwxr43ju3t8cu668nei",
			"amount": 1
		},
		{
			"account": "xrb_3o7iocfcx1gcpa4q33ze56jmgicgct15kz4b4feu8mwxr43ju3t8cu668nei",
			"amount": 1
		},
		{
			"account": "xrb_3o7iocfcx1gcpa4q33ze56jmgicgct15kz4b4feu8mwxr43ju3t8cu668nei",
			"amount": 1
		}
	]

	print(raiblocks_bulk_send("xrb_1bawnqs6cc9a91ziwoy7fgmdycyjk9r6dt7eerfgzdbysrfnbihfxzobt8c8", bulk))