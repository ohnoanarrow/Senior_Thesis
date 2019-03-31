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


    def archetype_search(conn):
        """
        Query all rows in the colors table
        :param conn: the Connection object
        :return:
        """
        sql = ''' SELECT Name
                  FROM Cards
                  WHERE Archetype='Sideboard''''

        cur = conn.cursor()
        cur.execute(sql,test)

        rows = cur.fetchall()

        return rows


    def archetype_update(conn,test):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        sql = ''' UPDATE Cards
                  SET Archetype=?
                  WHERE Name=?'''

        cur = conn.cursor()
        cur.execute(sql,test)


    def creature_search(conn):
        """
        Query all rows in the colors table
        :param conn: the Connection object
        :return:
        """
        sql = ''' SELECT Name
                  FROM Cards
                  WHERE Archetype='Creature''''

        cur = conn.cursor()
        cur.execute(sql,test)

        rows = cur.fetchall()

        return rows


    def creature_update(conn,test):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        sql = ''' UPDATE Cards
                  SET Power=?,Toughness=?
                  WHERE Name=?'''

        cur = conn.cursor()
        cur.execute(sql,test)
