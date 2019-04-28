import csv
import sqlite3
from mana_archetype_db import Database
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt; plt.rcdefaults()


def mana_and_archetype(rows,color_number):
    sns.set(style="whitegrid")
    # Rows in this order: Color Number Mana_Cost Archetype
    mana_array = []
    arch_array = []
    rare_array = []
    color_array = []
    for row in rows:
        color = row[0]
        number = row[1]
        cost = row[2]
        archetype = row[3]
        rarity = row[4]
        cardcol = row[5]
        # The following lines check to see if both the color and mana cost are
        # in an item in the 2d array
        if archetype != 'Land':
            if len(mana_array) == 0:
                mana_array.append([color,number,cost])

            else:
                count = 0
                for i in range(len(mana_array)):
                    if color in mana_array[i]:
                        if cost in mana_array[i]:
                            mana_array[i][1] += number
                            count += 1

                if count == 0:
                    mana_array.append([color,number,cost])

            if len(color_array) == 0:
                color_array.append([color,number,cardcol])

            else:
                count = 0
                for i in range(len(color_array)):
                    if color in color_array[i]:
                        if cardcol in color_array[i]:
                            color_array[i][1] += number
                            count += 1

                if count == 0:
                    color_array.append([color,number,cardcol])

        if len(arch_array) == 0:
            arch_array.append([color,number,archetype])

        else:
            count = 0
            for i in range(len(arch_array)):
                if color in arch_array[i]:
                    if archetype in arch_array[i]:
                        arch_array[i][1] += number
                        count += 1

            if count == 0:
                arch_array.append([color,number,archetype])

        if len(rare_array) == 0:
            rare_array.append([color,number,rarity])

        else:
            count = 0
            for i in range(len(rare_array)):
                if color in rare_array[i]:
                    if rarity in rare_array[i]:
                        rare_array[i][1] += number
                        count += 1

            if count == 0:
                rare_array.append([color,number,rarity])

    mana_array = sorted(mana_array, key=lambda x: x[2], reverse=False)

    temp_array = []
    for man in mana_array:
        for x in range(man[1]):
            temp_array.append(man[2])

    print(color," Std, mean, median, mode:",np.std(temp_array),np.mean(temp_array),np.median(temp_array),stats.mode(temp_array))

    # Takes the average of all cards so as to get a sensible curve.
    for j in range(len(mana_array)):
        mana_array[j][1] /= color_number

    plot_results(mana_array,arch_array,rare_array,color_array,row[0])


def plot_results(mana_array,arch_array,rare_array,color_array,color):
    mana_str = 'src/analysis/graphs/mana_' + color + '.png'
    arch_str = 'src/analysis/graphs/arch_' + color + '.png'
    rare_str = 'src/analysis/graphs/rare_' + color + '.png'
    color_str = 'src/analysis/graphs/color_' + color + '.png'
    mana_headers = [["color","number","cost"]]
    mana_headers += mana_array

    labels = []
    sizes = []
    for arc in arch_array:
        labels.append(arc[2])
        sizes.append(arc[1])


    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=90)

    # Equal aspect ratio ensures that pie is drawn as a circle
    ax1.axis('equal')

    plt.tight_layout()
    plt.savefig(arch_str)

    with open('src/analysis/mana_file.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(mana_headers)

    file = 'src/analysis/mana_file.csv'
    ufo = pd.read_csv(file)

    g = sns.catplot(x="cost", y = "number", hue="color", data=ufo, kind = "bar", aspect=2)
    g.despine(left=True)
    g.savefig(mana_str)


    rare_labels = []
    rare_sizes = []
    for rar in rare_array:
        rare_labels.append(rar[2])
        rare_sizes.append(rar[1])

    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']

    fig2, ax2 = plt.subplots()
    ax2.pie(rare_sizes, labels=rare_labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=90)

    # Equal aspect ratio ensures that pie is drawn as a circle
    ax2.axis('equal')

    plt.tight_layout()
    plt.savefig(rare_str)

    color_labels = []
    color_sizes = []
    for col in color_array:
        color_labels.append(col[2])
        color_sizes.append(col[1])

    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']

    fig2, ax2 = plt.subplots()
    ax2.pie(color_sizes, labels=color_labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=90)

    # Equal aspect ratio ensures that pie is drawn as a circle
    ax2.axis('equal')

    plt.tight_layout()
    plt.savefig(color_str)


def main():
    db_file = 'databases/MtG.db'
    conn = Database.create_connection(db_file)
    colors=['chaos','mono green','temur','bant']
    with conn:
        for color in colors:
            rows = Database.man_arch(conn,color)
            color_number = Database.deck_count(conn,color)
            mana_and_archetype(rows,color_number[0][0])

if __name__ == '__main__':
    main()
