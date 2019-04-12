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

    def tourn_rank(conn,color):
        """
        Query all rows in the colors table
        :param conn: the Connection object
        :return:
        """
        test=(color,)
        sql = ''' SELECT Tournament, Rank
                    FROM Decks
                    WHERE Deck_Color=?
                    AND Rank!=1'''

        cur = conn.cursor()
        cur.execute(sql,test)

        rows = cur.fetchall()

        return rows

    def deck_color(conn,test):
        """
        Query all rows in the colors table
        :param conn: the Connection object
        :return:
        """
        sql = ''' SELECT Deck_Color
                    FROM Decks
                    WHERE Tournament=?
                    AND Rank<?'''

        cur = conn.cursor()
        cur.execute(sql,test)

        rows = cur.fetchall()

        return rows
