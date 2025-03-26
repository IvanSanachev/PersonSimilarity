import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import datetime
url = "https://lenta.ru/news/"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
}
d = datetime.datetime.now()
data = pd.DataFrame(columns=['text', 'urls'])
for i in tqdm(range(3650)):
    d -= datetime.timedelta(days=1)
    for pg in range(1, 21):
        answer = requests.get(url + d.strftime('%Y/%m/%d') + f'/page/{pg}/', headers=headers)
        soup = BeautifulSoup(answer.text)
        for j in soup.find_all('a', {'class': 'card-full-news _archive'}):
            news = j.get('href', '')
            text = ''
            nwsans = requests.get('https://lenta.ru/' + str(news), headers=headers)
            nws = BeautifulSoup(nwsans.text)
            for el in nws.find_all('p', attrs={'class': 'topic-body__content-text'}):
                text += el.text
            data.loc[len(data)] = {'text': text, 'urls': 'https://lenta.ru/' + str(news)}
pd.DataFrame(data).to_csv('lenta.csv', index=False)