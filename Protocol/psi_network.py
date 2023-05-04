#!/usr/bin/python3
# Carey Hutchens m232850

import socket
import subprocess

host = "127.0.0.1"
ms_port = 8003
mr_port = 9003

def create_connections(size_alice, size_bob, bfr, stream_size):
    s_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_sock.bind((host, ms_port))
    r_sock.bind((host, mr_port))
    s_sock.listen()
    r_sock.listen()
    subprocess.Popen(["python3", "alice.py", str(size_alice), str(bfr)])
    subprocess.Popen(["python3", "bob.py", str(size_bob), str(bfr), str(stream_size)])
    s_conn, s_addr = s_sock.accept()
    r_conn, r_addr = r_sock.accept()
    return s_conn, r_conn


