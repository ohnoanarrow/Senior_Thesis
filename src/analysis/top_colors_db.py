import sys
import sqlite3
from sqlite3 import Error

class Database:
    def create_connection(db_file):
        """ create a database connection to a SQLite database """
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)

        return None

    def decks_search(conn):
        """
        Query all rows in the colors table
        :param conn: the Connection object
        :return:
        """
        sql = ''' SELECT Deck_Color, Rank
                  FROM Decks'''

        cur = conn.cursor()
        cur.execute(sql)

        rows = cur.fetchall()

        return rows
