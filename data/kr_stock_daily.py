from etc.date import date_num
import FinanceDataReader as fdr
import urllib
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import pymysql

import warnings
warnings.filterwarnings('ignore')
data = pd.read_csv('C:/Users/wsm26/Desktop/Flask_web_making/data/raw_data/kospi_code.csv')

code_list = []
for i in data['code']:
    code = str(i)
    if len(code) == 2:
        code = '0000' + code
        code_list.append(code)
    elif len(code) == 3:
        code = '000' + code
        code_list.append(code)
    elif len(code) == 4:
        code = '00' + code
        code_list.append(code)
    elif len(code) == 5:
        code = '0' + code
        code_list.append(code)
    else:
        code_list.append(code)

class kr_stock_daily:

    def daily_data(self): # 기본 가격
        dataframe_test = pd.DataFrame()

        for code in code_list:
            df = fdr.DataReader(code, date_num())
            df = df.reset_index()
            df.columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'close_diff']
            df['code'] = code
            df = df[['code', 'date', 'close', 'close_diff', 'open', 'high', 'low', 'volume']]
            dataframe_test = pd.concat([dataframe_test, df], axis=0)

        final_data = dataframe_test.dropna(axis=0).reset_index()[
            ['code', 'close', 'close_diff', 'open', 'high', 'low', 'volume']]
        final_data.columns = ['kr_stock_code', 'kr_stock_close', 'kr_stock_close_diff', 'kr_stock_open',
                              'kr_stock_high', 'kr_stock_low', 'kr_stock_volume']

        final_data['date'] = date_num()
        final_data = final_data[['kr_stock_code', 'date', 'kr_stock_open', 'kr_stock_close_diff','kr_stock_high', 'kr_stock_low', 'kr_stock_close',
             'kr_stock_volume']]

        return final_data

    def daily_data2(self): # 기관,외국인 투자자자
        final_df = pd.DataFrame(index=range(len(code_list)),
                                columns=['kr_stock_code', 'date', 'institution', 'foreigner', 'foreigner_owned',
                                         'foreigner_percent'])
        for num, code in enumerate(code_list):
            url = 'http://finance.naver.com/item/frgn.nhn?code=' + code + '&page=1'
            html = urlopen(url)
            source = BeautifulSoup(html.read(), "html.parser")
            dataSection = source.find("table", summary="외국인 기관 순매매 거래량에 관한표이며 날짜별로 정보를 제공합니다.")
            dayDataList = dataSection.find_all("tr")

            date = dayDataList[3].find_all("td", class_="tc")[0].text.replace('.', '-')
            institution = dayDataList[3].find_all("td", class_="num")[4].text
            foreigner = dayDataList[3].find_all("td", class_="num")[5].text
            foreigner_owned = dayDataList[3].find_all("td", class_="num")[6].text
            foreigner_percent = dayDataList[3].find_all("td", class_="num")[7].text

            value = [int(code), date, institution, foreigner, foreigner_owned, foreigner_percent]
            final_df.loc[num] = value
        return final_df

