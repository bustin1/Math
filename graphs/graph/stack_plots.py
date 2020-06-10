from matplotlib import pyplot as plt
import numpy as np

plt.style.use('fivethirtyeight')

minutes = np.arange(1,10)

player1 = [1,2,3,3,4,4,4,4,5]
player2 = [1,1,1,1,2,2,2,3,4]
player3 = [1,1,1,2,2,2,3,3,3]

colors = ['#6d904f', '#fc4f30', '#008fd5']
labels=['Player1', 'Player2', 'Player3']
plt.stackplot(minutes, player1, player2, player3, labels=labels, colors=colors)

plt.legend(loc='upper left')

plt.title('Stack Plots')
plt.tight_layout()
plt.show()