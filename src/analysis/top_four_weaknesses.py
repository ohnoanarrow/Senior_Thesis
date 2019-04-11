import sqlite3
from top_four_weaknesses_db import Database

def find_stronger_decks(conn,color):
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

def main():
    db_file = 'databases/MtG.db'
    conn = Database.create_connection(db_file)
    #colors=['chaos','mono green','temur','bant']
    with conn:
        find_stronger_decks(conn,'chaos')
        #for color in colors:
            #find_stronger_decks(conn,color)

if __name__ == '__main__':
    main()
