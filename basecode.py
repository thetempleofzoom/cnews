from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import urlparse
from pprint import pprint

def getLinks(url):

    USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'
    request = Request(url)
    request.add_header('User-Agent', USER_AGENT)
    response = urlopen(request)
    content = response.read().decode('utf-8')
    response.close()

    soup = BeautifulSoup(content, "html.parser")

    #links = soup.find_all("a") # Find all elements with the tag <a>
    links = soup.find_all("a", attrs={"class": "BlogList-item-title"})
    print(links)
    for link in links:
        if link.get("href").startswith("/"):
            res = urlparse(url)
            longlink = res.scheme+'://'+res.netloc+link.get("href")
        else:
            longlink = link.get("href")

        print("Link:", longlink, "Text:", link.string)


getLinks("https://www.jeffsachs.org/newspaper-articles")