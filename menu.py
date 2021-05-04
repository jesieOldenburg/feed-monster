import os
import re
import math
import urllib.request
import xml.dom.minidom
import xml.etree.ElementTree as ET
import shelve
import pprint
from prettytable import PrettyTable

PT = PrettyTable()

def create_main_menu():        
    os.system('cls' if os.name == 'nt' else 'clear')
    print("1. Display Subscribed Feeds")
    print("2. Input New RSS URL")
    print("3. Delete Feed")
    print("4. Exit")
    print("\n CHOOSE AN OPTION")
    pass

def main_menu_logic():
    create_main_menu()
    menu_selection = input(">> ")
    if menu_selection == "1":
        show_subs(whocall="main_menu")
        pass
    if menu_selection == "2":
        display_rss_url_search_menu()
    if menu_selection == "3":
        unsubscribe_menu()
        pass
    if menu_selection == "4":
        pass

def delete_feed(key):
    """This function will open an instance of the shelve database file and delete the selected key from the dictionary stored on disk

    Args:
        key [dict key]: A dictionary key passed to the function
    """    
    SH = shelve.open('feeds.db', writeback=True)
    feed_dict = SH['feeds']
    # print("FEED DICT IN DEL", key)
    print("FEED DICT KEYY", feed_dict[key])
    del feed_dict[key]
    SH.close()
    print(feed_dict)
    pass

def unsubscribe_menu():
    """A simple function that handles the logic of deleting an item from the Shelve stored dictionary
    """    
    show_subs(whocall="unsubscribe_menu")
    pass

def show_subs(whocall):
    os.system('cls' if os.name == 'nt' else 'clear')
    PT.field_names = ["SEL #", "RSS Feed Name", "RSS URL" ]
    item_nums = 0 

    SH = shelve.open('feeds.db')
    callable_feeds = dict()
    feeds_dict = SH['feeds']

    for feed in feeds_dict.items():
        item_nums += 1
        f_title = feed[0]
        f_link = feed[1]
        
        callable_feeds[str(item_nums)] = f_link
        
        PT.add_row([item_nums, f_title, f_link])
    SH.close()
    
    PT.align = "l"
    PT.align["SEL #"] = "c"
    print(PT)
    
    if whocall == "main_menu":
        print("Type 'main' to return to the main menu")
        print('Which Feed would you like to view?')
        choice = input(">> ")
        if choice.lower() == "main":
            main_menu_logic()
        else:
            url_choice = callable_feeds[choice]
            pull_subbed_RSS(url_choice)

    if whocall == "unsubscribe_menu":
        print('Which Feed would you like to delete?')
        feeds_dict_keys_list = list(feeds_dict)
        
        choice = input(">> ")
        INDEX_MODIFIER = int(choice) - 1
        KEY_TO_DEL = feeds_dict_keys_list[INDEX_MODIFIER] # ! The index of the user choice in the list
        delete_feed(KEY_TO_DEL)
        pass

def display_feeds_table():
    PT.field_names = ["Field Descriptions", "Values", "\n"]
    # print(PT)
    # pass

def create_table_rows(title, desc, link):
    PT.add_row([title, desc, link])

def chunk_list(passed_list, n):
    for i in range(0, len(passed_list), n):
        yield passed_list[i:i + n]

def print_chunks(*args, **kwargs):
    chunk = args[0]
    for item_tag in chunk:
            # PT.clear_rows()
            # Iterate over the tags in the chunk
            article_title = item_tag.find('title').text
            article_description = item_tag.find('description').text
            clean_desc = re.sub("(<img.*?>)", "", article_description, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
            article_URL = item_tag.find('link').text
            link_text = 'Link'
            hyperlink = f"\x1b]8;;{article_URL}\a{link_text}\x1b]8;;\a"

            PT.add_row([f"\033[1m Article Title :: \033[0m", article_title, ""])
            PT.add_row([f"\033[1m Article Description :: \033[0m", clean_desc, ""])
            PT.add_row([f"\033[1m Page Link (CMD/Ctrl + Click) :: \033[0m", hyperlink, "\n"])

def display_articles(f_len, f_list):
    # TODO: If the description tag has other tags within it, i.e. an <h1> tag, parse those tags out with a conditional.
        
    # TODO: Get the len() of the item list and display a limited number of results first, then allow the user to scroll through the table, i.e. enter for next page.
    
    # TODO: Add a value check condition to evaluate if the fields contain values, and what to do if not, such as return a string of "No [field_name] provided"
    chunks = list(chunk_list(f_list, 5))
    PT.border = False
   
    for i, chunk in enumerate(chunks):
        print(i == 0)
        os.system('cls' if os.name == 'nt' else 'clear')
        for item_tag in chunk:
            # Iterate over the tags in the chunk
            article_title = item_tag.find('title').text
            article_description = item_tag.find('description').text
            clean_desc = re.sub("(<img.*?>)", "", article_description, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
            article_URL = item_tag.find('link').text
            link_text = 'Link'
            hyperlink = f"\x1b]8;;{article_URL}\a{link_text}\x1b]8;;\a"

            PT.add_row([f"\033[1m Article Title :: \033[0m", article_title, ""])
            PT.add_row([f"\033[1m Article Description :: \033[0m", clean_desc, ""])
            PT.add_row([f"\033[1m Page Link (CMD/Ctrl + Click) :: \033[0m", hyperlink, "\n"])
        print(PT)
        proceed_prompt = input("Press Enter to Display next 5 results")
        PT.clear_rows()
    PT.border = False
    # TODO Add input() for the user to go back to the feeds menu and choose another feed

def display_rss_url_search_menu():
    # TODO Type check the input as a URL
    # os.system('cls' if os.name == 'nt' else 'clear')
    print("Enter an RSS URL: \n")
    RSS_URL_input = input('>> ') # Don't forget to change this back to regular input (>>) after testing
    get_rss_url(feed_to_search, whocall="url_search") # change this back to this: get_rss_url(RSS_URL_input)
    pass

feed_to_search = "http://rss.cnn.com/rss/edition_world.rss"
# ? 'http://feeds.bbci.co.uk/news/world/rss.xml'
# ? 'http://www.cbn.com/cbnnews/us/feed/'
# ? 'https://thewest.com.au/rss-feeds'
# ? 'https://www.nytimes.com/svc/collections/v1/publish/https://www.nytimes.com/section/world/rss.xml'

def store_data(title, link):
    # Uses shelve to persist data
    SH = shelve.open('feeds.db', writeback=True)
    # print('FEEDS', SH.keys())
    try:
        SH['feeds'][title] = link
    finally:
        SH.close()
    print("URL ADDED SUCCESSFULLY!!")


def parse_XML(xml_str, vURL, whocall):
    # TODO: typecheck the root tag to be <rss>
    root = ET.fromstring(xml_str) # grabs the root tag from the XML response [str], which will always be an RSS tag
    feed_provider = root.find('.//title').text
    feed_link = vURL
    item_tag_list = root.findall('.//item') # Finds all tags named item in the XML response
    feed_length = len(item_tag_list)
    
    if whocall == "url_search":
        print("search called me ")
        store_data(feed_provider, feed_link)
        
        print("Would you like to add another RSS URL?","\n Y/n?")
        choice = input("")
        
        if choice.lower() == 'y':
            display_rss_url_search_menu()
        if choice.lower() == 'n':
            main_menu_logic()

    if whocall == "pull_subs":
        PT.align = 'l'
        display_feeds_table()
        display_articles(feed_length, item_tag_list)
        # print('2... pull subs called me')
        # # TODO: If the description tag has other tags within it, i.e. an <h1> tag, parse those tags out with a conditional.
        
        # # TODO: Get the len() of the item list and display a limited number of results first, then allow the user to scroll through the table, i.e. enter for next page.
        
        # # TODO: Add a value check condition to evaluate if the fields contain values, and what to do if not, such as return a string of "No [field_name] provided"
        
        # FINAL_SLICE = feed_length % 5
        # print(FINAL_SLICE)
        # SLICE_MOD = math.floor(feed_length / 5)
        # print("Slice Mod", SLICE_MOD)
        
        # for item_tag in item_tag_list:
        #     # TODO: Need to eval the length of the tag list, then print 5 results per screen, then the result of (len(list) % 5) will be the value of the last splice operation.
            
        #     article_title = item_tag.find('title').text
        #     article_description = item_tag.find('description').text
        #     clean_desc = re.sub("(<img.*?>)", "", article_description, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        #     article_URL = item_tag.find('link').text
        #     link_text = 'Link'
        #     hyperlink = f"\x1b]8;;{article_URL}\a{link_text}\x1b]8;;\a"

        #     PT.add_row([f"\033[1m Article Title :: \033[0m", article_title, ""])
        #     PT.add_row([f"\033[1m Article Description :: \033[0m", clean_desc, ""])
        #     PT.add_row([f"\033[1m Page Link (CMD/Ctrl + Click) :: \033[0m", hyperlink, "\n"])
        # PT.border = False
        # # PT.header = True
        # print(PT) # ! UNCOMMENT ME
        # # TODO Add input() for the user to go back to the feeds menu and choose another feed


def get_rss_url(feed_url, whocall):
    """This function accepts an RSS feed URL and fetches an XML response. It then formats the response into a string and passes it to a parser function

    Args:
        feed_url (string): A url represented as a string
        whocall (string): A keyword argument used in a logical statement
    """    
    try:
        with urllib.request.urlopen(feed_url) as response:
            xml_response = response.read()
    except:
        print('An exception occurred')
        # print(xml_response, '\n')

    dom = xml.dom.minidom.parseString(xml_response) # Parses the response to a string
    xml_response = dom.toprettyxml() # Prettify the response
    # print(xml_response)
    if whocall == "url_search":
        print("search called me ")
        parse_XML(xml_response, feed_url, whocall="url_search")
        pass
    if whocall == "pull_subs":
        PT.clear_rows()
        parse_XML(xml_response, feed_url, whocall="pull_subs")
    #     pass
    # user_passed_URL = feed_url
    # tree = ET.parse(pretty_xml)
    # print(tree)
    
def pull_subbed_RSS(url):
    os.system('cls' if os.name == 'nt' else 'clear')
    # print('UUAREELLL')
    feed_to_pull = url
    get_rss_url(feed_to_pull, whocall="pull_subs")
    pass