from bs4 import BeautifulSoup
import requests
from peewee import *


db = SqliteDatabase('storage.db', autoconnect=True)


class Quotes(Model):
    quote = CharField()
    author = CharField()

    class Meta:
        database = db


db.create_tables([Quotes])


class GetAndStoreAndMore:

    def __init__(self):
        self.url = 'https://ru.citaty.net/tsitaty/sluchainaia-tsitata/'
        self.page = requests.get(self.url)

    def get(self):
        soup = BeautifulSoup(self.page.content, 'html.parser')
        quote = soup.find('h3', class_='blockquote-text')
        q = quote.a['title'][17:].split('“ —')[0].strip('\\xa0').strip('„')
        a = quote.a['title'][17:].split('“ —')[1].strip('\\xa0').strip('„')
        return q, a

    def add_quote(self, quote_):
        query = Quotes(quote=quote_[0], author=quote_[1])
        query.save()

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


obj = GetAndStoreAndMore()
