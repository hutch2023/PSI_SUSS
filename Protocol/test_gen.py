import sys
import numpy as np
import subprocess

# Get test sizes from cmd line
if len(sys.argv) != 8:
    print("Usage: python3 test_gen.py r_size bfrate stream_size s_start_size s_final_size s_size_step num_tests_per")
    exit()
r_size, bfrate, stream_size = sys.argv[1], sys.argv[2], sys.argv[3]
sss, sfs, sts, nt = int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7])

# set up tests each test
tests = np.arange(sss, sfs+sts, sts)
# tests = [128, 256, 512, 1024]
num_tests = len(tests)*nt
tests_run = 0

# Run tests
print("Running " + str(num_tests) + " tests")
for s_size in tests:
    for t in range(nt):
        subprocess.run(["python3", "middle.py", str(s_size), r_size, bfrate, stream_size])
        tests_run += 1
        print("Test " + str(tests_run) + " complete")
