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

    def pow_tough_color(conn,color):
        """
        Query all rows in the colors table
        :param conn: the Connection object
        :return:
        """
        creature = 'Creature'
        test = (color,creature)
        sql = ''' SELECT Power, Toughness
                    FROM Cards
                    INNER JOIN Colors
                    ON Colors.Card_ID=Cards.Card_ID
                    WHERE Color=?
                    AND Archetype=?'''

        cur = conn.cursor()
        cur.execute(sql,test)

        rows = cur.fetchall()

        return rows
