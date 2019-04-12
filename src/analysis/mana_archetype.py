import sqlite3
from mana_archetype_db import Database

def mana_and_archetype(rows):
    # Rows in this order: Color Number Mana_Cost Archetype
    mana_array = []
    arch_array = []
    for row in rows:
        color = row[0]
        number = row[1]
        cost = row[2]
        archetype = row[3]
        # The following lines check to see if both the color and mana cost are
        # in an item in the 2d array
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

    mana_array = sorted(mana_array, key=lambda x: x[2], reverse=False)

def main():
    db_file = 'databases/MtG.db'
    conn = Database.create_connection(db_file)
    #colors=['chaos','mono green','temur','bant']
    with conn:
        rows = Database.man_arch(conn,'chaos')
        mana_and_archetype(rows)
#        for color in colors:
#            rows = Database.man_arch(conn,color)
#            mana_and_archetype(rows)

if __name__ == '__main__':
    main()
