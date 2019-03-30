# import statements
# from urllib.request import urlopen
# import mechanize
import requests
import re
import sqlite3
from itertools import cycle
from bs4 import BeautifulSoup
from db_test import Database

db_file = "databases/MtG.db"
conn = Database.create_connection(db_file)

color_dictionary = {
    "u": "mono blue",
    "w": "mono white",
    "g": "mono green",
    "r": "mono red",
    "b": "mono black",
    "uw": "azorius",
    "bu": "dimir",
    "br": "rakdos",
    "gr": "gruul",
    "gw": "selesnya",
    "bw": "orzhov",
    "ru": "izzet",
    "bg": "golgari",
    "rw": "boros",
    "gu": "simic",
    "bgr": "jund",
    "guw": "bant",
    "bru": "grixis",
    "grw": "naya",
    "buw": "esper",
    "ruw": "jeskai",
    "brw": "mardu",
    "bgu": "sultai",
    "gru": "temur",
    "bgw": "abzan",
    "bgru": "chaos",
    "bgrw": "aggression",
    "bguw": "growth",
    "bruw": "artifice",
    "gruw": "altruism",
    "bgruw": "rainbow"
}

typelist = ["\nCreature ", "\nArtifact ", "\nInstant ", "\nSorcery ", "\nEnchantment ", "\nPlaneswalker ", "\nLand ", "\nSideboard "]

tourn_num = 0
card_ID = 1
cards = []

def PageParser(page_number):
    """ This function iterates through the tournament pages and grabs tournament hrefs """
    """ It also feeds the tournament number and tournament href into the DeckParser function"""

    # specify the url
    quote_page = 'https://mtgdecks.net/Modern/tournaments/page:' + page_number
    # query the website and return the html to the variable page
    page = requests.get(quote_page)
    # parse the html using beautiful soup and store in variable soup
    soup = BeautifulSoup(page.text, 'html.parser')

    str= r"[\x2D]"

    counter = 0
    for link in soup.find_all('a', attrs={'href':re.compile(str)}):
        if counter > 0 and counter <= 1 and link.get('href') is not None: #TODO Change this back to 20
            decks_page = 'https://mtgdecks.net/' + link.get('href')
            page = requests.get(decks_page)
            soupy = BeautifulSoup(page.text, 'html.parser')
            global tourn_num
            tourn_num += 1
            DeckParser(tourn_num, soupy)
        counter += 1

def DeckParser(tourn_num, soup):
    """ This function iterates through the decks and finds their color"""
    """ It also feeds the deck color, tournament number, deck rank, and deck href
    into the CardParser function"""

    # Grab the HREFS for the top 4 decks
    counter = 0
    first = ""
    second = ""
    third = ""
    fourth = ""

    for deck in soup.find_all('a', attrs={'href':re.compile("decklist")}):
        if deck.get('href') is not None:
            if counter == 1:
                first = deck.get('href')
            elif counter == 2:
                second = deck.get('href')
            elif counter == 3:
                third = deck.get('href')
            elif counter == 4:
                fourth = deck.get('href')
        counter += 1

    # Isolating the top 4 decks
    none_counter = 0
    rank_counter = 1

    for tag in soup.find_all('tr'):
        placeholder_string = ""
        color_string = ""

        # sb_color_string = ""
        # The strong tag will first come up with deck ranking
        if tag.strong is None:
            none_counter += 1
        # This is where we pull the top 4 decks
        if none_counter > 0 and none_counter < 2 and rank_counter <= 4:
            # Making sure there is a value under the strong tag
            if tag.strong is not None:
                color = tag.find('div', attrs={'class':"small"})
                for x in color.contents:
                    color = x.get('class')
                    if color[0] != 'small-icon':
                        # Saves the color in a placeholder so I can manipulate the string contents
                        placeholder_string = color[2]
                        # Concatenating the single letter indicating color onto the color string
                        color_string += placeholder_string[3]
                # Sorting the letters in alphabetical order for dictionary reference
                color_string_sorter = sorted(color_string)
                color_string = ''.join(color_string_sorter)
                deck_color = color_dictionary.get(color_string)

                # Making my soup based on which deck I'm looking at
                if rank_counter == 1:
                    cards_page = 'https://mtgdecks.net' + first
                    page = requests.get(cards_page)
                    soupy = BeautifulSoup(page.text, 'html.parser')
                elif rank_counter == 2:
                    cards_page = 'https://mtgdecks.net' + second
                    page = requests.get(cards_page)
                    soupy = BeautifulSoup(page.text, 'html.parser')
                elif rank_counter == 3:
                    cards_page = 'https://mtgdecks.net' + third
                    page = requests.get(cards_page)
                    soupy = BeautifulSoup(page.text, 'html.parser')
                elif rank_counter == 4:
                    cards_page = 'https://mtgdecks.net' + fourth
                    page = requests.get(cards_page)
                    soupy = BeautifulSoup(page.text, 'html.parser')

                CardParser(tourn_num, rank_counter, deck_color, soupy)

                rank_counter += 1

def CardParser(tourn_num, rank, deck_color, soup):
    global cards
    global card_ID
    global conn

    str = re.compile("[0-9]")

    soup2 = soup.find('div', attrs={'class':"cards"})
    archetype = ""
    cardname = ""
    number = -1
    rarity = ""
    mana_cost = 0
    card_color = ""
    sb_color = ""
    sb_tracker = []
    cardCheck = True

    # Each table corresponds to a new archetype
    for arch in soup2.find_all('table'):
        for arch2 in arch.find_all('tr'):
            # Finding the archetype class
            string_finder = arch2.get('class')
            # If they found no class
            if string_finder is None:
                # Text children
                for x in arch2.descendants:
                    global typelist
                    length = len(x) - 1
                    # For finding archetypes
                    if x in typelist:
                        archetype = x
                        archetype = archetype[1:length]

            # Individual cards
            elif string_finder[0] == 'cardItem':
                # For each attribute that we're looking for
                for attrs in arch2.find_all('td'):
                    # This will get us either the number or the mana
                    card_chars = attrs.get('class')
                    position = len(card_chars) - 1
                    if card_chars[position] == 'number':
                        rarity_class = attrs.find('span')
                        rarity_letter = rarity_class.get('class')
                        rarity = rarity_letter[1]

                        qualities = attrs.get_text(strip=True)
                        number = int(qualities[:1])
                        cardname = qualities[1:]

                        if cardname not in cards:
                            cardCheck = False
                            cards.append(cardname)
                        else:
                            cardCheck = True

                    elif card_chars[position] == 'manaCost':
                        # If the current card isn't catalogued
                        mana_cost = 0
                        card_color = ""
                        if cardCheck is False:
                            for mana in attrs.find_all('span'):
                                mana_list = mana.get('class')
                                if mana_list[1] == 'ms-cost':
                                    mana_type = mana_list[2]
                                    mt = mana_type[3:]
                                    if re.search("[a-z]", mt):
                                        # Creating the card color string
                                        if mt not in card_color:
                                            card_color += mt
                                        mana_cost += 1
                                    else:
                                        mana_cost += int(mt)
                                else:
                                    mana_type = mana_list[1]
                                    mt = mana_type[3:]
                                    if mt not in card_color:
                                        card_color += mt
                                    mana_cost += 1

                            color_string_sorter = sorted(card_color)
                            card_color = ''.join(color_string_sorter)

                            if archetype == 'Sideboard':
                                sb_color += card_color

                                sb_tracker.append([card_ID, number])

                                if cardCheck == False:
                                    with conn:
                                        cards_db = (card_ID,cardname,mana_cost,card_color,rarity,None,None,None)
                                        Database.create_cards(conn,cards_db)
                                    card_ID += 1
                            else:
                                if cardCheck == False:
                                    with conn:
                                        cards_db = (card_ID,cardname,mana_cost,card_color,rarity,archetype,None,None)
                                        colors_db = (deck_color,card_ID,number)
                                        Database.create_cards(conn,cards_db)
                                        Database.create_colors(conn, colors_db)

                                    card_ID += 1

                        else:
                            if archetype != 'Sideboard':
                                with conn:
                                    temp_ID = Database.cards_search(conn,cardname)
                                    temp_Number = Database.colors_search(conn,deck_color,temp_ID[0])
                                    if temp_Number is not None:
                                        temp_Number = int(temp_Number[0])
                                        number += temp_Number
                                        Database.colors_update(conn,temp_ID[0],number)
                                    else:
                                        colors_db = (deck_color,temp_ID[0],number)
                                        Database.create_colors(conn,colors_db)

    sb_string_sorter = sorted(sb_color)
    sb_color = ''.join(set(sb_string_sorter))
    for y in sb_tracker:
        with conn:
            temp_ID = y[0]
            temp_Number = Database.sideboard_search(conn,sb_color,temp_ID)
            if temp_Number is not None:
                temp_Number = int(temp_Number)
                number = int(y[1]) + temp_Number
                Database.sideboard_update(conn,temp_ID,number)
            else:
                sideboard_db = (sb_color,temp_ID,y[1])
                Database.create_sideboard(conn,sideboard_db)

    with conn:
        decks_db = (tourn_num,rank,deck_color,sb_color)
        Database.create_decks(conn,decks_db)

def main():
    i = 1

    # TODO Change this back to go through all the pages
    # for i in range(1,3):
    PageParser(str(i))

if __name__ == '__main__':
    main()
