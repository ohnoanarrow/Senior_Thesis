import requests
import re
import sqlite3
from itertools import cycle
from bs4 import BeautifulSoup
from query_db import Database

def sideboard_parser(conn,rows):
    # Run card name through

def creature_parser(conn,rows):

def main():
    db_file = "databases/MtG.db"
    conn = Database.create_connection(db_file)

    rows = Database.archetype_search(conn)
    sideboard_parser(conn,rows)

    rows = Database.creature_search()
    creature_parser(conn,rows)

if __name__ == '__main__':
    main()
