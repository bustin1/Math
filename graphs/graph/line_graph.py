from matplotlib import pyplot as plt
import numpy as np

plt.xkcd()
#print(plt.style.available)
#plt.style.use('fivethirtyeight')
ages_x = np.arange(25, 36)


# python developers
py_dev_y = [45372, 48876, 53850, 57287, 63016, 65998, 
            70003, 70000, 71496, 75370, 83640]
plt.plot(ages_x, py_dev_y, color='#5a7b9a', marker='o', linewidth='3', label='Python')

# javascript developers
js_dev_y = [37810, 43515, 46823, 49293, 53437,
            56373, 62375, 66674, 68745, 68746, 74583]
plt.plot(ages_x, js_dev_y, color='#adad3b', marker='o', linewidth='3', label='Javascript')

# all developers
dev_y = [38496, 42000, 46752, 49320, 53200, 56000, 
            62316, 64928, 67317, 68748, 73752]
plt.plot(ages_x, dev_y, color='#444444', linestyle='--', marker='.', label='All Devs')# or use format strings

plt.xlabel('Ages')
plt.ylabel('Median Salary (USD)')
plt.title("Median Salary (USD) by Age")

plt.legend()

#plt.grid(True)
plt.tight_layout()
plt.axis('on')
#plt.savefig('plot.png')
plt.show()  
