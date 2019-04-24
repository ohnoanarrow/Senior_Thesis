import csv
import sqlite3
from top_four_weaknesses_db import Database
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt; plt.rcdefaults()


def find_stronger_decks(conn,color):
    sns.set(style="whitegrid")

    with conn:
        color_ref = []
        tournament_rank = Database.tourn_rank(conn,color)
        for pair in tournament_rank:
            dc = Database.deck_color(conn,pair)
            for deck in dc:
                if any(deck[0] in refs for refs in color_ref):
                    for i in range(len(color_ref)):
                        if deck[0] in color_ref[i]:
                            color_ref[i][1] += 1
                else:
                    color_ref.append([deck[0],1])
        color_ref = sorted(color_ref, key=lambda x: x[1], reverse=True)
        color_str = 'src/analysis/graphs/top_four_' + color + '.png'

    color_headers = [["color","number"]]
    color_headers += color_ref
    color_final = []

    for i in range(0,6):
        color_final.append(color_headers[i])
        print(color_headers[i])

    with open('src/analysis/top_four_file.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(color_final)

    file = 'src/analysis/top_four_file.csv'
    ufo = pd.read_csv(file)

    g = sns.catplot(x="color", y = "number", data=ufo, kind = "bar", aspect=2)
    g.despine(left=True)
    g.savefig(color_str)


def main():
    db_file = 'databases/MtG.db'
    conn = Database.create_connection(db_file)
    colors=['chaos','mono green','temur','bant']
    with conn:
        for color in colors:
            find_stronger_decks(conn,color)

if __name__ == '__main__':
    main()
