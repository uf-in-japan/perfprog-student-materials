from hashlib import md5

hash_me_bro = "OneTwoThreeFourFive"
hash_obj = md5(hash_me_bro.encode()) # Default encoding is UTF-8
hash_int = int.from_bytes(hash_obj.digest(), byteorder='little') # digest() returns byte array
print(hash_int)
