# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
from peewee import *
from random import randint
from time import sleep
from newbot import Bot

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


class GetAndStoreAndMore(Bot):

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
        all_ = []
        for i in Quotes.select():
            quo = (i.id, i.quote, i.author)
            all_.append(quo)
        return all_

    @staticmethod
    def clear_all():
        for i in Quotes.select():
            query = i.delete()
            query.execute()

    def get_random_quote(self, raw=None):
        if raw is not None:
            try:
                q = self.list_quotes()[randint(1, len(self.list_quotes())-1)]
                return q
            except IndexError:
                self.get_random_quote()
        elif raw is None:
            try:
                q = self.list_quotes()[randint(1, len(self.list_quotes())-1)]
                return f'{q[1]} \n \n ©{q[2]}'
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

    def add_thosand(self):
        for i in range(1000):
            self.add_quote(self.get())
            sleep(0.5)

    def add_ten_thousand(self):
        for i in range(10000):
            self.add_quote(self.get())
            sleep(0.5)

    def add_100000(self):
        for i in range(100000):
            self.add_quote(self.get())
            sleep(0.5)

    def get_first(self):
        bag = self.list_quotes()
        return bag[0]

    def get_last(self):
        bag = self.list_quotes()
        return bag[-1]

    def remove_first(self):
        query = Quotes.delete().where(Quotes.id == self.get_first()[0])
        query.execute()

    def remove_last(self):
        query = Quotes.delete().where(Quotes.id == self.get_last()[0])
        query.execute()

    @staticmethod
    def add_particular(q, a):
        try:
            query = Quotes(quote=q, author=a)
            query.save()
        except Exception as e:
            print(e)
            pass

    async def begin_push(self, item):
        while True:
            quote = self.get_first()
            await self.send_message(item, chat_id='@known_quotes', message=f'{quote[1]}\n \n ©{quote[2]}')
            self.remove_first()
            sleep(8640)


obj = GetAndStoreAndMore()
