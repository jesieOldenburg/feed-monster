import os
import urllib.request
import xml.dom.minidom
import xml.etree.ElementTree as ET
import shelve
import pprint
from prettytable import PrettyTable

PT = PrettyTable()

def create_main_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    # TODO: Write logic for displaying feeds for option 1.
    print("1. Display Subscribed Feeds")
    print("2. Input New RSS URL")
    print("3. Refresh Feeds")
    print("4. Exit")
    print("\nCHOOSE AN OPTION")
    pass

def main_menu_logic():
    create_main_menu()
    menu_selection = input(">> ")
    if menu_selection == "1":
        show_subs()
        pass
    if menu_selection == "2":
        display_rss_url_search_menu()
    pass

def show_subs():
    print("-" * 19 + "Your Subscribed Feeds" + "-" * 19)
    SH = shelve.open('feeds.db')
    feeds_dict = SH['feeds']
    # print(feeds_dict.items())
    PT.field_names = ["SEL #", "RSS Feed Name", "RSS URL" ]
    item_nums = 0 

    callable_feeds = dict()
    
    for feed in feeds_dict.items():
        item_nums += 1
        f_title = feed[0]
        f_link = feed[1]

        callable_feeds[str(item_nums)] = f_link
        
        PT.add_row([item_nums, f_title, f_link])
    SH.close()
        
    print(callable_feeds)
    PT.align = "l"
    PT.align["SEL #"] = "c"
    print(PT)
    print('Which Feed would you like to view?')
    choice = input(">> ")

    if choice == "1":
        url_choice = callable_feeds['2']
        pull_subbed_RSS(url_choice)

def display_feeds_table():
    # TODO Need to try and format my own table. Draw it out first
    PT.field_names = ['Title', 'Description', 'Link']
    # print(PT)
    pass

def create_table_rows(title, desc, link):
    PT.add_row([title, desc, link])
    

def display_rss_url_search_menu():
    # TODO Type check the input as a URL
    # os.system('cls' if os.name == 'nt' else 'clear')
    print("Enter an RSS URL: \n")
    RSS_URL_input = input('>> ') # Don't forget to change this back to regular input (>>) after testing
    get_rss_url(feed_to_search, whocall="url_search") # change this back to this: get_rss_url(RSS_URL_input)
    pass

feed_to_search = 'http://feeds.bbci.co.uk/news/world/rss.xml'
# ? Test Feed URL: 'http://feeds.bbci.co.uk/news/world/rss.xml'
# ? Test Feed URL: 'http://www.cbn.com/cbnnews/us/feed/'
# ? Test Feed URL: 'https://thewest.com.au/rss-feeds'
# ? Test Feed URL: 'https://www.nytimes.com/svc/collections/v1/publish/https://www.nytimes.com/section/world/rss.xml'

def store_data(title, link):
    # Uses shelve to persist data
    SH = shelve.open('feeds.db', writeback=True)
    # print('FEEDS', SH.keys())
    try:
        SH['feeds'][title] = link
        SUBBED_FEEDS = SH['feeds']
    finally:
        SH.close()
    print("URL ADDED SUCCESSFULLY!!")

def parse_XML(xml_str):
    # TODO: typecheck the root tag to be <rss>
    root = ET.fromstring(xml_str) # grabs the root tag from the XML response [str], which will always be an RSS tag
    feed_provider = root.find('.//title').text
    feed_link = root.find('.//link').text
    item_tag_list = root.findall('.//item') # Finds all tags named item in the XML response
    # display_feeds_table()
    # TODO This will need a conditional to see which function called parse_xml. Maybe Fetch RSS feeds need the conditional
    store_data(feed_provider, feed_link)
    # ? Consider creating a function that fetches a few URLs once the program is ran, and loads those into the table.
    for item_tag in item_tag_list[:11]: # limit the results to ten 
        article_title = item_tag.find('title').text
        print('TITLE ==>', article_title[:150])
        article_description = item_tag.find('description').text[:20]
        # print('DESC ==>', article_description)
        article_URL = item_tag.find('link').text
        link_text = 'Link to Article'
        
        hyperlink = f"\x1b]8;;{article_URL}\a{link_text}\x1b]8;;\a"
        # print('LINK ==>', hyperlink)
        create_table_rows(article_title, article_description, hyperlink) # ! This will need to move. TEST ONLY!
    
    # print(PT) # ! UNCOMMENT ME
    display_feeds_table()
    # TODO: Set Timeout Here
    print("Would you like to add another RSS URL?","\nY/n?")
    choice = input("")
    print(type(choice))
    if choice.lower() == 'y':
        display_rss_url_search_menu()
    if choice.lower() == 'n':
        main_menu_logic()

def get_rss_url(feed_url, whocall):
    # TODO: Save the XML response as a var in this function, then call ElementTree.parse() and pass the XML res as an arg
    # This request takes a URL as an argument and opens the url, then parses the response and returns an XML string.
    try:
        with urllib.request.urlopen(feed_url) as response:
            xml_response = response.read()
            # print(xml_response)
    except:
        print('An exception occurred')
        # print(xml_response, '\n')

    dom = xml.dom.minidom.parseString(xml_response) # Parses the response to a string
    xml_response = dom.toprettyxml() # Prettify the response
    if whocall == "url_search":
        print("search called me ")
        parse_XML(xml_response)
        pass
    if whocall == "pull_subs":
        print('pull subs called me')
        # TODO Write logic for pulling the subs
        pass
    # user_passed_URL = feed_url
    # tree = ET.parse(pretty_xml)
    # print(tree)
    
def pull_subbed_RSS(*args, **kwargs):
    print(*args)
    get_rss_url(*args, whocall="pull_subs")
    pass