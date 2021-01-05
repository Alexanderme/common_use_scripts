import requests
from bs4 import BeautifulSoup

do_main = "https://www.cdfangxie.com"

for i in range(1, 119):
    resp = requests.get('https://www.cdfangxie.com/Infor/type/typeid/36.html?&p=%s' % i)
    soup = BeautifulSoup(resp.text, "html.parser", from_encoding="utf-8")
    links = soup.find_all('a')
    for link in links:
        try:
            if link.get_text().split("|")[1]:
                print(do_main + link['href'], link.get_text())
        except:
            pass
