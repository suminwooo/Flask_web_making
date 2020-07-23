import requests
from bs4 import BeautifulSoup
import re

import pandas as pd
data = pd.read_csv('kospi_code.csv')

code_list = []
for i in data['code']:
    code = str(i)
    if len(code) == 2 :
        code = '0000'+code
        code_list.append(code)
    elif len(code) == 3 :
        code = '000'+code
        code_list.append(code)
    elif len(code) == 4 :
        code = '00'+code
        code_list.append(code)
    elif len(code) == 5 :
        code = '0'+code
        code_list.append(code)
    else:
        code_list.append(code)

# 시가총액, 코스피 랭킹
URL = "https://finance.naver.com/item/coinfo.nhn?code=005380"
index = requests.get(URL)
html = index.text
soup = BeautifulSoup(html, 'html.parser')

price_info = list(filter(('').__ne__, soup.find('div',class_ = 'rate_info').text.replace('\t', '').split('\n')))
info1 = soup.find('div',class_ = 'aside_invest_info').find('div',class_='first').text.replace('\t','').replace('\n','')
info2 = soup.find('div',class_ = 'aside_invest_info').find('table',class_='rwidth').text.split('\n')
info3 = soup.find('div',class_ = 'aside_invest_info').find('table', class_='per_table')
info4 = soup.find('div',class_ = 'aside_invest_info').find('table', summary="동일업종 PER 정보")

# # OHLCV 정보
# name = price_info[0]
# today_close = price_info[1][5:-3].strip()
# today_close_diff = [price_info[2][-2:], price_info[2][:price_info[2].find('포인트')].strip()]
# today_close_percent = [price_info[3][price_info[3].find('%')+1:].strip(),price_info[3][:price_info[3].find('%')]]
# today_open = price_info[28][:int(len(price_info[28])/2)]
# today_high = price_info[20][:int(len(price_info[20])/2)]
# today_low = price_info[30][:int(len(price_info[30])/2)]
# today_vol = price_info[25]
# print('오늘 종가 : ', today_close)
# print('종가 차이 : ', today_close_diff)
# print('종가 변화율: ', today_close_percent)
# print('시가 : ', today_open)
# print('고가 : ', today_high)
# print('저가 : ', today_low)
# print('거래량 : ', today_vol)
#
#
# # 시가총액, 코스피 랭킹 (info1)
# market_list = ['시가총액시가총액', '시가총액순위', '상장주식수','액면가l매매단위']
# market_list_position = []
# length = []
# for i in range(len(market_list)):
#     length.append(len(market_list[i]))
#     market_list_position.append(info1.find(market_list[i]))
# position_start = [x+y for x,y in zip(market_list_position,length)]
# position_finish = market_list_position+[len(info1)]
# basic_info = []
# for x,y in zip(position_start, position_finish[1:]):
#     basic_info.append(info1[x:y])
# market_value = basic_info[0]
# kospi_rank = basic_info[1]
# total_stock_num = basic_info[2]
# print('시가총액 : ', market_value)
# print('코스피 순위 :', kospi_rank)
# print('상장 주식수 : ', total_stock_num)
#
# # 투자의견 (info2)
# comment = info2[4]
# goal_price = info2[6]
# high_52week = info2[-6]
# low_52week = info2[-4]
# print('투자 의견 : ', comment)
# print('목표 주가 : ', goal_price)
# print('52주 최고: ',high_52week)
# print('52주 최저: ',low_52week)
#
# # PER, EPS, 추정PER,EPS,
# PER = info3.find_all('em')[0].text
# EPS = info3.find_all('em')[1].text
# est_PER = info3.find_all('em')[2].text
# est_EPS = info3.find_all('em')[3].text
# PBR = info3.find_all('em')[4].text
# BPS = info3.find_all('em')[5].text
# DIV = info3.find_all('em')[6].text
# print('PER : ', PER)
# print('EPS : ', EPS)
# print('추정 PER : ',est_PER)
# print('추정 EPS : ', est_EPS)
# print('PBR : ', PBR)
# print('BPS : ',BPS)
# print('배당수익률 : ', DIV)
#
# # 동일 업종 PER, 예상 등락률
# same_ind_per= info4.text.replace('\t','').split('\n')[5]
# same_ind_per_percentage = info4.text.replace('\t','').split('\n')[-4]
# print('동일 업종 PER : ', same_ind_per)
# print('동일 업종 PER 예상 등락률 : ', same_ind_per_percentage)