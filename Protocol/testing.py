#!/usr/bin/python3
# Carey Hutchens m232850
# Testing Helper Methods

import random
import os

# create data sets
def create_data(size_alice, size_bob):
    overlap = max([(min([size_alice, size_bob])//2),1])
    add_to_bob = size_bob - overlap
    a_values = [os.urandom(32) for _ in range(size_alice)]
    b_values = random.sample(a_values, k=overlap)
    for _ in range(add_to_bob):
        b_values.append(os.urandom(32))
    random.shuffle(b_values)
    return a_values, b_values

# Distribute data sets
def distribute_data(s_conn, r_conn, a_values, b_values):
    for a in a_values:
        s_conn.sendall(a)
    for i,b in enumerate(b_values):
        r_conn.sendall(b)
