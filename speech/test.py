import numpy as np

count = 0
for i in range(10000):
    c = np.random.rand()
    d = np.random.rand()
    if int(c/d) % 2 == 0:
        count += 1

print(count/10000)
