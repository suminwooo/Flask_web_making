# daily 기관, 외국인 투자자 크롤링

from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from data.code_data.code_list import code_information
import time
from sqlalchemy import create_engine
import random


class foreigner_instituion_crolling():

    def crolling_naver(self): # 기관,외국인 투자자

        code_list = code_information().code_data()
        final_df = pd.DataFrame(index=range(len(code_list)),
                                columns=['kr_stock_code', 'date', 'institution', 'foreigner', 'foreigner_owned',
                                         'foreigner_percent'])

        for num, code in enumerate(code_list['kr_stock_code']):
            print(num , code)
            code = str(code).zfill(6)
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
            time.sleep(random.uniform(0, 2))

        engine = create_engine("mysql+pymysql://root:" + "0000" + "@127.0.0.1/web_db?charset=utf8",
                               encoding='utf-8')
        conn = engine.connect()
        final_df.to_sql(name='kr_stock_invest_value', con=engine, if_exists='append', index=False)
        conn.close()

        return final_df

print(foreigner_instituion_crolling().crolling_naver())