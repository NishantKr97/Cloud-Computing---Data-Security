from hashlib import sha256
import struct
import logging

import hashlib


class HashError(Exception):
    pass

class CryptError(HashError):
    pass

log = logging.getLogger("convergent")


KByte = 1024
MByte = KByte * 1024

try:
    # use either pycryptopp
    from pycryptopp.cipher.aes import AES
except ImportError:
    # or use PyCrypto 
    from Crypto.Cipher import AES


class Counter(object):
    """ 16 Byte binary counter
    
    Example:
        c = Counter()
        c() => \00 * 16
        c() => \00...01
    """
    
    def __init__(self, a=0, b=0, c=0, d=0):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        
    first = True
    def __call__(self):
        if self.first:
            self.first = False
        else:
            if self.d < 0xFFFFFFFF:
                self.d += 1                     # increment byte 0
            elif self.c < 0xFFFFFFFF:
                self.c += 1                     # increment byte 1
                self.d = 0                      # reset byte 0
            elif self.b < 0xFFFFFFFF:
                self.b += 1                     # increment byte 2
                self.c = self.d = 0             # reset bytes 0 and 1
            elif self.a < 0xFFFFFFFF:
                self.a += 1                     # increment byte 3 
                self.b = self.c = self.d = 0    # reset bytes 0, 1, 2
        return struct.pack(">4L", self.a, self.b, self.c, self.d)


def aes(key, data, counter=False):
    """ encrypt data with aes, using either pycryptopp or PyCrypto.
        Args
            key: The encryption key
            data: plain text data
            counter: a callable, usually not needed
    """
    # using either pycryptopp...
    if hasattr(AES, "process"):
        a = AES(key)
        return a.process(data)
    # ... or PyCrypto
    counter = counter or Counter()
    a = AES.new(key, AES.MODE_CTR, counter=counter)
    rest = len(data) % 16
    if not rest:
        return a.encrypt(data)
    # Data length must be a multiple of 16
    # Pad with bytes all of the same value as the number of padding bytes
    pad = (16 - rest)
    data += chr(pad) * pad
    return a.encrypt(data)[:-pad]


class SHA256d(object):
    """ implements SHA-265d against length-extensions-attacks
        as defined by Schneier and Fergusson
    """
    
    def __init__(self, data=None, truncate_to=None):
        """ SHA-265d against length-extensions-attacks
            with optional truncation of the hash

        Args:
            data: Initial string, optional
            truncate_to: length to truncate the hash to, optional
        """
        self.h = sha256()
        self.truncate_to = truncate_to
        if data:
            self.h.update(data)
    
    def update(self, data):
        assert(isinstance(data, str))
        self.h.update(data)

    def digest(self):
        return sha256(self.h.digest()).digest()[:self.truncate_to]

    def hexdigest(self):
        return self.digest().encode('hex')
    

class ConvergentEncryption(object):
    info = "Digest: SHA-256d, Enc-Algo: AES 256 CTR"
    __convergence_secret = None

    def __init__(self, secret=None, warn=True):

        if secret:
            self.set_convergence_secret(secret)
        if not warn:
            self.__warn_convergence(warn=False)

    def set_convergence_secret(self, secret):

        secret = clean_string(secret)
        if self.__convergence_secret and self.__convergence_secret != secret:
            msg = "Do not change the convergence secret during encryption!"
            raise CryptError(msg)
        self.__convergence_secret = secret
    
    @classmethod
    def __warn_convergence(cls, warn=True):
        """ Utter this warning only once per system run"""
        if not hasattr(cls, "warned") and warn:
            msg = "No convergence secret, some information may leak."
            log.warning(msg)
        cls.warned = True

    def __sec_key(self, data):

        h = SHA256d(data)
        if not self.__convergence_secret:
            self.__warn_convergence()
        else:
            h.update(self.__convergence_secret)
        key = h.digest()
        del h
        id = SHA256d(key).digest()
        return key, id
    
    def encrypt(self, data):
        assert(isinstance(data, str))
        key, id = self.__sec_key(data)
        return key, id, aes(key, data)
    
    def decrypt(self, key, ciphertext, verify=False):
        plain = aes(key, ciphertext)
        if verify:
            h = SHA256d(plain)
            if self.__convergence_secret:
                h.update(self.__convergence_secret)
            digest = h.digest()
            # can verify only if convergence secret is known!
            if self.__convergence_secret and not key == digest:
                msg = "Block verification error on %s." % SHA256d(key).hexdigest()
                log.error(msg)
                raise CryptError(msg)
        return plain


def encrypt_key(key, nonce, data):
    key = clean_string(key)
    key = SHA256d(key).digest()
    print(key)
    nonce_hash = SHA256d(nonce).digest()# assert 32 bytes key
    enc_key = aes(key, nonce_hash)      # generate encryption key
    return aes(enc_key, data)           # encrypt data using the new key

def convergent_encryption(plainText):
	sha_signature = hashlib.sha256(plainText.encode()).hexdigest()
	return sha_signature

def main():
	plainText = input("Enter the text to be Encrypted : \n")
	cipherText = convergent_encryption(plainText)
	print(cipherText)



if __name__ == '__main__':
	main()
