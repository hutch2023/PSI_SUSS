#!/usr/bin/python3
# Carey Hutchens m232850

from receiver import *
import sys
import time

# create alice
bob = Receiver(int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]))

############## OFFLINE STAGE ##############

# 1) bob generates an encoded message for each element 
t = time.process_time()
bob.gen_secrets_and_encodings()
gen_se_time = time.process_time() - t

# 2) bob interpolates the encodings
t = time.process_time()
bob.interpolate()
interp_time = time.process_time() - t

# Offline Stage complete, send ready message
bob.ready()

###########################################


############## ONLINE STAGE ###############

# begin online phase when both parties ready
bob.begin()
online_start_time = time.time()

# 3) bob receives alice's message and sends the polynomial (NETWORK)
bob.recv_m()
bob.send_p()

# 4) Generate potential matches for elements in K
t = time.process_time()
bob.gen_matches()
gen_mtchs_time = time.process_time() - t

# 5) Receive K (NETWORK)
bob.recv_k()

# 6) Check K for matches to generate an answer
t = time.process_time()
bob.check_k()
chk_k_time = time.process_time() - t

# Online phase complete
online_time = time.time() - online_start_time

###########################################

# Confirm answer correct
bob.send_ans()

# Save times
bob.benchmark_times(gen_se_time, interp_time, gen_mtchs_time, chk_k_time, online_time)
