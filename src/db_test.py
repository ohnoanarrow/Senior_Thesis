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


    def cards_search(conn,cardname):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        name = (cardname,)
        sql = ''' SELECT Card_ID
                  FROM Cards
                  WHERE Name=?'''

        cur = conn.cursor()
        cur.execute(sql,name)

        ID = cur.fetchall()

        if not ID:
            return None
        else:
            return ID[0]


    def colors_search(conn,deck_color,card_ID):
        """
        Query all rows in the colors table
        :param conn: the Connection object
        :return:
        """
        test = (deck_color,card_ID)
        sql = ''' SELECT Number
                  FROM Colors
                  WHERE Color=?
                  AND Card_ID=?'''

        cur = conn.cursor()
        cur.execute(sql,test)

        number = cur.fetchall()

        if not number:
            return None
        else:
            return number[0]

    def sideboard_search(conn,sb_color,card_ID):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        test = (sb_color,card_ID)
        sql = ''' SELECT Number
                  FROM Sideboard
                  WHERE SB_Color=?
                  AND Card_ID=?'''

        cur = conn.cursor()
        cur.execute(sql,test)

        number = cur.fetchall()

        if not number:
            return None
        else:
            return number[0]

    def colors_update(conn,card_ID,number):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        test=(number,card_ID)
        sql = ''' UPDATE Colors
                  SET Number=?
                  WHERE Card_ID=?'''

        cur = conn.cursor()
        cur.execute(sql,test)


    def sideboard_update(conn,card_ID,number):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        test=(number,card_ID)
        sql = ''' UPDATE Sideboard
                  SET Number=?
                  WHERE Card_ID=?'''

        cur = conn.cursor()
        cur.execute(sql,test)


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
        sql = ''' INSERT INTO Decks(Tournament,Rank,Deck_Color,SB_Color)
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
        sql = ''' INSERT INTO Sideboard(SB_Color,Card_ID,Number)
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
