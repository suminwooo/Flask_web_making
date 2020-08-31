import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import urllib
import time

from urllib.request import urlopen
from bs4 import BeautifulSoup

class foreinger_institurion():

    # 매일 업데이트 되는 부분(네이버에서 탑 6 크롤링)
    def daily_foreinger_institurion_crolling(self):
        URL = "https://finance.naver.com/sise/"

        index1 = requests.get(URL)
        html = index1.text
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('div', id='contentarea_left')

        total_df = pd.DataFrame()

        foreigner_buy = []
        for i in table.find_all('table')[2].text.replace('\t', '').split('\n'):
            if len(i) > 0:
                foreigner_buy.append(i)
        foreigner_buy = foreigner_buy[1:]
        foreigner_buy_df = pd.DataFrame(np.array(foreigner_buy).reshape(-1, 4))
        total_df = pd.concat([total_df, foreigner_buy_df], axis=0)

        foreigner_sell = []
        for i in table.find_all('table')[3].text.replace('\t', '').split('\n'):
            if len(i) > 0:
                foreigner_sell.append(i)
        foreigner_sell = foreigner_sell[1:]
        foreigner_sell_df = pd.DataFrame(np.array(foreigner_sell).reshape(-1, 4))
        total_df = pd.concat([total_df, foreigner_sell_df], axis=0)

        institution_buy = []
        for i in table.find_all('table')[4].text.replace('\t', '').split('\n'):
            if len(i) > 0:
                institution_buy.append(i)
        institution_buy = institution_buy[1:]
        institution_buy_df = pd.DataFrame(np.array(institution_buy).reshape(-1, 4))
        total_df = pd.concat([total_df, institution_buy_df], axis=0)

        institurion_sell = []
        for i in table.find_all('table')[5].text.replace('\t', '').split('\n'):
            if len(i) > 0:
                institurion_sell.append(i)
        institurion_sell = institurion_sell[1:]
        institurion_sell_df = pd.DataFrame(np.array(institurion_sell).reshape(-1, 4))
        total_df = pd.concat([total_df, institurion_sell_df], axis=0)
        total_df.columns = ['kr_stock_name', 'close', '상승or하락', '변동율']
        total_df = total_df.reset_index()
        total_df = total_df[['kr_stock_name', 'close', '상승or하락', '변동율']]

        total_df['change'] = None
        for i in range(len(total_df)):
            if total_df.loc[i]['상승or하락'] == '상승':
                total_df.loc[i]['change'] = int(total_df.loc[i]['변동율'].replace(',', ''))
            elif total_df.loc[i]['상승or하락'] == '하락':
                total_df.loc[i]['change'] = -1 * int(total_df.loc[i]['변동율'].replace(',', ''))
            else:
                total_df.loc[i]['change'] = 0
        total_df['date'] = '2020-08-31'
        total_df['close'] = [int(i.replace(",","")) for i in total_df['close']]
        total_df = total_df[['kr_stock_name','date', 'close', 'change']]

        return total_df

    # 매일 크롤링 부분 DB저장
    def daily_data_to_mysql(self):
        data = self.daily_foreinger_institurion_crolling()
        engine = create_engine("mysql+pymysql://root:" + "0000" + "@127.0.0.1/web_db?charset=utf8",
                               encoding='utf-8')
        conn = engine.connect()
        data.to_sql(name='kr_stock_foringer_instition', con=engine, if_exists='append', index=False)
        return data

    def show_seach_page_foreigner_instition(self,code):

        url = 'http://finance.naver.com/item/frgn.nhn?code=' + code
        html = urlopen(url)
        source = BeautifulSoup(html.read(), "html.parser")
        dataSection = source.find("table", summary="외국인 기관 순매매 거래량에 관한표이며 날짜별로 정보를 제공합니다.")
        dayDataList = dataSection.find_all("tr")

        day_list = []
        institutionPureDealing_list = []
        foreignerPureDealing_list = []
        ownedVolumeByForeigner_list = []
        ownedRateByForeigner_list = []

        for i in range(3, 10):
            if (len(dayDataList[i].find_all("td", class_="tc")) != 0 and len(
                    dayDataList[i].find_all("td", class_="num")) != 0):
                day = dayDataList[i].find_all("td", class_="tc")[0].text
                institutionPureDealing = dayDataList[i].find_all("td", class_="num")[4].text
                foreignerPureDealing = dayDataList[i].find_all("td", class_="num")[5].text
                ownedVolumeByForeigner = dayDataList[i].find_all("td", class_="num")[6].text
                ownedRateByForeigner = dayDataList[i].find_all("td", class_="num")[7].text
                day_list.append(day)
                institutionPureDealing_list.append(institutionPureDealing)
                foreignerPureDealing_list.append(foreignerPureDealing)
                ownedVolumeByForeigner_list.append(ownedVolumeByForeigner)
                ownedRateByForeigner_list.append(ownedRateByForeigner)
        final_df = pd.DataFrame(
            [day_list, institutionPureDealing_list, foreignerPureDealing_list, ownedVolumeByForeigner_list,
             ownedRateByForeigner_list]).T
        final_df.columns = ['date', 'institutionPureDealing', 'foreignerPureDealing', 'ownedVolumeByForeigner',
                            'ownedRateByForeigner']

        return final_df

print(foreinger_institurion().show_seach_page_foreigner_instition('005930'))