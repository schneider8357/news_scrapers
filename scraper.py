import os
import sys

import requests
from bs4 import BeautifulSoup


def get_news_urls(search_url):
    response = requests.get(search_url)
    if response.status_code != 200:
        response.raise_for_status()
    soup = BeautifulSoup(response.text, features="html.parser")
    news_links = []
    for element in soup.find_all("a"):
        if "https://www.cartacapital.com.br/" not in element["href"]:
            continue
        if element.find("h2") is not None:
            news_links.append(element["href"])
    return news_links

def get_news_content(news_url):
    response = requests.get(news_url)
    soup = BeautifulSoup(response.text, features="html.parser")
    content_open_div = soup.find("div", {"class": "contentOpen"})
    p_tags = content_open_div.find_all("p")
    # TODO: revover tags do innerHTML dos paragrafos
    news_content = []
    for tag in p_tags:
        news_content.append("".join(tag.decode_contents()))
    return "\n".join(news_content)

search_query = sys.argv[1].replace(" ", "+")

for i in range(1,1000000):
    search_url = f"https://www.cartacapital.com.br/page/{i}/?s={search_query}"
    try:
        news_urls = get_news_urls(search_url)
    except requests.exceptions.HTTPError:
        break

    for news_url in news_urls:
        news_content = get_news_content(news_url)
        news_filename = os.path.join("news", news_url.split("/")[-2])
        with open(news_filename, "w") as new_file:
            new_file.write(news_content)
