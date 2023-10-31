"""Scraper for the website cartacapital.com.br"""
import os
import sys
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from db import NewsArticle


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


def get_news_author(soup: BeautifulSoup):
    """Returns author name and author profile URL"""
    heading = soup.find("section", {"class": "s-content__heading"})
    author = heading.find("div", {"class": "s-content__infos"}).find("span").find("a")
    return author.decode_contents().replace("\n", ""), author["href"]

def get_news_tags(soup):
    """Returns list of tag names for the news article"""
    section_tags = soup.find("section", {"class": "s-tags"})
    tags = [tag.decode_contents() for tag in section_tags.find_all("a")]
    return tags

def get_news_title(soup: BeautifulSoup):
    """Returns news title"""
    heading = soup.find("section", {"class": "s-content__heading"})
    title = heading.find("h1")
    return title.decode_contents()

def get_news_lead(soup: BeautifulSoup):
    """Returns news lead text"""
    heading = soup.find("section", {"class": "s-content__heading"})
    for element in heading.find("p"):
        return element.decode_contents()

def get_news_content(soup):
    """Returns news content with internal HTML tags"""
    content_open_div = soup.find("div", {"class": "contentOpen"})
    p_tags = content_open_div.find_all("p")
    # TODO: revover tags do innerHTML dos paragrafos
    news_content = []
    for tag in p_tags:
        news_content.append("".join(tag.decode_contents()))
    return "\n".join(news_content)

def get_news(news_url):
    response = requests.get(news_url)
    soup = BeautifulSoup(response.text, features="html.parser")
    name, profile_url = get_news_author(soup)
    print(news_url, name, profile_url, get_news_tags(soup), get_news_title(soup), get_news_lead(soup))
    # article = NewsArticle(
    #         url=news_url,
    #         author=get_news_author(soup),
    #         tags=get_news_tags(soup),
    #         title=get_news_title(soup),
    #         subtitle=None,
    #         lead=get_news_lead(soup),
    #         section='',
    #         created_at='',
    #         accessed_at=datetime.now(),
    #         content_html=get_news_content(soup),
    #         content_txt=get_news_content(soup),
    #     )
    return article

search_query = sys.argv[1].replace(" ", "+")

for i in range(1,1000000):
    search_url = f"https://www.cartacapital.com.br/page/{i}/?s={search_query}"
    try:
        news_urls = get_news_urls(search_url)
    except requests.exceptions.HTTPError:
        break

    for news_url in news_urls:
        article = get_news(news_url)
        news_filename = os.path.join("news", news_url.split("/")[-2])
        #with open(news_filename, "w") as new_file:
        #    new_file.write(news)
