import os
import urllib.request
import xml.dom.minidom
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
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
    os.system('cls' if os.name == 'nt' else 'clear')
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
        print("F_LINK", f_link)
        callable_feeds[str(item_nums)] = f_link
        
        PT.add_row([item_nums, f_title, f_link])
    SH.close()
        
    # print(callable_feeds)
    PT.align = "l"
    PT.align["SEL #"] = "c"
    print(PT)
    print('Which Feed would you like to view?')
    choice = input(">> ")

    url_choice = callable_feeds[choice]
    pull_subbed_RSS(url_choice)
    # if choice == "1":

def display_feeds_table():
    # TODO Need to try and format my own table. Draw it out first
    PT.field_names = ['Title', 'Description', 'CMD/Ctrl + Click To Open Link']
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

feed_to_search = "https://www.yahoo.com/news/rss/world"
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

def parse_XML(bs, whocall):
    # TODO: typecheck the root tag to be <rss>
    # root = ET.fromstring(xml_str) # grabs the root tag from the XML response [str], which will always be an RSS tag
    root = bs.rss # grabs the root tag from the XML response [str], which will always be an RSS tag
    # print(root)
    # feed_provider = root.find('.//title').text
    feed_provider = root.channel.title.string
    print("feed pro", feed_provider)
    feed_link = root.find('.//link').text
    item_tag_list = root.findall('.//item') # Finds all tags named item in the XML response
    # display_feeds_table()
    if whocall == "url_search":
        print("search called me ")
        store_data(feed_provider, feed_link)
        
        print("Would you like to add another RSS URL?","\nY/n?")
        choice = input("")
        
        if choice.lower() == 'y':
            display_rss_url_search_menu()
        if choice.lower() == 'n':
            main_menu_logic()

    if whocall == "pull_subs":
        PT.align = 'l'
        display_feeds_table()
        # print('2... pull subs called me')

        for item_tag in item_tag_list[:11]: # limit the results to ten 
            article_title = item_tag.find('title').text[:20]
            article_description = item_tag.find('description').text[:20]
            article_URL = item_tag.find('link').text
            link_text = 'Link'
            hyperlink = f"\x1b]8;;{article_URL}\a{link_text}\x1b]8;;\a"
            # print(hyperlink)
            create_table_rows(article_title, article_description, hyperlink)
        print(PT) # ! UNCOMMENT ME
        # TODO Add input() for the user to go back to the feeds menu and choose another feed


def get_rss_url(feed_url, whocall):
    """This function accepts an RSS feed URL and fetches an XML response. It then formats the response into a string and passes it to a parser function

    Args:
        feed_url (string): A url represented as a string
        whocall (string): A keyword argument used in a logical statement
    """    
    try:
        with urllib.request.urlopen(feed_url) as response:
            # print("RESPONSE", response)
            xml_response = response.read()
            soup = BeautifulSoup(xml_response, "lxml")
            # print("CONTENT:: >>", soup.rss)
            # return soup
    except Exception as e:
        print('An exception occurred', e)

    # parser = ET.XMLParser(encoding="utf-8")
    # dom = xml.dom.minidom.parseString(xml_response) # Parses the response to a string
    # print(type(dom))
    # xml_data = ET.fromstring(xml_response, parser=parser)  # Prettify the response
    # print('SOUP', soup)
    # root = xml_data.root()
    # print('XML', xml_data)
    if whocall == "url_search":
        print("search called me ")
        parse_XML(soup, whocall="url_search")
        pass
    if whocall == "pull_subs":
        PT.clear_rows()
        # parse_XML(soup, whocall="pull_subs")
    #     # TODO Write logic for pulling the subs
    #     pass
    # user_passed_URL = feed_url
    # tree = ET.parse(pretty_xml)
    # print(tree)
    
def pull_subbed_RSS(url):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(url)
    get_rss_url(url, whocall="pull_subs")
    pass