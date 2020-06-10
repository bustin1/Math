from matplotlib import pyplot as plt
import numpy as np

data = np.linspace(0, 2*np.pi)
print(data)



''' use of context manager to draw dark background'''
with plt.style.context('dark_background'):
    plt.plot(data, np.sin(data), 'r-o')
plt.show()