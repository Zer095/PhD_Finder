import requests
from pytz import timezone
from django.core.management.base import BaseCommand

from positions.models import Position
import datetime
from django.utils import dateparse


def get_positions():
    url = "https://inspirehep.net/api/"
    record_type = "jobs?"
    query_string = "sort=mostrecent&status=open&field_of_interest=astro-ph&field_of_interest=gr-qr&rank=PHD"

    search = requests.get(url + record_type + query_string)

    jobs = search.json()["hits"]["hits"]
    return jobs

def seed_position():
    for i in get_positions():
            country = []
            field = []
            title = i["metadata"]["position"]

            for fld in i["metadata"]["arxiv_categories"]:
                field.append(fld)
                
            desc = str(i["metadata"]["description"]).replace("<div>","").replace("</div>","").replace("<br>"," ")
            host = i["metadata"]["institutions"][0]["value"]
            for region in i["metadata"]["regions"]:
                country.append(region)
            pub_date = dateparse.parse_datetime(i["created"])
            exp_date = dateparse.parse_datetime(i["metadata"]["deadline_date"])
            exp_date = timezone('UTC').localize(exp_date)
            try:
                link = i["metadata"]["urls"][0]["value"]
            except KeyError:
                link = " "
            
            position = Position.objects.get_or_create(pos_title = title, pos_field = field, pos_desc=desc,
                         pos_host=host, pos_country=country, pos_pub_date=pub_date, 
                         pos_exp_date=exp_date, pos_link=link)

            
            

class Command(BaseCommand):
     def handle(self, *args, **options):
          seed_position()
          print("Positions created successfully")