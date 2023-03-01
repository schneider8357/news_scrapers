import requests
from bs4 import BeautifulSoup


search_query = "impeachment"

search_url = f"https://www.cartacapital.com.br/?s={search_query}"

response = requests.get(search_url)

soup = BeautifulSoup(response.text, features="html.parser")

links = soup.find_all("a")


news_pages = []

for link in links:
    if "https://www.cartacapital.com.br/" in link["href"]:
        # print(link["href"])
        title = link.find("h2")
        if title is not None:
            news_pages.append(link["href"])


for news_url in news_pages:
    response = requests.get(news_url)
    soup = BeautifulSoup(response.text, features="html.parser")
    content_open_div = soup.find("div", {"class": "contentOpen"})
    p_tags = content_open_div.find_all("p")
    # TODO: revover tags do innerHTML dos paragrafos
    news_content = []
    for tag in p_tags:
        news_content.append("".join(tag.decode_contents()))
    with open("news/" + news_url.split("/")[-2], "w") as new_file:
        new_file.write("\n".join(news_content))

# TODO: visitar outras paginas da busca
# https://www.cartacapital.com.br/page/2/?s=impeachment

