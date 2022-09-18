from threading import Thread
import web_request as web
from bs4 import BeautifulSoup
import urllib.parse

# Get all search results from a card
def GetSearchCardURLs(name):
    # Create the URL for the YuGiOh card you are looking for and load the website
    search_url = f"https://www.cardmarket.com/de/YuGiOh/Products/Search?searchString={urllib.parse.quote(name)}"
    search_request = web.Get_Webpage(search_url)
    search_page = BeautifulSoup(search_request, "html.parser")
    # check at least one yugioh card has been found
    check_cards = search_page.find_all(class_ = "table table-striped")
    try:
        check_cards = check_cards[0]
    except:
        return None
    # Control how many pages of results there are and create a URL for each page
    card_search_urls = []
    try:
        pages = search_page.find(class_ = "mx-1")
        pages = pages.find(text=True)
        pages = pages.split()
        pages = int(pages[-1])
    except:
        pages = 1
    for page in range(1, pages+1):
        card_search_urls.append(f"https://www.cardmarket.com/de/YuGiOh/Products/Search?searchString={urllib.parse.quote(name)}&site={page}")
    return card_search_urls

def GetCardlistFromSearchURL(URL, cardlist):
    search_request = web.Get_Webpage(URL)
    search_page = BeautifulSoup(search_request, "html.parser")
    # Receive the table with the found cards
    cards_table = search_page.find(class_ = "table-body")
    # Get all rows of the table (direct childs of the table)
    rows = cards_table.find_all(recursive=False)
    # Get all information of cards from all rows
    for row in rows:
        card = {}
        card["package"] = row.find(class_ = "col-icon small").find(text=True)
        card["name"] = row.find(class_ = "col-12 col-md-8 px-2 flex-column").find(text=True)
        card["url"] = f"https://www.cardmarket.com/{row.find(class_ = 'col-12 col-md-8 px-2 flex-column').find('a')['href']}"
        card["rarity"] = row.find(class_ = "col-12 col-md-auto col-rarity d-none d-md-flex px-2").find("span").find("span")["data-original-title"]
        cardlist.append(card)

def GetCardlistFromSearchURLs(URLs, cardlist):
    threads = []
    # create a thread for each url
    for URL in URLs:
        threads.append(Thread(target=GetCardlistFromSearchURL, args=(URL, cardlist)))
    # start all threads
    for process in threads:
        process.start()
    # wait until all threads a finish
    for process in threads:
        process.join()