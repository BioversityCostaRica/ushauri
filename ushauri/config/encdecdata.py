# # From http://depado.markdownblog.com/2015-05-11-aes-cipher-with-python-3-x
#
# import base64
# import hashlib
#
# from Crypto import Random
# from Crypto.Cipher import AES
#
#
# class AESCipher(object):
#     """
#     A classical AES Cipher. Can use any size of data and any size of password thanks to padding.
#     Also ensure the coherence and the type of the data with a unicode to byte converter.
#     """
#
#     def __init__(self, key):
#         self.bs = 32
#         self.key = hashlib.sha256(AESCipher.str_to_bytes(key)).digest()
#
#     @staticmethod
#     def str_to_bytes(data):
#         u_type = type(b"".decode("utf8"))
#         if isinstance(data, u_type):
#             return data.encode("utf8")
#         return data
#
#     def _pad(self, s):
#         return s + (self.bs - len(s) % self.bs) * AESCipher.str_to_bytes(
#             chr(self.bs - len(s) % self.bs)
#         )
#
#     @staticmethod
#     def _unpad(s):
#         return s[: -ord(s[len(s) - 1 :])]
#
#     def encrypt(self, raw):
#         raw = self._pad(AESCipher.str_to_bytes(raw))
#         iv = Random.new().read(AES.block_size)
#         cipher = AES.new(self.key, AES.MODE_CBC, iv)
#         return base64.b64encode(iv + cipher.encrypt(raw)).decode("utf-8")
#
#     def decrypt(self, enc):
#         enc = base64.b64decode(enc)
#         iv = enc[: AES.block_size]
#         cipher = AES.new(self.key, AES.MODE_CBC, iv)
#         return self._unpad(cipher.decrypt(enc[AES.block_size :])).decode("utf-8")


from Crypto.Cipher import AES
import base64


# the block size for the cipher object; must be 16, 24, or 32 for AES
BLOCK_SIZE = 32

# the character used for padding--with a block cipher such as AES, the value
# you encrypt must be a multiple of BLOCK_SIZE in length.  This character is
# used to ensure that your value is always a multiple of BLOCK_SIZE
PADDING = "|"
BPADDING = b"|"


def pad(s):
    # pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
    return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING


# encrypt with AES, encode with base64


def encode_aes(c, s):
    # EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
    return base64.b64encode(c.encrypt(pad(s).encode()))


def decode_aes(c, e):
    # DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(BPADDING)
    return c.decrypt(base64.b64decode(e)).rstrip(BPADDING)


def encodeData(request, data):
    secret = request.registry.settings["aes.key"].encode()
    cipher = AES.new(secret, 1)
    return encode_aes(cipher, data)


def decodeData(request, data):
    secret = request.registry.settings["aes.key"].encode()
    cipher = AES.new(secret, 1)
    return decode_aes(cipher, data)


def encode_data_with_aes_key(data, key):
    cipher = AES.new(key, 1)
    return encode_aes(cipher, data)
