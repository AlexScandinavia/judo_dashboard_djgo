import requests
from bs4 import BeautifulSoup
import datetime as dt
from urllib.parse import urlparse
from django.core.files.base import ContentFile
from tqdm import tqdm
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from app.models import Judoka

# Loop over judo inside IDs
for judoins_id in tqdm(range(1, 1000)):
    url = r'https://www.judoinside.com/judoka/' + str(judoins_id) + r"/judo-results"

    # Get the HTML page
    txt = requests.post(url=url).content.decode(encoding='ISO-8859-1')
    soup = BeautifulSoup(txt, features="html.parser")

    if not "Judoka not found." in str(soup):
        # Get the Person info
        names = soup.find_all(class_="small-12 medium-6 judokaData columns")[0].contents[0]
        first_name = names.split(" ")[0].lower().capitalize()
        last_name = names.split(" ")[1].upper()
        html_country = soup.find("ul", {"id": "judokaUserDatas"}).find("li").contents
        if len(html_country) > 1:
            country = html_country[1]
        else:
            country = ""
        html_desc = soup.find("div", {"id": "judokaDesc"}).contents
        if len(html_desc) > 0:
            description = html_desc[0]
        else:
            description = ""

        html_birthday = soup.find("ul", {"id": "judokaUserDatas"}).find("li", class_="spacing").contents[1]
        # Handle case where birthday is not provided
        if "Unknown" in str(html_birthday):
            birthday = None
        else:
            birthday = dt.datetime.strptime(html_birthday.split(" (")[0], "%d %B %Y").date()

        # Get the picture
        photo = soup.find_all(class_="small-12 medium-6 columns judokaData profile-photo-centered")[0].findAll("img")[0][
            "src"]
        url_image = r'https://www.judoinside.com' + photo
        image_name = urlparse(url_image).path.split('/')[-1]

        # Insert data in database
        judoka, _ = Judoka.objects.get_or_create(first_name=first_name, last_name=last_name,
                                                 country=country, description=description,
                                                 birthday=birthday, judoins_id=judoins_id)
        if image_name != "avatar-man.jpg" and "avatar-man.jpg" in str(judoka.photo.path):
            judoka.photo.save(image_name, ContentFile(requests.get(url_image).content), save=True)

        # # Get the judo events
        # events = soup.find_all(class_="accordTable")[0].find_all(class_='accord')
        # for event in events:
        #     date = dt.datetime.strptime(event.find_all(class_="date")[0].contents[0], '%d/%m/%Y').date()
        #     result = int(event.find_all(class_="result")[0].contents[0])
        #     event_name = event.find_all('a', class_="insidelink")[0].contents[0]
        #     category = event.find_all(class_="cat")[0].contents[0]
