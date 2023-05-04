#!/usr/bin/python3
# Carey Hutchens m232850

from sender import *
import sys
import time

# create alice
alice = Sender(int(sys.argv[1]), float(sys.argv[2]))


############## OFFLINE STAGE ##############

# 1) alice generates her private key and message
t = time.process_time()
alice.gen_m()
sender_msg_time = time.process_time() - t

# 2) alice hashes her own elements
t = time.process_time()
alice.hash_elements()
hash_time = time.process_time() - t

# Offline Stage complete, send ready message
alice.ready()

###########################################


############## ONLINE STAGE ###############

# begin online phase when both parties ready
alice.begin()

# 3) alice sends her message to bob and receives the polynomial (NETWORK)
alice.send_m()
alice.recv_p()

# 4) alice generates the return set K
t = time.process_time()
alice.gen_k()
gen_k_time = time.process_time() - t

# 5) Send the set K to bob
alice.send_k()

###########################################


# Save times
alice.benchmark_times(sender_msg_time, hash_time, gen_k_time)
