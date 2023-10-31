from urllib.parse import unquote
import re

import requests
from bs4 import BeautifulSoup

termo_de_busca = "lula"
termo_de_busca = termo_de_busca.replace(" ", "+")
url = f"https://g1.globo.com/busca/?q={termo_de_busca}"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

articles = soup.find_all("div", {"class": "widget--info__text-container"})

for article in articles:
    url = unquote(article.find("a")["href"])
    padrao = r'&u=(https://[^&]+)'
    correspondencias = re.search(padrao, url)

    if correspondencias:
        url = correspondencias.group(1)
        print(url)
    print("--------------------------------------------------")
