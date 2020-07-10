from bs4 import BeautifulSoup
import requests


class GetAndStore:

    def __init__(self):
        self.url = 'https://ru.citaty.net/tsitaty/sluchainaia-tsitata/'
        self.page = requests.get(self.url)

    def get(self):
        soup = BeautifulSoup(self.page.content, 'html.parser')
        quote = soup.find('h3', class_='blockquote-text')
        q = quote.a['title'][17:].split('“ —')[0].strip('\\xa0').strip('„')
        a = quote.a['title'][17:].split('“ —')[1].strip('\\xa0').strip('„')
        return q, a


obj = GetAndStore()

print(obj.get()[1])
