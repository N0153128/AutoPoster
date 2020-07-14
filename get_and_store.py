# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
from peewee import *
from random import randint
from time import sleep

db = SqliteDatabase('storage.db', autoconnect=True)


class Quotes(Model):
    quote = CharField()
    author = CharField()

    class Meta:
        database = db
        indexes = (
            (('quote', 'author'), True),
        )


db.create_tables([Quotes])


class GetAndStoreAndMore:

    # def __init__(self):
    #     self.
    #     self.

    def get(self):
        url = 'https://ru.citaty.net/tsitaty/sluchainaia-tsitata/'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        quote = soup.find('h3', class_='blockquote-text')
        q = quote.a['title'][17:].split('“ —')[0].strip('„')
        a = quote.a['title'][17:].split('“ —')[1].strip('„')
        return q, a

    def add_quote(self, quote_):
        try:
            query = Quotes(quote=quote_[0], author=quote_[1])
            query.save()
        except Exception as e:
            print(e)
            pass

    def list_quotes(self):
        all = []
        for i in Quotes.select():
            quo = (i.id, i.quote, i.author)
            all.append(quo)
        return all

    def clear_all(self):
        for i in Quotes.select():
            query = i.delete()
            query.execute()

    def get_random_quote(self):
        try:
            return self.list_quotes()[randint(1, len(self.list_quotes())-1)][1]
        except IndexError:
            self.get_random_quote()

    def add_lots(self, lots):
        for i in range(lots):
            self.add_quote(self.get())
            sleep(1)


    def add_particular(self, q, a):
        try:
            query = Quotes(quote=q, author=a)
            query.save()
        except Exception as e:
            print(e)
            pass

obj = GetAndStoreAndMore()
