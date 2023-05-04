#!/usr/bin/python3
# Carey Hutchens m232850

from testing import *
from psi_network import create_connections
import time
import sys

####################################################################
                        # HELPER FUNCTIONS #
####################################################################

def get_args():
    if len(sys.argv) != 5:
        print("Usage: python3 middle.py size_alice size_bob bfrate stream_size")
        exit()
    return int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4])

def ready_set_go():
    s_conn.recv(1)
    r_conn.recv(1)
    s_conn.sendall((1).to_bytes(1,"big"))
    r_conn.sendall((1).to_bytes(1,"big"))

def send_alice_msg():
    alice_msg = s_conn.recv(32)
    r_conn.sendall(alice_msg)
    return 32

def send_polynomial():
    size = 4
    bdeg = r_conn.recv(4)
    s_conn.sendall(bdeg)
    deg = int.from_bytes(bdeg,'big')
    for _ in range(deg+1):
        c = r_conn.recv(32)
        s_conn.sendall(c)
        size += 32
    return size

def send_k_list():
    ksize = s_conn.recv(4)
    r_conn.sendall(ksize)
    size = 4
    ksize = int.from_bytes(ksize,'big')
    for _ in range(ksize):
        m = s_conn.recv(32)
        r_conn.sendall(m)
        size += 32
    return size

def send_k_bf():
    bf_size = s_conn.recv(4)
    r_conn.sendall(bf_size)
    sender_set_size = s_conn.recv(4)
    r_conn.sendall(sender_set_size)
    bf_size = int.from_bytes(bf_size,'big')
    m = s_conn.recv(bf_size)
    r_conn.sendall(m)
    return bf_size + 8

def send_k():
    if bfr == 0:
        return send_k_list()
    else:
        return send_k_bf()
    
def recv_ans():
    ans_size = int.from_bytes(r_conn.recv(4), 'big') 
    comp_ans = set()
    for _ in range(ans_size):
        comp_ans.add(r_conn.recv(32))
    return comp_ans

def display_wrong_ans(act_ans, comp_ans):
    print("Produced wrong answer")
    print("Actual answer:")
    for a in act_ans:
        print(a)
    print("\nComputed answer:")
    for c in comp_ans:
        print(c)
    exit()

####################################################################
                        # PROGRAM SET UP #
####################################################################

# get arguments
size_alice, size_bob, bfr, stream_size = get_args()

# create datasets
a_values, b_values = create_data(size_alice, size_bob)

# connections to sender and receiver
s_conn, r_conn = create_connections(size_alice, size_bob, bfr, stream_size)

# distribute data sets
distribute_data(s_conn, r_conn, a_values, b_values)

# Wait for sender and receiver to be ready, then start
ready_set_go()

####################################################################
                        # RUN PROTOCOL #
####################################################################

# pass alice msg
sender_msg_size = send_alice_msg()

# pass polynomial
polynomial_size = send_polynomial()

# pass K
k_size = send_k()

####################################################################
                        # ENSURE CORRECTNESS #
####################################################################

comp_ans = recv_ans()
act_ans = set(a_values).intersection(b_values)
if not act_ans == comp_ans:
    display_wrong_ans(act_ans, comp_ans)
else:
    print('Test correct!')

####################################################################
                            # BENCHMARK #
####################################################################

# Receive Sender Times
sender_msg_time = str(int.from_bytes(s_conn.recv(4),"big") / 10000)
sender_hsh_time = str(int.from_bytes(s_conn.recv(4),"big") / 10000)
sender_gkt_time = str(int.from_bytes(s_conn.recv(4),"big") / 10000)

# Receive Receiver Times
recver_gse_time = str(int.from_bytes(r_conn.recv(4),"big") / 10000)
recver_itp_time = str(int.from_bytes(r_conn.recv(4),"big") / 10000)
recver_gmt_time = str(int.from_bytes(r_conn.recv(4),"big") / 10000)
recver_chk_time = str(int.from_bytes(r_conn.recv(4),"big") / 10000)
recver_onl_time = str(int.from_bytes(r_conn.recv(4),"big") / 10000)

# Sizes
ttl_size = str(sender_msg_size + polynomial_size + k_size)
msg_size = str(sender_msg_size)
pol_size = str(polynomial_size)
kst_size = str(k_size)

# Label this test
test_type = str(size_alice) + "_" + str(size_bob) + "_" + str(bfr) + "_" + str(stream_size)

# Write times to times file
times_file = open("../data_collection/times.csv", "a")
times_file.write(test_type      + "," +
                sender_msg_time + "," + 
                sender_hsh_time + "," + 
                sender_gkt_time + "," +
                recver_gse_time + "," +
                recver_itp_time + "," +
                recver_gmt_time + "," +
                recver_chk_time + "," +
                recver_onl_time + "\n")
times_file.close()

# write sizes to sizes file
sizes_file = open("../data_collection/sizes.csv", "a")
sizes_file.write(test_type + "," +
                msg_size + "," + 
                pol_size + "," + 
                kst_size + "," +
                ttl_size + "\n")
sizes_file.close()

