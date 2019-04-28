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

    def top_cards(conn):
        """
        Query all rows in the colors table
        :param conn: the Connection object
        :return:
        """
        sql = ''' SELECT Name, Number, Colors.Card_ID
                    FROM Colors
                    INNER JOIN Cards
                    ON Colors.Card_ID=Cards.Card_ID
                    WHERE Rarity!='B'
                    ORDER BY Colors.Card_ID'''

        cur = conn.cursor()
        cur.execute(sql)

        rows = cur.fetchall()

        return rows

    def top_cards_specific(conn,color):
        """
        Query all rows in the colors table
        :param conn: the Connection object
        :return:
        """
        test=(color,)
        sql = ''' SELECT Name, Number
                    FROM Colors
                    INNER JOIN Cards
                    ON Colors.Card_ID=Cards.Card_ID
                    WHERE Rarity!='B'
                    AND Color=?
                    ORDER BY Number
                    DESC LIMIT 20'''

        cur = conn.cursor()
        cur.execute(sql,test)

        rows = cur.fetchall()

        return rows
