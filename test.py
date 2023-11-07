# beauty_soup.py

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

url = "https://medium.com/swlh/what-is-bitcoin-ffab5e2e6a1c#:~:text=Bitcoin%20is%20the%20first%20decentralized%20electronic%20cash%20payment%20network%20that,government%20or%20a%20central%20bank"
req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
page = urlopen(req)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
print(soup.get_text())


from bs4 import BeautifulSoup, NavigableString

