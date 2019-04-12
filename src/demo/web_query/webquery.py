import requests
import re
import sqlite3
from itertools import cycle
from bs4 import BeautifulSoup
from bs4 import NavigableString
from query_db import Database
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


def navigate_website(row):
    driver = webdriver.Firefox()
    driver.implicitly_wait(5)
    driver.get('https://www.cardkingdom.com/')

    search_bar = driver.find_element_by_xpath("//*[@id='tags']")
    search_bar.clear()
    search_bar.send_keys(row)
    search_bar.send_keys(Keys.RETURN)

    try:
        nextlink = driver.find_element_by_link_text(row)
        nextlink.click()
        url = driver.current_url
        driver.close()
        return url
    except NoSuchElementException as exception:
        print("Card not found: ",row)
        driver.close()
        return None



def sideboard_update(conn, url, row):
    typelist = ["Creature", "Artifact", "Instant", "Sorcery", "Enchantment", "Planeswalker", "Land"]
    archetype = ""
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    for x in soup.find_all('tr'):
        for y in  x.find_all('td',string=True):
            for z in typelist:
                if z in y.string:
                    archetype = z

    with conn:
        arch_test = (archetype,row)
        Database.archetype_update(conn,arch_test)


def creature_update(conn, url, row):
    power = -1
    toughness = -1

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    for x in soup.find_all('tr'):
        for y in  x.find_all('td',string=True):
            if re.search("[a-zA-Z]",y.string):
                pass
            else:
                pt = y.string
                pt_list = pt.split("/")
                try:
                    power = int(pt_list[0])
                except ValueError:
                    power = None
                    pass
                try:
                    toughness = int(pt_list[1])
                except ValueError:
                    toughness = None
                    pass

    with conn:
        test_creature = (power,toughness,row)
        Database.creature_update(conn,test_creature)


def main():
    db_file = 'databases/Backup.db'
    conn = Database.create_connection(db_file)
    with conn:
        rows = Database.archetype_search(conn)
        for row in rows:
            url = navigate_website(row[0])
            if url is not None:
                sideboard_update(conn,url,row[0])
            else:
                pass

        rows = Database.creature_search(conn)
        for row in rows:
            url = navigate_website(row[0])
            if url is not None:
                creature_update(conn, url, row[0])
            else:
                pass

if __name__ == '__main__':
    main()
