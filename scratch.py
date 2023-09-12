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

def compare(snapshotnow, snapshotzero):
    # compare snapshot against current links

    #use url as unique identifier
    previous = []
    for s in snapshotzero:
        previous.append(s[2])

    new = []
    for c in snapshotnow:
        if c[2] in previous:
            continue
        else:
            new.append(c)

    return new


#dfdict = upload_settings()
#pickledown(dfdict, 'dfdict.pkl')

#dfdict = pickleup('dfdict.pkl')

#pprint(dfdict)
#snapshotnow = getLinks(dfdict)

# snapshotnow = pickleup('snapshotnow.pkl')
# snapshotzero = pickleup('dummy.pkl')
# new = compare(snapshotnow, snapshotzero)
#pickledown(new, 'new.pkl')
#pickledown(snapshotnow, 'snapshotzero.pkl')
#testnew(new, dfdict)
#  consolidate inputs for email into one dictionary
#  loop by topic, then by blog (w link), then new articles (title followed by longlink)
        
#send_mail(new, dfdict)
