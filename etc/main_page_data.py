# 네이버 국내 증시 메인 페이지

import requests
from bs4 import BeautifulSoup


def main_page_value():
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



    # 코스닥
    kosdaq = korea_index_information.find('div',class_='kosdaq_area group_quot').text.split(' ')
    kosdaq_close = kosdaq[2]
    kosdaq_change = kosdaq[3]
    kosdaq_change_rate = kosdaq[4]
    kosdaq_ant = kosdaq[9].split('\n')[9]
    kosdaq_foreigner = kosdaq[9].split('\n')[16]
    kosdaq_ins = kosdaq[9].split('\n')[23]


    # 코스피200
    kospi200 = korea_index_information.find('div',class_='kospi200_area group_quot').text.split(' ')
    kospi200_close = kospi200[2]
    kospi200_change = kospi200[3]
    kospi200_change_rate = kospi200[4]




    # ##### 2. 미국 인덱스
    # us_index = us_index_information.find('tbody').text.split(' ')
    # nasdaq = us_index[2:4]
    # nasdaq_close = nasdaq[0].split('\n')[1]
    # nasdaq_change = [nasdaq[0].split('\n')[2],nasdaq[1].split('\n')[0]]
    #
    #
    #
    # # 2. 다우 산업
    # dow = us_index[0:2]
    # dow_close = dow[0].split('\n')[3]
    # dow_change = [dow[0].split('\n')[4],dow[1].split('\n')[0]]


    ##### 기타 인덱스
    exchange = market_index_information.find('tbody')
    # 1. 달러
    usd = exchange.find_all('td')[0].text
    usd_rate = exchange.find_all('td')[1].text.split(' ')

    # 2. 유로
    eur = exchange.find_all('td')[2].text
    eur_rate = exchange.find_all('td')[3].text.split(' ')

    # 3. 엔화
    jpy = exchange.find_all('td')[4].text
    jpy_rate = exchange.find_all('td')[5].text.split(' ')

    # 4. WTI
    wti = market_index_information.text.split('\n')[164]
    wti_rate = market_index_information.text.split('\n')[165].split(' ')


    # 5. 달러인덱스
    dollor_index = market_index_information.text.split('\n')[84]
    dollor_index_rate = market_index_information.text.split('\n')[85].split(' ')



    # 5. 금

    market_gold = market_index_information.find_all('div', class_="group2")[-1]
    gold = market_gold.find("tbody").text.split("\n")[3]
    gold_rate = market_gold.find("tbody").text.split("\n")[4].split(' ')

    # 시장지표의 변화율은 (상승or하락, float)의 형태로 나옴 -> +와 -로 변경해줌
    change_value_list = []
    for each_value in [usd_rate, eur_rate, jpy_rate, wti_rate, dollor_index_rate, gold_rate]:
        if each_value[0] == "상승":
            change_value = float(each_value[1])
            change_value_list.append(change_value)
        else:
            change_value = -1 * float(each_value[1])
            change_value_list.append(change_value)

    values = [kospi_close, kospi_change, kospi_change_rate, kospi_ant, kospi_foreigner, kospi_ins,
              kosdaq_close, kosdaq_change, kosdaq_change_rate, kosdaq_ant, kosdaq_foreigner, kosdaq_ins,
              kospi200_close, kospi200_change, kospi200_change_rate, usd, change_value_list[0], eur,
              change_value_list[1], jpy, change_value_list[2], wti, change_value_list[3], dollor_index,
              change_value_list[4], gold, change_value_list[5]]

    return values
# # 재무제표 부분
#
# import requests
# from bs4 import BeautifulSoup
#
# URL = "https://finance.naver.com/sise/sise_index.nhn?code=KOSPI"
#
# index1 = requests.get(URL)
# html = index1.text
# soup = BeautifulSoup(html, 'html.parser')
# keywords = soup.find_all('div',class_='subtop_sise_detail')
#
# print(keywords)