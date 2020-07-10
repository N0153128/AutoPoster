import requests

r = requests.get('https://ru.citaty.net/tsitaty/sluchainaia-tsitata/')

with open('file.txt', 'wb') as f:
    f.write(r.content)

