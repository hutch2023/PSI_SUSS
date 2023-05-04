import math
import matplotlib.pyplot as plt
import numpy as np

def calc_fp(k):
    x = 1 - pow(math.e, -math.log(2))
    return x ** k

def savings(k):
    return (256 * math.log(2)) / k

ks = np.arange(40,100,10)
ys = list(map(savings, ks))

plt.plot(ks, ys)

# Axis and Title
xticks = ["$2^{-" + str(k) + "}$" for k in ks]
plt.xticks(ks,xticks)
plt.xlabel('False Positive Rate')
plt.ylabel('Improvement Factor')
plt.title('Set K Communication Cost Improvement Using a Bloom Filter')
plt.savefig('pngs/savings.png')
