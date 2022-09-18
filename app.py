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
