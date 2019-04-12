import csv
import sqlite3
from top_cards_db import Database
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt; plt.rcdefaults()

def plot_data(rows):
    sns.set(style="whitegrid")

    top_headers=[["name","number"]]
    top_headers += rows

    with open('src/analysis/topcards_file.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(top_headers)

    file = 'src/analysis/topcards_file.csv'
    ufo = pd.read_csv(file)

    g = sns.catplot(x="number", y = "name", data=ufo, kind = "bar", orient="h", aspect=2)
    g.despine(left=True)
    g.savefig('src/analysis/graphs/top_cards.png')

def plot_data_specific(rows,mana_str):
    sns.set(style="whitegrid")

    mana_headers=[["name","number"]]
    mana_headers += rows

    with open('src/analysis/topcards_file.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(mana_headers)

    file = 'src/analysis/topcards_file.csv'
    ufo = pd.read_csv(file)

    g = sns.catplot(x="number", y = "name", data=ufo, kind = "bar", orient="h", aspect=2)
    g.despine(left=True)
    g.savefig(mana_str)

def main():
    db_file = 'databases/MtG.db'
    conn = Database.create_connection(db_file)
    colors=['chaos','mono green','temur','bant']
    with conn:
        rows = Database.top_cards(conn)
        plot_data(rows)
        for color in colors:
            mana_str = 'src/analysis/graphs/top_' + color + '.png'
            rows = Database.top_cards_specific(conn,color)
            plot_data_specific(rows,mana_str)

if __name__ == '__main__':
    main()
