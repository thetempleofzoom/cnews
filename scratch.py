from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import urlparse
from pprint import pprint
from runemail import send_mail
import pickle, pandas as pd

def upload_settings():
    df = pd.read_excel("readinglist.xlsx", sheet_name="Sheet1")
    df.path = df.path.fillna('')
    dfdict = df.set_index('baseurl').to_dict()
    print(dfdict['path'])

    for k,v in dfdict['path']:
        if len(v) == 0:
            dfdict['path'][k] = k
        else:
            v = v.split(',')
            dfdict['path'][k] = [k+cat.strip() for cat in v]

    pprint(dfdict['path'])

    

def getLinks(url):
    #this list will house all current links from various websites
    snapshotnow = []

    USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'
    request = Request(url)
    request.add_header('User-Agent', USER_AGENT)
    response = urlopen(request)
    content = response.read().decode('utf-8')
    response.close()

    soup = BeautifulSoup(content, "html.parser")

    #create loop here
    links = []
    tag = 'div'
    filter = {"class": "BlogList-item-image"}

    dsoup = soup.find_all(tag, **filter)

    for d in dsoup:
        links.append(d.find('a', href=True))

    for link in links:
        title = link.get_text() #alternatively link.string
        if link.get("href").startswith("/"):
            res = urlparse(url)
            longlink = res.scheme+'://'+ res.netloc + link.get("href")
        else:
            longlink = link.get("href")
        print(longlink)
        snapshotnow.append((longlink, title))

    return snapshotnow

def compare(current):
    # compare snapshot against current links
    with open('ostb.pkl', 'rb') as file:
        snapshotzero = pickle.load(file)

    #use url as unique identifier
    previous = []
    for s in snapshotzero:
        previous.append(s[0])

    new = []
    for c in current:
        if c[0] in previous:
            continue
        else:
            new.append(c)

    with open('ostb.pkl', 'wb') as file:
        pickle.dump(current, file)

    return new

#new = compare(getLinks("http://syedsoutsidethebox.blogspot.com/"))
#send_mail(new)
#getLinks("http://jeffsachs.org/interviewsandmedia")
upload_settings()

