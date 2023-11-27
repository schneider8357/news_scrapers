import sys

import requests
from bs4 import BeautifulSoup


soup = BeautifulSoup(requests.get(sys.argv[1]).text)
print(soup.prettify())
