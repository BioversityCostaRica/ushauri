# From http://depado.markdownblog.com/2015-05-11-aes-cipher-with-python-3-x

import base64
import logging

from cryptography.fernet import Fernet

log = logging.getLogger("ushauri")


class AESCipher(object):
    """
    A classical AES Cipher. Can use any size of data and any size of password thanks to padding.
    Also ensure the coherence and the type of the data with a unicode to byte converter.
    """

    def encrypt(self, request, data):
        key = request.registry.settings["aes.key"].encode()
        key = base64.b64encode(key)
        f = Fernet(key)
        if not isinstance(data, bytes):
            data = data.encode()
        return f.encrypt(data)

    def decrypt(self, request, data):
        key = request.registry.settings["aes.key"].encode()
        key = base64.b64encode(key)
        f = Fernet(key)
        try:
            return f.decrypt(data)
        except Exception as e:
            log.error("Error when decrypting a password. Error: {}".format(str(e)))
            return ""


def encode_data_with_key(data, key):
    key = base64.b64encode(key)
    f = Fernet(key)
    if not isinstance(data, bytes):
        data = data.encode()
    return f.encrypt(data)


def decode_data_with_key(data, key):
    key = base64.b64encode(key)
    f = Fernet(key)
    try:
        return f.decrypt(data)
    except Exception as e:
        log.error("Error when decrypting a password. Error: {}".format(str(e)))
        return ""
