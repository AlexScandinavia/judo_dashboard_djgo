import json
import requests
from django.core.files.base import ContentFile
from tqdm import tqdm
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from app.models import Judoka


def get_judoka_info(judobase_id):
    # World ranking info
    url_wrl = r"https://data.ijf.org/api/get_json?access_token=&params%5Baction%5D=competitor.wrl_current&params%5B_" \
              r"_ust%5D=&params%5Bid_person%5D={}".format(judobase_id)

    resp_wrl = json.loads(requests.post(url=url_wrl).content)
    if len(resp_wrl)>0:
        resp_wrl = resp_wrl[0]
        resp_wrl["points"]= int(resp_wrl["points"])
        resp_wrl["place"] = int(resp_wrl["place"])

    else:
        resp_wrl = dict()
        resp_wrl["points"] = None
        resp_wrl["place"] = None
        resp_wrl["weight"] = None

    # General info
    url_info = r"https://data.ijf.org/api/get_json?access_token=&params%5Baction%5D=competitor.info&params%5B_" \
               r"_ust%5D=&params%5Bid_person%5D={}".format(judobase_id)
    resp_info = json.loads(requests.post(url=url_info).content)

    if resp_info["height"] is not None:
        resp_info["height"] = int(resp_info["height"])

    info_dict = {"judobase_id":judobase_id,
                "wrl_points": resp_wrl["points"],
                 "world_ranking": resp_wrl["place"],
                 "wrl_category": resp_wrl["weight"],
                 "category": resp_info["categories"],
                 "last_name": resp_info["family_name"],
                 "first_name": resp_info["given_name"],
                 "gender": resp_info["gender"][0].upper(),
                 "country": resp_info["country"],
                 "fav_tech": resp_info["ftechique"],
                 "height": resp_info["height"],
                 "belt": resp_info["belt"],
                 "birthyear": int(resp_info["dob_year"])
                 }


    return info_dict

def get_picture(judobase_id):
    url_image = r"https://78884ca60822a34fb0e6-082b8fd5551e97bc65e327988b444396" \
                r".ssl.cf3.rackcdn.com/profiles/350/{}.jpg".format(judobase_id)
    image_file = ContentFile(requests.get(url_image).content)

    return image_file


def fill_database(n_max: int = 0):
    if n_max == 0:
        n_max = 61448  # 61448 is the max on the 12/04/2020

    # Loop over judo inside IDs
    for judobase_id in tqdm(range(1, n_max)):

        info_dict = get_judoka_info(judobase_id)
        image_file = get_picture(judobase_id)

        # Update or Insert data in database
        query = Judoka.objects.filter(judobase_id=judobase_id)
        if len(query) > 0:
            query.update(**info_dict)
            query[0].photo.delete()
            query[0].photo.save("{}.jpg".format(judobase_id), image_file, save=True)
            query[0].save()
        else:
            judoka = Judoka(**info_dict)
            judoka.photo.delete()
            judoka.photo.save("{}.jpg".format(judobase_id), image_file, save=True)
            judoka.save()

if __name__ == "__main__":
    fill_database(n_max=1000)
