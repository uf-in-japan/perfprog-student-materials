from hashlib import md5

hash_me_bro = "OneTwoThreeFourFive"
hash_obj = md5(hash_me_bro.encode()) # Default encoding is UTF-8
hash_digest = hash_obj.digest()
hash_int = int.from_bytes(hash_digest, byteorder='little') # digest() returns byte array
print(hash_digest) # Output: b"\xa7'5\x0b\x11\x93\x14\x01\xc3\xce\x958{\x15\xe5\x9d"
print(hash_int) # Output: 209878267012014200414229936932467845031
