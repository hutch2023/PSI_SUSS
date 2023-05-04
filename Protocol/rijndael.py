#!/usr/bin/python3
# Carey Hutchens m232850

from py3rijndael.rijndael import Rijndael

# Rijndael 256 cipher with block size 32
class MyRijndael:

    def __init__(self):
        self.bs = 32
        n = 2023202320232023 # Fixed key
        self.k = n.to_bytes(32,'big')

    # Methods encrypt and decrypt on 32 bytes only
    def encrypt(self,m):
        rij = Rijndael(key=self.k,block_size=self.bs)
        return rij.encrypt(m)

    def decrypt(self,c):
        rij = Rijndael(key=self.k,block_size=self.bs)
        return rij.decrypt(c)
