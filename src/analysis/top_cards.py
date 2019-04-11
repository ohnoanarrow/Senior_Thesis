import sqlite3
from top_cards_db import Database

def main():
    db_file = 'databases/MtG.db'
    conn = Database.create_connection(db_file)
    colors=['chaos','mono green','temur','bant']
    with conn:
        rows = Database.top_cards(conn)
#        for color in colors:
#            rows = Database.top_cards_specific(conn,color)

if __name__ == '__main__':
    main()
