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

def create_test(conn, test):
    """
    Create a new project into the projects table
    :param conn:
    :param test:
    :return: test id
    """
    sql = ''' INSERT INTO Test(Name,Age,Gender)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, test)
    return cur.lastrowid

def main():
    # create a database connection
    conn = create_connection(sys.argv[1])
    with conn:
        # create a new project
        test_1 = ('Cathy', 22, 'F')
        test_2 = ('Paul', 80, 'M')
        create_test(conn, test_1)
        create_test(conn, test_2)

    conn.close()

if __name__ == '__main__':
    main()
