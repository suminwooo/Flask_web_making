# 메인페이지에 들어가는 대부분 데이터 크롤링
# 주요 인덱스 및 시장 지표 데이터

import json
from etc.date import date_method
import requests
from bs4 import BeautifulSoup
import pymysql

class main_page_data_crolling:

    def main_page_value(self):
        URL = "https://finance.naver.com/"

        index1 = requests.get(URL)
        html = index1.text
        soup = BeautifulSoup(html, 'html.parser')
        korea_index_information = soup.find('div', class_='section_stock_market')
        market_index_information = soup.find('div', class_='article2')

        ##### 1. 한국 인덱스
        # 코스피
        kospi = korea_index_information.find('div', class_='kospi_area group_quot quot_opn').text.split(' ')
        kospi_close = kospi[2]
        kospi_change = kospi[3]
        kospi_change_rate = kospi[4]
        kospi_ant = kospi[9].split('\n')[9]
        kospi_foreigner = kospi[9].split('\n')[16]
        kospi_ins = kospi[9].split('\n')[23]

        # 코스닥
        kosdaq = korea_index_information.find('div', class_='kosdaq_area group_quot').text.split(' ')
        kosdaq_close = kosdaq[2]
        kosdaq_change = kosdaq[3]
        kosdaq_change_rate = kosdaq[4]
        kosdaq_ant = kosdaq[9].split('\n')[9]
        kosdaq_foreigner = kosdaq[9].split('\n')[16]
        kosdaq_ins = kosdaq[9].split('\n')[23]

        # 코스피200
        kospi200 = korea_index_information.find('div', class_='kospi200_area group_quot').text.split(' ')
        kospi200_close = kospi200[2]
        kospi200_change = kospi200[3]
        kospi200_change_rate = kospi200[4]

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
        market_wti_gold = market_index_information.find_all('table', class_='tbl_home')[3].text.replace('\n\n',
                                                                                                        '').split('\n')
        wti = market_wti_gold[9]
        wti_rate = market_wti_gold[10].split(' ')

        # 5. 달러인덱스
        dollor_index_link = market_index_information.find_all('table', class_='tbl_home')[1].text.split('\n')
        dollor_index = dollor_index_link[-5]
        dollor_index_rate = dollor_index_link[-4].split(' ')

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
            elif each_value[0] == '보합':
                change_value_list.append(0)
            else:
                change_value = -1 * float(each_value[1])
                change_value_list.append(change_value)

        main_values = [kospi_close, kospi_change, kospi_change_rate, kospi_ant, kospi_foreigner, kospi_ins,
                       kosdaq_close, kosdaq_change, kosdaq_change_rate, kosdaq_ant, kosdaq_foreigner, kosdaq_ins,
                       kospi200_close, kospi200_change, kospi200_change_rate, usd, change_value_list[0], eur,
                       change_value_list[1], jpy, change_value_list[2], wti, change_value_list[3], dollor_index,
                       change_value_list[4], gold, change_value_list[5]]

        market_index_per = []  # 네이버에는 시장 인덱스 %가 존재 하지 않으므로 새로 만들어줌

        for i, j in zip([15, 17, 19, 21, 23, 25], [16, 18, 20, 22, 24, 26]):
            value = str(round(((float(main_values[i].replace(',', '')) - float(main_values[j])) /
                               float(main_values[i].replace(',', '')) - 1) * 100, 2)) + '%'
            market_index_per.append(value)


        main_values_final = [kospi_close, kospi_change, kospi_change_rate, kospi_ant, kospi_foreigner, kospi_ins,
                             kosdaq_close, kosdaq_change, kosdaq_change_rate, kosdaq_ant, kosdaq_foreigner, kosdaq_ins,
                             kospi200_close, kospi200_change, kospi200_change_rate, usd, change_value_list[0],
                             market_index_per[0], eur, change_value_list[1], market_index_per[1], jpy, change_value_list[2],
                             market_index_per[2], wti, change_value_list[3], market_index_per[3], dollor_index, change_value_list[4],
                             market_index_per[4], gold, change_value_list[5], market_index_per[5]]

        return main_values_final


    def world_page_value(self):
        URL = "https://finance.naver.com/world/"

        index1 = requests.get(URL)
        html = index1.text
        soup = BeautifulSoup(html, 'html.parser')
        index = str(soup.find_all('script', language="javascript"))
        america_index = index[index.find('var americaData') + 27:index.find('var asiaData') - 3]
        america_index_dict = json.loads(america_index)
        us_index_list = ['NAS@NDX', 'NAS@IXIC', 'DJI@DJI', 'SPI@SPX']  # 나스닥 100, 나스닥 종합, 다우산업, S&P500 순
        detail_list = ['last', 'diff', 'rate']
        world_value = []
        for i in us_index_list:
            for j in detail_list:
                world_value.append('{}'.format(america_index_dict[i][j]))
        return world_value

    def final_value(self):

        main_value = self.main_page_value()
        world_value = self.world_page_value()
        final_list = [
            main_value[0], main_value[1], main_value[2],
            main_value[6], main_value[7], main_value[8],
            world_value[3], world_value[4], world_value[5],
            world_value[0], world_value[1], world_value[2],
            world_value[6], world_value[7], world_value[8],
            world_value[9], world_value[10], world_value[11],
            main_value[15], main_value[16], main_value[17],
            main_value[18], main_value[19], main_value[20],
            main_value[21], main_value[22], main_value[23],
            main_value[27], main_value[28], main_value[29],
            main_value[30], main_value[31], main_value[23],
            main_value[24], main_value[25], main_value[26],
            main_value[3], main_value[4], main_value[5],
            main_value[9], main_value[10], main_value[11]]

        today_date = date_method().date_num()
        data = [today_date] + final_list

        return data

    def input_main_page_data(self):
        connection = pymysql.connect(host='localhost', user='root', password='0000', charset='utf8', db='web_db')
        cur = connection.cursor()
        sql = "INSERT INTO main_page_data (date,kospi_close,kospi_close_diff,kospi_close_rate,kosdaq_close,kosdaq_close_diff,kosdaq_close_rate,nasdaq_close,nasdaq_close_diff,nasdaq_close_rate,nasdaq100_close,nasdaq100_close_diff,nasdaq100_close_rate,dow_close,dow_close_diff,dow_close_rate,snp500_close,snp500_close_diff,snp500_close_rate,usd_close,usd_close_diff,usd_close_rate,eur_close,eur_close_diff,eur_close_rate,jpy_close,jpy_close_diff,jpy_close_rate,dollorindex_close,dollorindex_close_diff,dollorindex_close_rate,gold_close,gold_close_diff,gold_close_rate,wti_close,wti_close_diff,wti_close_rate,kospi_individual,kospi_foreigner,kospi_Institutional,kosdaq_individual,kosdaq_foreigner,kosdaq_Institutional) VALUES {};".format(
            "(" + str(main_page_data_crolling().final_value())[1:-1] + ")")
        cur.execute(sql)
        connection.commit()
        connection.close()
