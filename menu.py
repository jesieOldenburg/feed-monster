import os

def create_main_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    # print('+' + '-++' *16 + '-+')
    # print('|  K  e  a  h  u  a    A  r  b  o  r  e  t  u  m  |' )
    # print('+' + '-++' *16 + '-+\n')
    # print(f'+{'-++' * 16}-+')
    # TODO: Logic for searching for URL Feeds
    print("1. Display Subscribed Feeds") 

    # TODO: Write logic for displaying feeds for option 1.
        # * Need a function to build the menu for this option. This menu should display an option to input a URL, as well as a prompt
    print("2. Input New RSS URL")
    # print("3. Feed Animal")
    # print("4. Cultivate New Plant")
    # print("5. Show Arboretum Report")
    print("3. Exit\n")
    print("CHOOSE AN OPTION")
    pass

def main_menu_logic():
    create_main_menu()
    menu_selection = input(">> ")
    # TODO: Write some if statements to determine the function to be called based off of the menu choice.
    # TODO: Write the functions that handle the menu choices in a separate module.
    if menu_selection == 1: pass
    if menu_selection == 2: pass
    pass

def display_feeds_table():
    pass

def rss_url_search_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    pass