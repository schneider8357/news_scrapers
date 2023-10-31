from selenium import webdriver
from selenium.webdriver.common.by import By


termo_de_busca = "lula"
url = f"https://elpais.com/buscador/?q={termo_de_busca}"

driver = webdriver.Chrome()
driver.get(url)

button = driver.find_element(By.ID, "didomi-notice-agree-button")

button.click()

results_container = driver.find_element(By.ID, "results-container")

articles = results_container.find_elements(By.TAG_NAME, "article")
articles = articles[:5]

header = []
urls = []

for article in articles:
    # print(article.text)
    header.append(article.find_element(By.TAG_NAME, "h2").text)
    urls.append(article.find_element(By.TAG_NAME, "h2").find_element(By.TAG_NAME, "a").get_attribute("href"))

content = []

for url in urls:
    driver.get(url)
    h2 = driver.find_element(By.TAG_NAME, "article").find_element(By.TAG_NAME, "header").find_element(By.TAG_NAME, "h2")
    content.append(h2.text)

input()

with open("header.txt", "w") as f:
    f.write("\n".join(header))
with open("content.txt", "w") as f:
    f.write("\n".join(content))