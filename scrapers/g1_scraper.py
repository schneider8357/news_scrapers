import os
from urllib.parse import unquote
import re
import sys

import requests
from bs4 import BeautifulSoup


termo_de_busca = " ".join(sys.argv[1::])
termo_de_busca = termo_de_busca.replace(" ", "+")
os.makedirs(f"articles/{termo_de_busca}", exist_ok=True)
url = f"https://g1.globo.com/busca/?q={termo_de_busca}"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

articles = soup.find_all("div", {"class": "widget--info__text-container"})

list_urls_noticias = []

for article in articles:
    url = unquote(article.find("a")["href"])
    padrao = r'&u=(https://[^&]+)'
    correspondencias = re.search(padrao, url)

    if correspondencias:
        url = correspondencias.group(1)
        if url.startswith("https://g1.globo.com"):
            list_urls_noticias.append(url)


print(list_urls_noticias)

for url in list_urls_noticias:
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    article_body = soup.find("div", {"class": "mc-article-body"})
    
    try:
        paragrafos = article_body.find_all("p", {"class": "content-text__container"})
    except AttributeError as exc:
        print(url)
        print("Erro ao fazer o scraping da url:", exc)

    with open(f"articles/{termo_de_busca}/" + url[url.rfind("/")+1:url.rfind(".")], "w") as f:
        f.write("\n".join([p.text for p in paragrafos]))
