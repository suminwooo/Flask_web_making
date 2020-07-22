# <S&P500 data> <- 미국 가치 종목으로 사용

import pandas as pd
import requests
from bs4 import BeautifulSoup

URL = "https://www.slickcharts.com/sp500"

index1 = requests.get(URL)
html = index1.text
soup = BeautifulSoup(html, 'html.parser')
test = soup.find('div', class_='table-responsive').text.split('\n')


inc_name, inc_code, price, change, change_per = [],[],[],[],[]
for i in range(15,4507,9):
    inc_name.append(test[i+1])
    inc_code.append(test[i+2])
    price.append(test[i+4])
    change.append(test[i+5])
    change_per.append(test[i+6])

movements = []
for i in change:
    if float(i)>0:
        movements.append('상승')
    elif float(i) == 0:
        movements.append('보합')
    else:
        movements.append('하락')


data = [inc_name, inc_code, price, change, change_per, movements]

df = pd.DataFrame(data).T
df.columns = ['inc_name', 'inc_code', 'price', 'change', 'change_per', 'movements']
print(df)
# df.to_csv('s&p500.csv')

