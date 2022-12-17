from email.message import EmailMessage
from creds import password
import ssl, smtplib, requests, schedule, time
from bs4 import BeautifulSoup
url='https://www.apaoltenia.ro/index.php/category/anunturi/'
import datetime
now = datetime.datetime.now()
date = now.strftime("%d.%m.%Y")

def smail(msg, link, titlu):
    sender = 'pythonradu1@gmail.com'
    receiver = 'florianmradu@gmail.com'
    subject = 'Compania de Apă Oltenia'
    body = f'''
    S.C. Compania de Apă Oltenia S.A.: {titlu.text.strip()}

    Link: {link}
    Mesaj:
    {msg}
    '''
    em = EmailMessage()
    em['From'] = sender
    em['To'] = receiver
    em['Subject'] = subject
    em.set_content(body)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
       smtp.login(sender, password)
       smtp.sendmail(sender, receiver, em.as_string())


def verifica(link):
    reqs = requests.get(link)
    soup = BeautifulSoup(reqs.content, 'html.parser')
    source = [list.find('u') for list in soup.find_all('div', class_="entry-content clear")]
    page = soup.find('div', class_="entry-content clear")
    message = page.text.strip()
    for x in source:
        try:
            if date in message or "Romanești" in message:
                print ("Sent a message")
                smail(message, link, x)
        except Exception as e:
            continue
def check():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [list.find('a', href=True)['href'] for list in soup.find_all('h2', class_="entry-title")]
    for x in links:
        verifica(x)


schedule.every().day.at("09:00").do(check)

while True:
    schedule.run_pending()
    time.sleep(1380)