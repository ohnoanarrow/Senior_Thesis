import csv
import sqlite3
from pow_tough_db import Database
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt; plt.rcdefaults()

def plot_data(rows,color):
    sns.set(style="whitegrid")

    mana_str = 'src/analysis/graphs/pow_tough_' + color + '.png'

    pt_headers=[["power","toughness"]]
    pt_headers += rows

    with open('src/analysis/pow_tough_file.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(pt_headers)

    file = 'src/analysis/pow_tough_file.csv'
    ufo = pd.read_csv(file)


    g = sns.scatterplot(x="power", y = "toughness", palette="ch:r=-.2,d=.3_r", data=ufo)
    fig = g.get_figure()
    fig.savefig(mana_str)

def main():
    db_file = 'databases/MtG.db'
    conn = Database.create_connection(db_file)
    colors=['chaos','mono green','temur','bant']
    with conn:
        for color in colors:
            rows = Database.pow_tough_color(conn,color)
            plot_data(rows,color)

if __name__ == '__main__':
    main()
