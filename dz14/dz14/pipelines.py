# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests
import lxml.html
from bs4 import BeautifulSoup
from .models import Person, Keywords, Quotes

start_urls = "http://quotes.toscrape.com/"


class Dz14Pipeline(object):
    def process_item(self, item, authors):
        engine = create_engine("sqlite:///dz14.db")
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        # print(f"sssssssssssssssssssssss{item}")
        try:
            excist = 0
            if item["keywords"] and item["author"] and item["quote"]:
                name = item["author"]
                name = name[0]
                for person in session.query(Person).all():
                    if f"{name}" == person.author_name:
                        excist = 1
            if excist == 0:
                additional_info = item["additional_info"]
                additional_info_clean = additional_info[10:-13] + "/"
                additional_info_clean_full_path = start_urls + additional_info_clean

                response = requests.get(additional_info_clean_full_path)
                soup = BeautifulSoup(response.text, "lxml")
                birthday = soup.find(class_="author-born-date").get_text(strip=True)
                place = soup.find(class_="author-born-location").get_text(strip=True)
                name = item["author"]
                name = name[0]
                new_person = Person(
                    author_name=f"{name}",
                    additional_info=f"{additional_info_clean_full_path}",
                    birthday_and_place_of_born=f"{birthday} {place}",
                )

                print(f"BBBBBBBBBBBBBBBB {additional_info_clean_full_path}")
                session.add(new_person)
                session.commit()

            if item["keywords"] and item["author"] and item["quote"]:
                cleanquote = item["quote"]
                cleanquote = cleanquote[1:-1] 
                for person in session.query(Person).all():
                    if f"{name}" == person.author_name:
                        id=person.id
                        quotes = Quotes(quote=f"{cleanquote}", author_id=int(id))
                        session.add(quotes)

            if item["keywords"] and item["author"] and item["quote"]:
                kw = []
                for i in item["keywords"]:
                    keywords = Keywords(keyword=f"{i}")
                    kw.append(keywords)
                    session.add(keywords)
                quotes.keywords = kw

            session.commit()

        finally:
            print("aaa")
            #session.close()

        return item


# a= Dz14Pipeline()