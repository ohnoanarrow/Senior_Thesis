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

    def colors_search(conn,color,card_ID):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        cur = conn.cursor()
        cur.execute("SELECT {clr} FROM Colors WHERE {clr} = {color}")

        rows = cur.fetchall()

        return rows

    def sideboard_search(conn,SB_color,card_ID):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        cur = conn.cursor()
        cur.execute("SELECT * FROM Sideboard")

        rows = cur.fetchall()

        return rows



    def create_cards(conn, test):
        """
        Create a new project into the projects table
        :param conn:
        :param test:
        :return: test id
        """
        sql = ''' INSERT INTO Cards(Card_ID,Name,Mana_Cost,Card_Color,Rarity,Archetype,Power,Toughness)
                  VALUES(?,?,?,?,?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, test)
        return cur.lastrowid

    def create_colors(conn,test):
        """
        Create a new project into the projects table
        :param conn:
        :param test:
        :return: test id
        """
        sql = ''' INSERT INTO Colors(Color,Card_ID,Number)
                  VALUES(?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, test)
        return cur.lastrowid

    def create_decks(conn,test):
        """
        Create a new project into the projects table
        :param conn:
        :param test:
        :return: test id
        """
        sql = ''' INSERT INTO Test(Tournament,Rank,Deck_Color,SB_Color)
                  VALUES(?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, test)
        return cur.lastrowid

    def create_sideboard(conn,test):
        """
        Create a new project into the projects table
        :param conn:
        :param test:
        :return: test id
        """
        sql = ''' INSERT INTO Test(SB_Color,Card_ID,Number)
                  VALUES(?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, test)
        return cur.lastrowid

    #def main():
        # create a database connection
    #    conn = create_connection("databases/MtG.db")
    #    with conn:
            # create a new project
    #        test_1 = ('Cathy', 22, 'F')
    #        test_2 = ('Paul', 80, 'M')
    #        create_test(conn, test_1)
    #        create_test(conn, test_2)

    #    conn.close()

    #if __name__ == '__main__':
    #    main()
