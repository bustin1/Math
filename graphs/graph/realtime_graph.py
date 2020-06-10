import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')

# x_vals = []
# y_vals = []

#plt.plot(x_vals, y_vals)


# index = count() # just keeps a counter

# def animate(i):
#     # x_vals.append(next(index))
#     # y_vals.append(random.randint(0, 5))
#     data = pd.read_csv('../data/data5.csv')
#     x = data['x_value']
#     y1 = data['total_1']
#     y2 = data['total_2']

#     plt.cla()

#     plt.plot(x,y1, label='Channel 1') # possible 
#     plt.plot(x,y2, label='Channel 2')

#     plt.legend(loc='upper left')
#     plt.tight_layout()

plt.plot([], [], label='Channel 1')
plt.plot([], [], label='Channel 2')

def animate(i):
    data = pd.read_csv('../data/data5.csv')
    x = data['x_value']
    y1 = data['total_1']
    y2 = data['total_2']

    ax = plt.gca()
    line1, line2 = ax.lines

    line1.set_data(x, y1)
    line2.set_data(x, y2)

    xlim_low, xlim_high = ax.get_xlim()
    ylim_low, ylim_high = ax.get_ylim()

    ax.set_xlim(xlim_low, (x.max() + 5))

    y1max = y1.max()
    y2max = y2.max()
    current_ymax = y1max if (y1max > y2max) else y2max

    y1min = y1.min()
    y2min = y2.min()
    current_ymin = y1min if (y1min < y2min) else y2min

    ax.set_ylim((current_ymin - 5), (current_ymax + 5))
    
# if need to animate once in beginning, use init func
ani = FuncAnimation(plt.gcf(), animate, interval=1000)

plt.tight_layout()
plt.show()


