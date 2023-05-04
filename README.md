# Private Set Intersection on Small, Unequal Sized Sets

## Authors
Dr. Seung Geol Choi, Associate Professor, United States Naval Academy, Computer Science Department  
Dr. Daniel Roche, Professor, United States Naval Academy, Computer Science Department  
Carey Hutchens, MIDN, United States Naval Academy, Computer Science Department  

## Description
We design and implement a private set intersection (PSI) algorithm for small, unequally sized sets. We begin with a protocol developed by Rosulek and Trieu in 2021. We then incorporate a bloom filter to improve communication costs in the case of a larger Sender set size with a memory-limited Receiver. This adaptation achieves a significant reduction in communication costs while upholding security and maintaining computational costs. We implemented our protocol in Python and showed that our protocol achieves 2.6 - 4.4$\times$ improvement in communication cost using a bloom filter.

## Installation
1. Download the entire Protocol folder into a directory.
2. Download Mambaforge by doing the following:  
- Choose and download the appropriate installer for your machine [here](https://github.com/conda-forge/miniforge#mambaforge)  
- Execute the installer
- Run the following command: mamba create -n psi sage numpy pandas matplotlib pycryptodome mmh3
- Then run mamba activate psi to activate the environment  
3. Lastly, pip install the following libraries:  
- pip install py3rijndael

## Usage
To run the PSI protocol, run the following:  
python3 test_gen.py r_size bfrate stream_size s_start_size s_final_size s_size_step num_tests_per
- r_size is the size of the receiver set
- bfrate is the false positive rate of the bloom filter, or 0 when not using a bloom filter
- stream_size is the storage cap the Receiver has when processing the bloom filter, or 0 when not streaming
- s_start_size is the first sender set size
- s_final_size is the last sender set size
- s_size_step is how the sender set size linearly grows
- num_tests_per is the number of times to run each test 

These tests will output their time and size costs to times.csv and sizes.csv in the Data folder. The data can be analyzed directly, or the user can run the graph generator code found there to visualize test results.

## Description of Files
alice.py - Runs the Sender Code  
bob.py - Runs the Receiver Code  
middle.py - acts as the network on which Alice and Bob conduct the PSI protocol  
sender.py - contains the Sender code  
receiver.py - contains the Receiver code  

test_gen.py - interface for running multiple psi protocol tests  
testing.py - contains code to initialize a new test  
psi_network.py - contains code for setting up sockets  

curves.py - contains code for all ECDHKA operations  
elligator.py - contains code for all ECDHKA encodings  
polynomial.py - contains code for all polynomial interpolation and evaluations  
rijndael.py - contains code for all R256 block cipher operations  
bloom_filter.py - contains code for all bloom filter operations  

slack.py - code to determine the minimum number of hashes for the bloom_filter for a given adversary  

## Help
If you have any troubles with installing or running the code, reach out to Carey Hutchens at careyhutchens@gmail.com.  

## Acknowledgment
Thank you to the USNA Bowman Scholar program for spurring this project, and thank you to Dr. Roche and Dr. Choi for showing me the daunting and rewarding sides of research. 
