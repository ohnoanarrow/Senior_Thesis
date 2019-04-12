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

    def man_arch(conn,color):
        """
        Query all rows in the colors table
        :param conn: the Connection object
        :return:
        """
        arch = 'Land'
        test = (arch,color)
        sql = ''' SELECT Color, Number, Mana_Cost, Archetype
                    FROM Colors
                    INNER JOIN Cards
                    ON Colors.Card_ID=Cards.Card_ID
                    WHERE Archetype !=?
                    AND Color=?'''

        cur = conn.cursor()
        cur.execute(sql,test)

        rows = cur.fetchall()

        return rows

    def deck_count(conn,color):
        """
        Query all rows in the colors table
        :param conn: the Connection object
        :return:
        """
        test = (color,)
        sql = ''' SELECT count(*)
                    FROM Decks
                    WHERE Deck_Color=?'''

        cur = conn.cursor()
        cur.execute(sql,test)

        rows = cur.fetchall()

        return rows
