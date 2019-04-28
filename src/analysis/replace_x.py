import sys
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

def get_x(conn):
    """
    Query all rows in the colors table
    :param conn: the Connection object
    :return:
    """
    test=('%x%',)
    sql = ''' SELECT Card_ID, Card_Color
                FROM Cards
                WHERE Card_Color
                LIKE ?'''

    cur = conn.cursor()
    cur.execute(sql,test)

    rows = cur.fetchall()

    return rows

def update_x(conn,test):
    """
    Query all rows in the colors table
    :param conn: the Connection object
    :return:
    """
    sql = ''' UPDATE Cards
                SET Card_Color=?
                WHERE Card_ID=?'''

    cur = conn.cursor()
    cur.execute(sql,test)


def color_updater(conn):
    with conn:
        rows = get_x(conn)
        for row in rows:
            newcolor = row[1].replace('x','')
            test = (newcolor,row[0])
            update_x(conn,test)

def main():
    db_file = 'databases/MtG.db'
    conn = create_connection(db_file)
    with conn:
        color_updater(conn)

if __name__ == '__main__':
    main()
