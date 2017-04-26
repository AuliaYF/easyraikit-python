import re
import binascii
from hashlib import blake2b

is_array = lambda var: isinstance(var, (list, tuple))

def array_slice( array , offset , length = None ):
	if is_array( array ) and not isinstance( array , dict ):
		if isinstance( array , set ):
			array = list( array )
			return set( array[offset:length] )
		return array[offset:length]
	return False

def raiblocks_account_validate(account):
	if isinstance(account, str):
		if ('xrb_1' in account) or ('xrb_3' in account) and (len(account) == 64):
			account = account[4:]
			char_validation = re.search('^[13456789abcdefghijkmnopqrstuwxyz]+$', account)
			if char_validation is not None:
				def to_uint5(n):
					letter_list = list("13456789abcdefghijkmnopqrstuwxyz")
					return letter_list.index(n)
				def test(n):
					return str(n)

				account_array = list(account)
				uint5 = list(map(to_uint5, account_array))
				
				uint8 = [None]*37
				uint8[0] = ((uint5[0] << 7) + (uint5[1] << 2) + (uint5[2] >> 3)) % 256;
				uint8[1] = ((uint5[2] << 5) + uint5[3]) % 256;

				for i in range(0, 7):
					uint8[5*i+2] = (uint5[8*i+4] << 3) + (uint5[8*i+5] >> 2);
					uint8[5*i+3] = ((uint5[8*i+5] << 6) + (uint5[8*i+6] << 1) + (uint5[8*i+7] >> 4)) % 256;
					uint8[5*i+4] = ((uint5[8*i+7] << 4) + (uint5[8*i+8] >> 1)) % 256;
					uint8[5*i+5] = ((uint5[8*i+8] << 7) + (uint5[8*i+9] << 2) + (uint5[8*i+10] >> 3)) % 256;
					uint8[5*i+6] = ((uint5[8*i+10] << 5) + uint5[8*i+11]) % 256;

				key = uint8[:32]
				key_string = ''.join(map(chr, key))
				tKey_string = str.encode(key_string)
				tStr = ''.join(list(map(chr, list(reversed(array_slice(uint8, 32))))))
				tByte = str.encode(tStr)
				hash = binascii.hexlify(tByte)
				tHash1 = hash[2:-5]
				tHash2 = hash[11:]
				hash = "{}{}".format(tHash1.decode("utf-8"), tHash2.decode("utf-8"))

				b2 = blake2b(digest_size=5)
				b2.update(tKey_string)
				check = b2.hexdigest()
				
				if hash == check:
					return True
				else:
					return False
			else:
				return False
		else:
			return False
	else:
		return False