from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import urlparse
import socket
from urllib3.connection import HTTPConnection
from pprint import pprint



HTTPConnection.default_socket_options = (
    HTTPConnection.default_socket_options + [
        (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1),
        (socket.SOL_TCP, socket.TCP_KEEPIDLE, 45),
        (socket.SOL_TCP, socket.TCP_KEEPINTVL, 10),
        (socket.SOL_TCP, socket.TCP_KEEPCNT, 6)
    ]
)

def getLinks(url):

    USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'
    request = Request(url)
    request.add_header('User-Agent', USER_AGENT)
    response = urlopen(request, timeout=200)
    content = response.read().decode('utf-8')
    response.close()

    soup = BeautifulSoup(content, "html.parser")
    #links = soup.find_all("a") # Find all elements with the tag <a>
    links = soup.find_all("div", attrs={"class": "categoryArticle__content"})

    for link in links:
        if link.name == 'a':
            # title goes before link is changed to just the href link
            title = link.text.strip()
            link = link['href']
        else:
            title = link.find('a').text.strip()
            link = link.find('a')['href']
        if link.startswith("/"):
            res = urlparse(url)
            longlink = res.scheme+'://'+res.netloc+link
        else:
            #longlink = link.get("href")
            longlink = link
        
        print("Link:", longlink, "Text:", title)


getLinks("https://oilprice.com/Latest-Energy-News/World-News/")