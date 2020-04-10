import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt


URL_API = r'https://www.judoinside.com/judoka/1/judo-results'
URL_API = 'https://www.judoinside.com/judoka/110277/Alexandre_Mathieu/judo-results'
URL_API = 'https://www.judoinside.com/judoka/32265/Teddy_Riner/judo-results'

resp = requests.post(url=URL_API)
txt = resp.content.decode(encoding='ISO-8859-1')
soup = BeautifulSoup(txt)


# Get the judo events
events = soup.find_all(class_="accordTable")[0].find_all(class_='accord')
for event in events:
    date = dt.strptime(event.find_all(class_="date")[0].contents[0], '%d/%m/%Y').date()
    result = int(event.find_all(class_="result")[0].contents[0])
    event = event.find_all('a', class_="insidelink")[0].contents[0]
    category = event.find_all(class_="cat")[0].contents[0]

# Get the picture
photo = soup.find_all(class_="small-12 medium-6 columns judokaData profile-photo-centered")[0].findAll("img")[0]["src"]
URL_image = r'https://www.judoinside.com' + photo

from app.models import Judoka

import os

env = os.environ.copy()
SECRET_KEY = env['SECRET_KEY']