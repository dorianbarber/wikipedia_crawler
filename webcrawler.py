from bs4 import BeautifulSoup
from time import sleep
import requests
import urllib

start_url = "https://en.wikipedia.org/wiki/Special:Random"
target_url = "https://en.wikipedia.org/wiki/Psychology"
"""
This boolean function checks to see if we found the target article,
    if the search is going on for too long, if the search is going
    through articles in a loop. If any of those conditions are met
    the function returns false otherwise it return true and the search
    continues.
"""
def continue_crawl(search_history, target_url, article_limit=25):
    if search_history[-1] == target_url:
        print("The target article has been found!")
        return False
    elif len(search_history) > article_limit:
        print("The search has gone on for too long, aborting search")
        return False
    elif len(search_history) != len(set(search_history)):
        print(search_history[-1])
        print("The search is going in a loop, aborting search")
        return False
    else:
        return True

#this recursive=False statement only checks the children of the tags, not the sub
#children. The content_div brings us to the main content of each wikipedia page
def find_first_link(input_article):
    response = requests.get(input_article)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    article_link = None
    content_div = soup.find(id='mw-content-text').find(class_='mw-parser-output')
    for element in content_div.find_all('p', recursive=False):
        if element.find('a',recursive=False):
            article_link = element.find('a',recursive=False).get('href')
            break
    #if the article_link remains none then return nothing
    if not article_link:
        return
    first_link = urllib.parse.urljoin('https://en.wikipedia.org/', article_link)
    return first_link




"""
web_crawl will use the continue_crawl function and then proceed
    to find the first link in the article and record it in the
    visitied article list (aka article_chain). Then pause for
    two seconds to not overload wikipedia with searches.
"""
print("Target article is: " + target_url)
article_chain = [start_url]

while continue_crawl(article_chain, target_url):
    print(article_chain[-1])
    first_link = find_first_link(article_chain[-1])
    if not first_link:
        print("There was no link in this article, aborting search.")
        break
    article_chain.append(first_link)
    sleep(2)
