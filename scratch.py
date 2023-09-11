from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import urlparse
from pprint import pprint
from tasks import *
import pickle, pandas as pd

def upload_settings():
    df = pd.read_excel("readinglist.xlsx", sheet_name="Sheet1")
    df.path = df.path.fillna('')
    #orient=index is key to getting all other columns into v side of things
    dfdict = df.set_index('baseurl').to_dict(orient='index')

    for k,v in dfdict.items():
        #get full webpage links
        if len(v['path']) == 0:
            dfdict[k]['path'] = [k]
        else:
            v['path'] = v['path'].split(',')
            dfdict[k]['path'] = [k+cat.strip() for cat in v['path']]
        #convert attribute tags into dictionary item
        v['filter'] = v['filter'].split(',')
        dfdict[k]['filter'] = [cat.strip() for cat in v['filter']]
        if v['filter'][1] == 'True': v['filter'][1] = True
        x = iter(v['filter'])
        v['filter'] = dict(zip(x,x))

    pprint(dfdict)
    return dfdict


def getLinks(dfdict):
    #this list will house all current links from various websites
    snapshotnow = []

    for k,v in dfdict.items():
        try:
            print(f"running {v['name']}")
            for url in v['path']:
                USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'
                request = Request(url)
                request.add_header('User-Agent', USER_AGENT)
                response = urlopen(request)
                content = response.read().decode('utf-8')
                response.close()

                soup = BeautifulSoup(content, "html.parser")

                links = []
                tag = v['tag']
                filter = v['filter']

                dsoup = soup.find_all(tag, **filter)


                for d in dsoup:
                    line = d.find('a', href=True)
                    text = line.text.strip()
                    if not text:
                        line = d.find('a', {'class':'BlogList-item-title'})
                    links.append(line)
                #pprint(links)

                for link in links:
                    title = link.text.strip() #alternatively link.get_text()
                    print(title)
                    if link.get("href").startswith("/"):
                        res = urlparse(url)
                        longlink = res.scheme+'://'+ res.netloc + link.get("href")
                    else:
                        longlink = link.get("href")
                    snapshotnow.append((k, title, longlink))
        except:
            print(f"error with {v['name']}. continuing to the next link..")
            continue
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

upload_settings()
#dfdict = upload_settings()
#pickledown(dfdict, 'dfdict.pkl')

dfdict =  {'https://www.jeffsachs.org/': {'filter': {'id': True},
                                'name': 'Jeffrey Sachs',
                                'path': ['https://www.jeffsachs.org/recorded-lectures',
                                         'https://www.jeffsachs.org/interviewsandmedia',
                                         'https://www.jeffsachs.org/newspaper-articles'],
                                'tag': 'article',
                                'topic': 'world_affairs'}}
#dfdict = pickleup('dfdict.pkl')

#pprint(dfdict)
#current = getLinks(dfdict)
#new = compare(getLinks("http://syedsoutsidethebox.blogspot.com/"))
#send_mail(new)
#pprint(current)