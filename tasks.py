import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pickle
from datetime import datetime, date
from inputs import *

def pickledown(input, pklfile):
    with open(pklfile, 'wb') as f:
        pickle.dump(input, f)

def pickleup(pklfile):
    with open(pklfile, 'rb') as f:
        try:
            res = pickle.load(f)
        except EOFError:
            res = []
    return res

# *** fix so that separate email sent to indiv users ***
def send_mail(new, dfdict, togglelist):
    # me == my email address
    # you == recipient's email address
    me = emailfrom
    you = emailto
    PASSWORD = pw

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "new articles"
    msg['From'] = me
    msg['To'] = you

    last_run = pickleup(togglelist[4])
    if last_run == []:
        last_run = "(N/A) - this is first run"

    # Create the body of the message (a plain-text and an HTML version).
    text = f"""Here are the newest articles from your custom list since 
    the last email update on {last_run}."""

    html = """\
               <html>
               <head></head>
               <body>
               <p>""" + text + """</p>"""
    if new:
        for i, n in enumerate(new):
            newtup = (dfdict[n[0]]['name'], dfdict[n[0]]['topic'])
            new[i] = n + newtup

        topics = sorted(list(set([n[4] for n in new])))
        blogs = sorted(list(set([(n[3], n[4], n[0]) for n in new])))

        for topic in topics:
            html = html + f"""
                <h1>{topic}</h1>"""
            for blog in blogs:
                if blog[1] in topic:
                    html = html + f"""
                        <ul><h2>From <a href={blog[2]}>{blog[0]}</a></h2></ul>"""
                    for n in new:
                        if n[0] == blog[2]:
                            html = html + f"""<ul><li><a href={n[2]}>{n[1]}</a></ul>"""
    else:
        html = html + """<h3>No new articles, sorry!</h3>"""
        pass

    html = html+"""<br>
        </body>
        </html>
        """

    # Record the MIME types of both parts - text/plain and text/html.
    #part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    #msg.attach(part1)
    msg.attach(part2)

    with smtplib.SMTP_SSL(server,port) as smtp_server:
        smtp_server.login(me, PASSWORD)
        smtp_server.sendmail(me, you, msg.as_string())

    current_day = date.today().strftime("%b-%d-%Y")
    current_time = datetime.now().strftime("%H:%M:%S")
    last_run = current_day + ", " + current_time
    pickledown(last_run, togglelist[4])
    print("Update complete! Please check email")

if __name__ == "__main__":
    current_day = date.today().strftime("%b-%d-%Y")
    current_time = datetime.now().strftime("%H:%M:%S")
    last_run = current_day + ", " + current_time
    pickledown(last_run, pkllastrun)
    # new = pickleup('new.pkl')
    # dfdict = pickleup('dfdict.pkl')
    # send_mail(new, dfdict)


    