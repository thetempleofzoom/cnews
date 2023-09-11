import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pickle

def pickledown(input, pklfile):
    with open(pklfile, 'wb') as f:
        pickle.dump(input, f)

def pickleup(pklfile):
    with open(pklfile, 'rb') as f:
        res = pickle.load(f)
    return res

def send_mail(new):
    # me == my email address
    # you == recipient's email address
    me = "shadowysupercoderssc@gmail.com"
    you = "shadowysupercoderssc@gmail.com"
    PASSWORD = os.environ.get('SSCPW')

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "new articles"
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message (a plain-text and an HTML version).
    text = "Here are the latest articles from your custom list, updated daily."

    html = """\
        <html>
        <head></head>
        <body>
        <p>"""+text+"""</p>
        <h2>From <a href='http://syedsoutsidethebox.blogspot.com'>Outsyed The Box</a></h2><ul>"""
    if new:
        for n in new:
            html = html + """<li>"""+str(n[1])+ """</li>""" +str(n[0])
    else:
        html = html + """<h3>No new articles, sorry!</h3>"""

    html = html+"""</ul><br>
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

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(me, PASSWORD)
        smtp_server.sendmail(me, you, msg.as_string())

if __name__ == "__main__":
    new = [('http://syedsoutsidethebox.blogspot.com/2023/09/penipuan-harga-beras-pula-siapa-yang.html',
            'PENIPUAN HARGA BERAS PULA !! SIAPA YANG PENIPU SEB...'),
           ('http://syedsoutsidethebox.blogspot.com/2023/09/idrus-harun-must-answer-madani-says.html',
            'IDRUS HARUN MUST ANSWER - MADANI SAYS "Peguam Nega...'),
           ('http://syedsoutsidethebox.blogspot.com/2023/09/russia-destroys-2nd-british-challenger.html',
            'Russia Destroys 2nd British Challenger 2 Tank In U...')]
    send_mail(new)
    