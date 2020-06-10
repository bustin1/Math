import csv
import numpy as np
import pandas as pd # read the csv file
from matplotlib import pyplot as plt
from collections import Counter # count the dictionary


plt.style.use('fivethirtyeight')


''' How to Read using context managers '''
# with open('../data/data.csv') as csv_file:
#     csv_reader = csv.DictReader(csv_file)
# language_counter = Counter()
# for row in csv_reader:
#     language_counter.update(row['LanguagesWorkedWith'].split(';'))

    
data = pd.read_csv('../data/data.csv')
ids = data['Responder_id']
lang_responses = data['LanguagesWorkedWith']

language_counter = Counter()
for response in lang_responses:
    language_counter.update(response.split(';'))

#print(language_counter)

languages = []
popularity = []
for item in language_counter.most_common(15):
    languages.append(item[0])
    popularity.append(item[1])

# or use all = list(zip(*language_counter))
# and the language = all[0], popularity = all[1]



languages.reverse()
popularity.reverse()


# change the font size settings dynamically
plt.rc('font', size=8)
plt.barh(languages, popularity, height=.25)

plt.title('Most Popular Languages')
# plt.xlabel('# of People who use')
plt.ylabel('Programming Languages', fontsize=10)

plt.tight_layout()

plt.show()
