import csv
import sqlite3
# import leather
# import statsmodels
import numpy as np
import pandas as pd
import seaborn as sns
from top_colors_db import Database
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt; plt.rcdefaults()


sns.set(style="whitegrid")

db_file = 'databases/MtG.db'
conn = Database.create_connection(db_file)

total = 0
count = 1
colors = []
color_rank_array = []
top_colors_array = []


with conn:
    rows = Database.decks_search(conn)
    for row in rows:
        rank = row[1]
        if row[0] not in colors:
            rank_object = [row[0],0,0,0,0]
            rank_object[rank] += 1
            color_rank_array.append(rank_object)
            colors.append(row[0])
        else:
            for elem in range(len(color_rank_array)):
                if row[0] in color_rank_array[elem]:
                    rank_object = color_rank_array[elem]
                    rank_object[rank] += 1
                    color_rank_array[elem] = rank_object


for deck in color_rank_array:
    print(deck)
    total = 0
    for count in range(1,5):
        total += deck[count]
    top_colors_array.append([deck[0],total])

top_colors_array = sorted(top_colors_array, key=lambda x: x[1], reverse=True)

# There are 767 total decks
# There are 32 decks in total

labels = []
sizes = []
count = 0
top_decks = 0
for x in top_colors_array:
    if count < 10:
        labels.append(x[0])
        sizes.append(x[1])
        top_decks += x[1]
        count += 1
    else:
        pass

other_decks = 767-top_decks
labels.append("other")
sizes.append(other_decks)

#add colors
colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
        shadow=True, startangle=90)

# Equal aspect ratio ensures that pie is drawn as a circle
ax1.axis('equal')

plt.tight_layout()
plt.savefig('src/analysis/graphs/Top_Decks_Pie.png')

first = sorted(color_rank_array, key=lambda x: x[1], reverse=True)
second = sorted(color_rank_array, key=lambda x: x[2], reverse=True)
third = sorted(color_rank_array, key=lambda x: x[3], reverse=True)
fourth = sorted(color_rank_array, key=lambda x: x[4], reverse=True)

headers = [["color","count","rank"]]

for x in first[:4]:
    values = []
    for y in x[:2]:
        values.append(y)
    values.append("First")
    headers.append(values)

for x in second[:4]:
    values = []
    for y in range(len(x)):
        if y == 0 or y == 2:
            values.append(x[y])
    values.append("Second")
    headers.append(values)

for x in third[:4]:
    values = []
    for y in range(len(x)):
        if y == 0 or y == 3:
            values.append(x[y])
    values.append("Third")
    headers.append(values)

for x in fourth[:4]:
    values = []
    for y in range(len(x)):
        if y == 0 or y == 4:
            values.append(x[y])
    values.append("Fourth")
    headers.append(values)

with open('src/analysis/rank_file.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(headers)


file = 'src/analysis/rank_file.csv'
ufo = pd.read_csv(file)


g = sns.catplot(x="rank", y = "count", hue="color", data=ufo, kind = "bar", aspect=2)
g.despine(left=True)
#plt.show(g)
g.savefig("src/analysis/graphs/rank.png")
