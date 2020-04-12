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

from app.models import Judoka, JudoResult, JudoEvent


def get_judoka_info(judoins_id):
    url = r'https://www.judoinside.com/judoka/' + str(judoins_id) + r"/judo-results"
    # Get the HTML page
    txt = requests.post(url=url).content.decode(encoding='utf_8')
    soup = BeautifulSoup(txt, features="html.parser")

    # Scrap information
    if not "Judoka not found." in str(soup):
        # Get the Person info
        names = soup.find_all(class_="small-12 medium-6 judokaData columns")[0].contents[0]
        first_name = names.split(" ")[0].lower().capitalize()
        last_name = names.split(" ")[1].upper()

        html_country = soup.find("ul", {"id": "judokaUserDatas"}).find("li").contents
        # Handle case where country is not provided
        if len(html_country) > 1:
            country = html_country[1]
        else:
            country = ""
        html_desc = soup.find("div", {"id": "judokaDesc"}).contents
        if len(html_desc) > 0:
            description = html_desc[0]
        else:
            description = ""

        html_birthday = soup.find("ul", {"id": "judokaUserDatas"}).find_all("li")[1].contents[1]
        # Handle case where birthday is not provided
        if "Unknown" in str(html_birthday):
            birthday = None
        else:
            birthday = dt.datetime.strptime(html_birthday.split(" (")[0], "%d %B %Y").date()

        # Get the picture
        photo = \
            soup.find_all(class_="small-12 medium-6 columns judokaData profile-photo-centered")[0].findAll("img")[0][
                "src"]
        url_image = r'https://www.judoinside.com' + photo

        judoka_info = (first_name, last_name, country, birthday, description, url_image, soup)
    else:
        judoka_info = None

    return judoka_info


def get_event_info(event_id):
    # Go on the event page to get information about it
    url_event = "https://www.judoinside.com/event/{}".format(event_id)
    txt = requests.post(url=url_event).content.decode(encoding='ISO-8859-1')
    event_soup = BeautifulSoup(txt, features="html.parser")

    # Scrap information
    event_name = event_soup.find("div", {"id": "eventsDatas"}).find("h2").contents[0]
    date_start_str = event_soup.find("ul", {"id": "eventsLocation"}).find_all("li")[0].contents[1].split(" - ")[0]
    date_end_str = event_soup.find("ul", {"id": "eventsLocation"}).find_all("li")[0].contents[1].split(" - ")[1]
    if date_end_str == "":
        date_end_str = date_start_str
    date_start = dt.datetime.strptime(date_start_str, '%d %b %Y').date()
    date_end = dt.datetime.strptime(date_end_str, '%d %b %Y').date()
    event_type = event_soup.find("ul", {"id": "eventsLocation"}).find_all("li")[2].contents[1]
    country = event_soup.find("ul", {"id": "eventsLocation"}).find_all("li")[1].contents[1].split(", ")[1].upper()

    return event_name, date_start, date_end, event_type, country


def fill_database(n_max: int = 0):
    if n_max == 0:
        n_max = 1000  # 148099 is the max on the 12/04/2020

    # Loop over judo inside IDs
    for judoins_id in tqdm(range(1, n_max)):
        judoins_id = 450

        judoka_info = get_judoka_info(judoins_id)
        if judoka_info is not None:
            (first_name, last_name, country, birthday, description, url_image, soup) = judoka_info

            # Insert data in database
            judoka, _ = Judoka.objects.get_or_create(first_name=first_name, last_name=last_name,
                                                     country=country, description=description,
                                                     birthday=birthday, judoins_id=judoins_id)

            # Update picture if it is not the default one and if there isn't one already
            image_name = urlparse(url_image).path.split('/')[-1]
            default_image_name = Judoka._meta.get_field('photo').get_default().split('/')[-1]
            if image_name != default_image_name and default_image_name in str(judoka.photo.path):
                judoka.photo.save(image_name, ContentFile(requests.get(url_image).content), save=True)

            # Get the judo events
            events = soup.find_all(class_="accordTable")
            if len(events) > 0:
                events = events[0].find_all(class_='accord')
                for event in events:
                    event_date = dt.datetime.strptime(event.find_all(class_="date")[0].contents[0], '%d/%m/%Y').date()
                    result = int(event.find_all(class_="result")[0].contents[0])
                    event_id = int(event.find_all('a', class_="insidelink")[0]["href"].split("/")[2])
                    category = event.find_all(class_="cat")[0].contents[0]

                    event_name, date_start, date_end, event_type, event_country = get_event_info(event_id)
                    # Insert event in JudoEvent database
                    event, _ = JudoEvent.objects.get_or_create(event_name=event_name, event_judoins_id=event_id,
                                                               date_start=date_start, date_end=date_end,
                                                               country=event_country, event_type=event_type)

                    # Insert Result in JudoResult database
                    judo_result, _ = JudoResult.objects.get_or_create(result=result, category=category,
                                                                      date=event_date, judoka=judoka,
                                                                      event=event)

if __name__ == "__main__":
    fill_database(n_max=10)
