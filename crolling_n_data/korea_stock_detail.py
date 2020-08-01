import requests
from bs4 import BeautifulSoup
import pandas as pd

data = pd.read_csv('raw_data/kospi_code.csv')

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

final_raw_data = []

for num, i in enumerate(code_list):
    print(num,'번째 진행중 : ',i)
    final_raw_data.append(i)
    # 시가총액, 코스피 랭킹
    URL = "https://finance.naver.com/item/main.nhn?code=005380"
    index = requests.get(URL.format(i))
    html = index.text
    soup = BeautifulSoup(html, 'html.parser')

    price_info = list(filter(('').__ne__, soup.find('div',class_ = 'rate_info').text.replace('\t', '').split('\n')))
    info1 = soup.find('div',class_ = 'aside_invest_info').find('div',class_='first').text.replace('\t','').replace('\n','')
    info2 = soup.find('div',class_ = 'aside_invest_info').find('table',class_='rwidth').text.split('\n')
    info3 = soup.find('div',class_ = 'aside_invest_info').find('table', class_='per_table')
    info4 = soup.find('div',class_ = 'aside_invest_info').find('table', summary="동일업종 PER 정보")

    # OHLCV 정보
    name = price_info[0]
    today_close = price_info[1][5:-3].strip()
    today_close_diff = [price_info[2][-2:], price_info[2][:price_info[2].find('포인트')].strip()]
    today_close_percent = [price_info[3][price_info[3].find('%')+1:].strip(),price_info[3][:price_info[3].find('%')]]
    today_open = price_info[28][:int(len(price_info[28])/2)]
    today_high = price_info[20][:int(len(price_info[20])/2)]
    today_low = price_info[30][:int(len(price_info[30])/2)]
    today_vol = price_info[25]
    final_raw_data.append(today_close)
    final_raw_data.append(today_close_diff)
    final_raw_data.append(today_close_percent)
    final_raw_data.append(today_open)
    final_raw_data.append(today_high)
    final_raw_data.append(today_low)
    final_raw_data.append(today_vol)


    # 시가총액, 코스피 랭킹 (info1)
    market_list = ['시가총액시가총액', '시가총액순위', '상장주식수','액면가l매매단위']
    market_list_position = []
    length = []
    for i in range(len(market_list)):
        length.append(len(market_list[i]))
        market_list_position.append(info1.find(market_list[i]))
    position_start = [x+y for x,y in zip(market_list_position,length)]
    position_finish = market_list_position+[len(info1)]
    basic_info = []
    for x,y in zip(position_start, position_finish[1:]):
        basic_info.append(info1[x:y])
    market_value = basic_info[0]
    kospi_rank = basic_info[1]
    total_stock_num = basic_info[2]
    final_raw_data.append(market_value)
    final_raw_data.append(kospi_rank)
    final_raw_data.append(total_stock_num)

    # 투자의견 (info2)
    comment = info2[4]
    goal_price = info2[6]
    high_52week = info2[-6]
    low_52week = info2[-4]
    final_raw_data.append(comment)
    final_raw_data.append(goal_price)
    final_raw_data.append(high_52week)
    final_raw_data.append(low_52week)

    # PER, EPS, 추정PER,EPS,
    PER = info3.find_all('em')[0].text
    EPS = info3.find_all('em')[1].text
    est_PER = info3.find_all('em')[2].text
    est_EPS = info3.find_all('em')[3].text
    PBR = info3.find_all('em')[4].text
    BPS = info3.find_all('em')[5].text
    DIV = info3.find_all('em')[6].text
    final_raw_data.append(PER)
    final_raw_data.append(EPS)
    final_raw_data.append(est_PER)
    final_raw_data.append(est_EPS)
    final_raw_data.append(PBR)
    final_raw_data.append(BPS)
    final_raw_data.append(DIV)

    # 동일 업종 PER, 예상 등락률
    same_ind_per= info4.text.replace('\t','').split('\n')[5]
    same_ind_per_percentage = info4.text.replace('\t','').split('\n')[-4]
    final_raw_data.append(same_ind_per)
    final_raw_data.append(same_ind_per_percentage)