from matplotlib import pyplot as plt
import pandas as pd
from collections import Counter

# plt.xkcd()
plt.style.use('fivethirtyeight')

data = pd.read_csv('../data/data.csv')
language_counter = Counter()
for response in data['LanguagesWorkedWith']:
    language_counter.update(response.split(';'))


labels, values = list(zip(*language_counter.most_common(5)))
explode = [0, 0, 0, 0.1, 0]

plt.pie(values, explode=explode, shadow=True, startangle=90, autopct='%1.1f%%', labels=labels, wedgeprops={'edgecolor': 'black'})


plt.title('Pie Charts')
plt.tight_layout()
plt.show()

#colors = ['#008fd5', '#fc4f30', '#e5ae37', '#6d904f']
