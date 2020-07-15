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

    @staticmethod
    def get():
        url = 'https://ru.citaty.net/tsitaty/sluchainaia-tsitata/'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        quote = soup.find('h3', class_='blockquote-text')
        q = quote.a['title'][17:].split('“ —')[0].strip('„')
        a = quote.a['title'][17:].split('“ —')[1].strip('„')
        return q, a

    @staticmethod
    def add_quote(quote_):
        try:
            query = Quotes(quote=quote_[0], author=quote_[1])
            query.save()
        except Exception as e:
            print(e)
            pass

    @staticmethod
    def list_quotes():
        all = []
        for i in Quotes.select():
            quo = (i.id, i.quote, i.author)
            all.append(quo)
        return all

    @staticmethod
    def clear_all():
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

    def add_ten(self):
        for i in range(10):
            self.add_quote(self.get())
            sleep(0.5)

    def add_hundred(self):
        for i in range(100):
            self.add_quote(self.get())
            sleep(0.5)

    @staticmethod
    def add_particular(q, a):
        try:
            query = Quotes(quote=q, author=a)
            query.save()
        except Exception as e:
            print(e)
            pass


obj = GetAndStoreAndMore()
