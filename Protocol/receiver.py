#!/usr/bin/python3
# Class for PSI Receiver

from polynomial import *
from psi_network import host, mr_port
import bloom_filter
import random
import socket
import mmh3

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
                        # BOB INTERFACE #
####################################################################

class Receiver:
    def __init__(self, size, bfr, stream_size):
        self.connect()
        self.get_dataset(size)
        self.bfr = bfr
        self.stream_size = stream_size
        self.secrets = []
        self.encodings = []
        self.possible_matches = []
        self.ans = []

    # Generate a secret and encoding for every element in Receiver set
    def gen_secrets_and_encodings(self):
        for _ in self.set:
            self.sec_and_enc()

    # Interpolate hashed set element, encoding pairs into a polynomial 
    def interpolate(self):
        xs = [hash(s).digest() for s in self.set]
        self.poly = interp(xs, self.encodings)

    # Receive Sender message
    def recv_m(self):
        self.msg = int.from_bytes(self.sock.recv(32), "big")

    # Send the polynomial degree and coefficients
    def send_p(self):
        self.sock.sendall(int(self.poly.degree()).to_bytes(4,"big"))
        for c in self.poly.list():
            self.sock.sendall(int(c).to_bytes(32,"big"))

    # Generate a potential match for every element in Receiver set
    def gen_matches(self):
        for i,e in enumerate(self.set):
            self.gen_a_match(i,e)

    # Receive K from Sender
    def recv_k(self):
        if self.bfr == 0:
            self.recv_set()
        else:
            self.recv_bf()

    # Check Receiver matches for K membership
    def check_k(self):
        if self.stream_size == 0:
            self.check_all_k()
        else:
            self.stream_check_k()

    # Send answer to Middle
    def send_ans(self):
        self.sock.sendall(len(self.ans).to_bytes(4,"big"))
        for i in self.ans:
            self.sock.sendall(i)


####################################################################
                        # HELPER FUNCTIONS #
####################################################################

    # Send Middle a message saying ready to begin online phase
    def ready(self):
        self.sock.sendall((1).to_bytes(1,"big"))

    # Receive begin message from Middle
    def begin(self):
        self.sock.recv(1)

    # Connect to middle
    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host,mr_port))

    # Receive dataset from middle
    def get_dataset(self, size):
        self.size = size
        self.set = []
        for _ in range(size):
            self.set.append(self.sock.recv(32))

    # generate a single secret and encoded message
    def sec_and_enc(self):
        b, m = curve.secretAndMessage()
        f = cipher.decrypt(m.val.to_bytes(32,'big'))
        self.secrets.append(b)
        self.encodings.append(f)

    # Receive K if its a set
    def recv_set(self):
        self.ret_set = set()
        ksize = int.from_bytes(self.sock.recv(4), 'big')
        for _ in range(ksize):
            self.ret_set.add(self.sock.recv(32))

    # Receive K if its a bloom filter
    def recv_bf(self):
        self.bfsize = int.from_bytes(self.sock.recv(4), 'big')
        self.sender_size = int.from_bytes(self.sock.recv(4), 'big')

        # If not streaming, just receive the full bloom filter
        if self.stream_size == 0:
            ba = self.sock.recv(self.bfsize)
            self.ret_set = bloom_filter.BloomFilter(self.sender_size, self.bfr, ba)

        # Else, receive the BF via streaming while checking in check_k()

    # Generate one potential match for K
    def gen_a_match(self, i, e):
        key = curve.sKey(self.secrets[i], self.msg, hash)
        h = hash()
        h.update(e)
        h.update(key)
        self.possible_matches.append(h.digest())

    # Check against the whole K
    def check_all_k(self):
        for i,m in enumerate(self.possible_matches):
            if self.query_k_mem(m):
                self.ans.append(self.set[i])

    # Stream check K
    def stream_check_k(self):
        # Setup for streaming
        item_hash_map = self.stream_setup()
        # Start Streaming
        i_shift = 0
        # While there is more BF to receive...
        while i_shift < self.bf_num_bits:
            # Get the next BF part
            bf_part = self.sock.recv(self.stream_size)
            bit_range = i_shift + self.stream_size * 8
            items_to_remove = []
            # For each potential item for the Receiver
            for i in item_hash_map.keys():
                ind_to_remove = []
                # For each index this item hashes to
                for ind in item_hash_map[i]:
                    # If this index is in this part of the BF (else break)
                    if ind < bit_range:
                        # If this bit is in the bloom filter, no need to check it again later
                        if bloom_filter.check_bit(bf_part, ind-i_shift):
                            ind_to_remove.append(ind)
                        # Else this index was not flipped in the BF, so its not a match
                        else:
                            items_to_remove.append(i)
                            break
                    else:
                        break
                # Remove all indices that were matches from this item
                for ind in ind_to_remove:
                    item_hash_map[i].remove(ind)
 
            # Shift the index shift
            i_shift += self.stream_size * 8
            # Remove all unwanted items
            for i in items_to_remove:
                item_hash_map.pop(i)

        # All remaining keys must be in the BF
        for i,e in list(item_hash_map.keys()):
            self.ans.append(self.set[i])

    # Streaming setup
    def stream_setup(self):
        self.bf_num_bits = self.bfsize * 8
        num_hashes = bloom_filter.get_hash_count(self.bf_num_bits, self.sender_size)
        return self.create_index_hash_map(self.possible_matches, num_hashes, self.bf_num_bits)

    # See if match is in K
    def query_k_mem(self, m):
        if self.bfr == 0:
            return m in self.ret_set
        else:
            return self.ret_set.check(m)

    # Create hash map for set items to their bf indices
    def create_index_hash_map(self, items, num_hashes, num_bits):
        d = dict()
        for i,e in enumerate(items):
            index_list = []
            for h in range(num_hashes):
                digest = mmh3.hash(e, h) % num_bits
                index_list.append(digest)
            index_list.sort()
            index_item_pair = (i,e)
            d[index_item_pair] = index_list
        return d
        
    # Send the benchmark times to middle
    def benchmark_times(self, gset, intt, gmt, ckkt, ot):
        self.sock.sendall(int(gset*10000).to_bytes(4,"big"))
        self.sock.sendall(int(intt*10000).to_bytes(4,"big"))
        self.sock.sendall(int(gmt*10000).to_bytes(4,"big"))
        self.sock.sendall(int(ckkt*10000).to_bytes(4,"big"))
        self.sock.sendall(int(ot*10000).to_bytes(4,"big"))
        self.sock.close()


