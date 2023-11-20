from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import urlparse
from pprint import pprint
from tasks import *
import pandas as pd
from inputs import *

# for multiple users/sheets. this is main file now
def upload_settings():
    users = pd.read_excel(datafile, sheet_name=userlist)
    usersrun = users[users['run'] == "Yes"]["user"].values.tolist()
    users = users[users['run'] == "Yes"]
    userdict = dict(zip(users.user, users.email))

    df = pd.read_excel(datafile, sheet_name=sheet)
    df.path = df.path.fillna('')
    # filter only those websites linked to users that need to be run
    df = df[df['user'].isin(usersrun)]
    # orient=index is key to getting all other columns into v side of things
    dfdict = df.set_index('baseurl').to_dict(orient='index')

    toggle = pd.read_excel(datafile, sheet_name=settings)
    if len(userdict)==1 and usersrun[0]=="SY":
        togglelist = toggle[toggle['runtype'] == "private"].values.tolist()[0]
    else:
        togglelist = toggle[toggle['runtype'] == "public"].values.tolist()[0]

    for k,v in dfdict.items():
        #get full webpage links for websites with multiple pages
        if len(v['path']) == 0:
            dfdict[k]['path'] = [k]
        else:
            v['path'] = v['path'].split(',')
            dfdict[k]['path'] = [k+cat.strip() for cat in v['path']]
        #convert attribute tags into dictionary item
        v['filter'] = v['filter'].split(',')
        dfdict[k]['filter'] = [cat.strip() for cat in v['filter']]
        # there can be multiple attributes to search for in a list
        v['filter'] = {v['filter'][0]:v['filter'][1:]}
    return dfdict, userdict, togglelist


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
                response = urlopen(request, timeout=30)
                content = response.read().decode('utf-8')
                response.close()

                soup = BeautifulSoup(content, "html.parser")

                tag = v['tag']
                filter = v['filter']
                dsoup = soup.find_all(tag, **filter)


                for d in dsoup:
                    if d.name == 'a':
                        # title is extracted before link is transformed to just the href link
                        title = d.text
                        link = d['href']
                    else:
                        title = d.find('a').text
                        link = d.find('a')['href']
                    if link.startswith("/"):
                        res = urlparse(url)
                        longlink = res.scheme + '://' + res.netloc + link
                    else:
                        longlink = link
                    title = title.strip().splitlines()[0]
                    print("Link:", longlink, "Text:", title)
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


dfdict = upload_settings()[0]
userdict = upload_settings()[1]
togglelist = upload_settings()[2]

pickledown(dfdict, togglelist[1])
snapshotnow = getLinks(dfdict)
snapshotzero = pickleup(togglelist[2])
new = compare(snapshotnow, snapshotzero)
pickledown(new, togglelist[3])
pickledown(snapshotnow, togglelist[2])
send_mail(new, dfdict, togglelist)
