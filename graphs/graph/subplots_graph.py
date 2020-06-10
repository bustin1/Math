import pandas as pd
from matplotlib import pyplot as plt

plt.style.use('seaborn')

data = pd.read_csv('../data/data6.csv')
ages = data['Age']
dev_salaries = data['All_Devs']
py_salaries = data['Python']
js_salaries = data['JavaScript']

# stateful, comes with single axes and single figure object
# one figure can have multiple plots. ax is a subplot object
# fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True)

fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()

# print(fig)


ax1.plot(ages, dev_salaries, color='#444444',
         linestyle='--', label='All Devs')

ax2.plot(ages, py_salaries, label='Python')
#L = [5,11,3,50,60,90]
ax2.plot(ages, js_salaries, label='JavaScript')


ax1.legend()
ax1.set_title('Median Salary (USD) by Age')
# ax1.set_xlabel('Ages')
ax1.set_ylabel('Median Salary (USD)')

ax2.legend()
# ax2.set_title('Median Salary (USD) by Age')
ax2.set_xlabel('Ages')
ax2.set_ylabel('Median Salary (USD)')


# pyplot object
plt.tight_layout()

plt.show()

# fig1.savefig('jfdlsa')
