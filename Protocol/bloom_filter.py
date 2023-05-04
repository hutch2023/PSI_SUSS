#! /usr/bin/env python3
# Carey Hutchens m232850

import math
import mmh3

# Set this bit in the bytearray
def set_bit(bf, bit):
	bf[bit//8] |= (0b10000000 >> (7-(bit%8)))

# Check this bit in the bytearray
def check_bit(bf, bit):
	return bool(bf[bit//8] & (0b10000000 >> (7-(bit%8))))

# For a given number of items and fp_rate, return the BF size in bits
def get_size(n, p):
	m = int(-(n * math.log(p))/(math.log(2)**2))
	m += 8 - (m % 8)
	return m

# For a given size and expected number of items, return the hash count
def get_hash_count(m, n):
	k = (m/n) * math.log(2)
	return int(k)

class BloomFilter(object):

	# init a new Bloom Filter
	def __init__(self, items_count, fp_prob, ba=None):

		# False possible probability in decimal
		self.fp_prob = fp_prob

		# Size of bytearray to use in bits
		self.num_bits = get_size(items_count, fp_prob)

		# Size in bytes
		self.num_bytes = self.num_bits // 8

		# number of hash functions to use
		self.hash_count = get_hash_count(self.num_bits, items_count)

        # Initialized or Zeroed Bytearray
		if ba is not None:
			self.bf = ba
		else:
			self.bf = bytearray(self.num_bytes)
	
	# Add an item to the bloom filter
	def add(self, item):
		
		# For each hash,
		for i in range(self.hash_count):

			# create digest for given item where i is a seed to the hash
			digest = mmh3.hash(item, i) % self.num_bits

			# Set that digest in the bytearray
			set_bit(self.bf, digest)

	# Check for existence of an item in filter
	def check(self, item):

		# for each hash
		for i in range(self.hash_count):

			# create digest for given item where i is a seed to the hash
			digest = mmh3.hash(item, i) % self.num_bits

			# Return false if that digest isn't set
			if not check_bit(self.bf, digest):
				return False
			
		# If every digest is set, it's probably True
		return True
	
	# Get the length
	def len(self):
		return len(self.bf)

	
			

	