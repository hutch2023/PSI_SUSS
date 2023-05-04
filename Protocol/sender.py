#!/usr/bin/python3
# Class for PSI Sender

from polynomial import *
from psi_network import host, ms_port
import bloom_filter
import random
import socket

#######################
# Curve 25519 as EC
# R256 as Block Cipher
# SHA256 as Hash Oracle
import curves
import rijndael
import hashlib
cipher = rijndael.MyRijndael()
curve = curves.Curve25519()
hash = hashlib.sha256
########################

####################################################################
                        # ALICE INTERFACE #
####################################################################

class Sender:
    def __init__(self, size, bfr):
        self.connect()
        self.get_dataset(size)
        self.create_return_set(bfr)

    # Generate Sender message
    def gen_m(self):
        self.a, self.m = curve.secretAndMessage()

    # Send Sender message
    def send_m(self):
        self.sock.sendall(self.m.val.to_bytes(32,"big"))

    # Receive the polynomial
    def recv_p(self):
        coef = self.receive_coef()
        self.poly = reform_poly(coef)

    # Generate set K
    def gen_k(self):
        for i,e in enumerate(self.hash_set):
            self.gen_k_ele(i,e)
        if self.bfr == 0:
            random.shuffle(self.ret_set)

    # Send K to Receiver
    def send_k(self):
        if self.bfr == 0:
            self.send_set()
        else:
            self.send_bf()

####################################################################
                        # HELPER FUNCTIONS #
####################################################################

    # Send Middle a message saying ready to begin online phase
    def ready(self):
        self.sock.sendall((1).to_bytes(1,"big"))

    # Receive begin message from Middle
    def begin(self):
        self.sock.recv(1)

    # Connect to middle socket
    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host,ms_port))

    # Receive the sender datast from middle
    def get_dataset(self, size):
        self.size = size
        self.set = []
        for _ in range(size):
            self.set.append(self.sock.recv(32))

    # Create K, either a list or a bloom filter
    def create_return_set(self, bfr):
        self.bfr = bfr
        if bfr > 0:
            self.ret_set = bloom_filter.BloomFilter(self.size, bfr)
        else:
            self.ret_set = []

    # Hash elements in the offline phase
    def hash_elements(self):
        self.hash_set = []
        for e in self.set:
            self.hash_set.append(hash(e).digest())

    # Receive the coefficients of the polynomial
    def receive_coef(self):
        deg = int.from_bytes(self.sock.recv(4), "big")
        coef = []
        for _ in range(deg+1):
            coef.append(int.from_bytes(self.sock.recv(32), "big"))
        return coef

    # For a given element in the set, generate its K represention
    def gen_k_ele(self, i, e):
        m = eval(self.poly, e, cipher)
        key = curve.sKey(self.a, m, hash)
        self.add_to_ret_set(self.set[i], key)

    # Add the item to K
    def add_to_ret_set(self, item, key):
        h = hash()
        h.update(item)
        h.update(key)
        x = h.digest()
        if self.bfr > 0:
            self.ret_set.add(x)
        else:
            self.ret_set.append(x)

    # Send K if its a bloom filter
    def send_bf(self):
        self.sock.sendall(self.ret_set.len().to_bytes(4,'big'))
        self.sock.sendall(self.size.to_bytes(4,'big'))
        self.sock.sendall(self.ret_set.bf)

    # Send K if its a list
    def send_set(self):
        self.sock.sendall(len(self.ret_set).to_bytes(4,'big'))
        for k in self.ret_set:
            self.sock.sendall(k)

    # Send the benchmark times to middle
    def benchmark_times(self, smt, ht, gkt):
        self.sock.sendall(int(smt*10000).to_bytes(4,"big"))
        self.sock.sendall(int(ht*10000).to_bytes(4,"big"))
        self.sock.sendall(int(gkt*10000).to_bytes(4,"big"))
        self.sock.close()

        