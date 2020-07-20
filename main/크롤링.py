# 네이버 국내 증시 메인 페이지

import requests
from bs4 import BeautifulSoup

URL = "https://finance.naver.com/"

index1 = requests.get(URL)
html = index1.text
soup = BeautifulSoup(html, 'html.parser')
korea_index_information = soup.find('div',class_='section_stock_market')
us_index_information = soup.find('div',class_='group_aside')
market_index_information = soup.find('div',class_='article2')

##### 1. 한국 인덱스
# 코스피
kospi = korea_index_information.find('div',class_='kospi_area group_quot quot_opn').text.split(' ')
kospi_close = kospi[2]
kospi_change = kospi[3]
kospi_change_rate = kospi[4]
kospi_ant = kospi[9].split('\n')[9]
kospi_foreigner = kospi[9].split('\n')[16]
kospi_ins = kospi[9].split('\n')[23]
print('코스피 현재가 : ', kospi_close)
print('코스피 변화 : ', kospi_change)
print('코스피 변화율 : ', kospi_change_rate)
print('코스피 개인: ', kospi_ant)
print('코스피 외국인: ', kospi_foreigner)
print('코스피 기관: ', kospi_ins)


# 코스닥
kosdaq = korea_index_information.find('div',class_='kosdaq_area group_quot').text.split(' ')
kosdaq_close = kosdaq[2]
kosdaq_change = kosdaq[3]
kosdaq_change_rate = kosdaq[4]
kosdaq_ant = kosdaq[9].split('\n')[9]
kosdaq_foreigner = kosdaq[9].split('\n')[16]
kosdaq_ins = kosdaq[9].split('\n')[23]
print('코스닥 현재가 : ', kosdaq_close)
print('코스닥 변화 : ', kosdaq_change)
print('코스닥 변화율 : ', kosdaq_change_rate)
print('코스닥 개인: ', kosdaq_ant)
print('코스닥 외국인: ', kosdaq_foreigner)
print('코스닥 기관: ', kosdaq_ins)

# 코스피200
kospi200 = korea_index_information.find('div',class_='kospi200_area group_quot').text.split(' ')
kospi200_close = kospi200[2]
kospi200_change = kospi200[3]
kospi200_change_rate = kospi200[4]
print('코스피200 현재가 : ', kospi200_close)
print('코스피200 변화 : ', kospi200_change)
print('코스피200 변화율 : ', kospi200_change_rate)



##### 2. 미국 인덱스
us_index = us_index_information.find('tbody').text.split(' ')
nasdaq = us_index[2:4]
nasdaq_close = nasdaq[0].split('\n')[1]
nasdaq_change = [nasdaq[0].split('\n')[2],nasdaq[1].split('\n')[0]]
print('나스닥 현재가 : ', nasdaq_close)
print('나스닥 변화 : ', nasdaq_change)


# 2. 다우 산업
dow = us_index[0:2]
dow_close = dow[0].split('\n')[3]
dow_change = [dow[0].split('\n')[4],dow[1].split('\n')[0]]
print('다우산업 현재가 : ', dow_close)
print('다우산업 변화 : ', dow_change)

##### 기타 인덱스
exchange = market_index_information.find('tbody')
# 1. 달러
usd = exchange.find_all('td')[0].text
usd_rate = exchange.find_all('td')[1].text.split(' ')
print('달러 : ', usd)
print('달러 변화율 : ',usd_rate)
# 2. 유로
eur = exchange.find_all('td')[2].text
eur_rate = exchange.find_all('td')[3].text.split(' ')
print('유로 : ', eur)
print('유로 변화율 : ', eur_rate)
# 3. 엔화
jpy = exchange.find_all('td')[4].text
jpy_rate = exchange.find_all('td')[5].text.split(' ')
print('엔화 : ', jpy)
print('엔화 변화율 : ', jpy_rate)
# 4. WTI
market_wti_gold = market_index_information.find_all('tr',class_='down bold')
wti = market_wti_gold[2].text.split('\n')[2:4][0]
wti_rate = market_wti_gold[2].text.split('\n')[2:4][1].split(' ')
print('wti 인덱스 : ',wti)
print('wti 변화율 : ',wti_rate)

# 5. 달러인덱스
dollor_index = market_wti_gold[1].text.split('\n')[2:4][0]
dollor_index_rate = market_wti_gold[1].text.split('\n')[2:4][1].split(' ')

print('달러 인덱스 : ',dollor_index)
print('달러 인덱스 변화율 : ',dollor_index_rate)


# 5. 금

market_gold = market_index_information.find_all('div', class_="group2")[-1]
gold = market_gold.find("tbody").text.split("\n")[3]
gold_rate = market_gold.find("tbody").text.split("\n")[4].split(' ')
print('골드 : ', gold)
print('골드 변화율 : ', gold_rate)