# 재무제표 부분

import requests
from bs4 import BeautifulSoup

URL = "https://finance.naver.com/sise/sise_index.nhn?code=KOSPI"

index1 = requests.get(URL)
html = index1.text
soup = BeautifulSoup(html, 'html.parser')
keywords = soup.find_all('div',class_='subtop_sise_detail')

print(keywords)
