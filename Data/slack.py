import pandas as pd
import math
import matplotlib.pyplot as plt

################ FUNCTIONS ################

# for a given fp rate and set items, 
# find number of bits needed for bloom filter
def get_size(p, m):
	n = -(m * math.log(p))/(math.log(2)**2)
	return int(n)

# for a given num hash functions, set items, and bits in the bloom filter,
# find the false positive rate 
def get_fprate(k,m,n):
    return (1 - (math.e)**(-1 * k * m / n))**k

# calculate the chance that an adversary would win the pack bloom filter game
# the odds are negligible as long as tf < 1
def calc_tf(k,t,q,m):
    term1 = (2*math.e)**(1/(2*math.log(2)))
    term2 = (1/2)**(t*k)
    term3 = ((math.e * q)/(t*m))**t
    tf = term1*term2*term3
    return tf

# The sizes of the sender set using the normal protocol (no bloom filter)
nobf_sizes = {500:16004, 600:19204, 700:22404, 800:25604, 900:28804, 1000:32004}

####################################################################

################ DATA COLLECTION ################

# fix slack to 1.1
t = 1.1

# adversarial power (computing hash keywords)
q_pows = [i for i in range(40, 105, 10)]
qs = [2**pow for pow in q_pows]

# number of bloom filter elements (based on protocol application)
ms = [128, 256, 512, 1024]

data = {'q':[],'k':[],'m':[],'t':[],'term':[]}
data = pd.DataFrame(data=data)

# find the smallest k that makes adversary winning odds negligible
for m in ms:
    for q in qs:
        k = 120
        while True:
            tf = calc_tf(k,t,q,m)
            if tf == 0 or m*math.log(tf) < -80*math.log(2):
                k -= .001
            else:
                k += .001
                data.loc[len(data.index)] = [q,k,m,t,tf]
                break

# ks for desired false positive rate
fp_rates = ["$2^{-40}$", "$2^{-60}$", "$2^{-80}$"]
ks = [40,60,80]

####################################################################

################ GRAPHING ################

# Adding Data
data_lines = []
for m in ms:
    this_m_data = data[data['m'] == m]
    this_m_ks = this_m_data['k'].values
    line, = plt.plot(q_pows, this_m_ks, label=str(m))
    data_lines.append(line)

# Adding Ks for FP Rates
k_lines = []
for i,k in enumerate(ks):
    line, = plt.plot(q_pows,[k for _ in range(len(q_pows))],'--',label=fp_rates[i])
    k_lines.append(line)

# Axis and Title
xticks = ["$2^{" + str(pow) + "}$" for pow in q_pows]
plt.xticks(q_pows,xticks)
plt.xlabel('Adversary Power (q)')
plt.ylabel('Number of Hashes (k)')
plt.title('Minimum Hashes to Beat an Adversary Packing a Bloom Filter')

# Legends
leg1 = plt.legend(handles=data_lines, title='Bloom Filter Elements (m)', loc=2)
plt.legend(handles=k_lines, title='K for Given FP Rate', loc=4)
plt.gca().add_artist(leg1)
plt.tight_layout()
plt.savefig('ks_to_advpower.png')

