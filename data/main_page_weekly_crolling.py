# 메인 페이지 데이터 내용
# 일주일에 한번 크롤링 하는 데이터

from etc.date import date_method
import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
import pymysql


# 메인 페이지 데이터 내용
# 일주일에 한번 크롤링 하는 데이터

import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
import pymysql


class kr_stock_weekly:

    def kr_stock_code_list(self):
        connection = None
        try:
            connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password='0000',
                                         db='web_db',
                                         port=3306,
                                         charset='utf8')

            with connection.cursor() as cursor:
                sql = "SELECT kr_stock_code FROM kr_stock_list;"
                cursor.execute(sql)
                kr_stock_list = cursor.fetchall()

            self.kr_stock_list = [i[0] for i in kr_stock_list]

        except Exception as e:
            print('->', e)

        finally:
            if connection:
                connection.close()

        return kr_stock_list

    def weekly_data(self):

        code_list = [str(i[0]).zfill(6) for i in kr_stock_weekly().kr_stock_code_list()]
        final_set = []
        for num,code in enumerate(code_list):
            if num in list(range(0,10000,100)):
                print(round(num/len(code_list),2),'% 완료')
            # 시가총액, 코스피 랭킹
            try:
                URL = "https://finance.naver.com/item/main.nhn?code={}"
                index = requests.get(URL.format(code))
                html = index.text
                soup = BeautifulSoup(html, 'html.parser')

                price_info = list(
                    filter(('').__ne__, soup.find('div', class_='rate_info').text.replace('\t', '').split('\n')))
                info1 = soup.find('div', class_='aside_invest_info').find('div', class_='first').text.replace('\t','').replace('\n', '')
                info2 = soup.find('div', class_='aside_invest_info').find('table', class_='rwidth').text.split('\n')
                info3 = soup.find('div', class_='aside_invest_info').find('table', class_='per_table')
                info4 = soup.find('div', class_='aside_invest_info').find('table', summary="동일업종 PER 정보")

                # OHLCV 정보
                today_close = price_info[1][5:-3].strip()
                today_close_diff = [price_info[2][-2:], price_info[2][:price_info[2].find('포인트')].strip()]
                today_close_percent = [price_info[3][price_info[3].find('%') + 1:].strip(),
                                       price_info[3][:price_info[3].find('%')]]
                today_open = price_info[28][:int(len(price_info[28]) / 2)]
                today_high = price_info[20][:int(len(price_info[20]) / 2)]
                today_low = price_info[30][:int(len(price_info[30]) / 2)]
                today_vol = price_info[25]

                # 시가총액, 코스피 랭킹 (info1)
                market_list = ['시가총액시가총액', '시가총액순위', '상장주식수', '액면가l매매단위']
                market_list_position = []
                length = []
                for i in range(len(market_list)):
                    length.append(len(market_list[i]))
                    market_list_position.append(info1.find(market_list[i]))
                position_start = [x + y for x, y in zip(market_list_position, length)]
                position_finish = market_list_position + [len(info1)]
                basic_info = []
                for x, y in zip(position_start, position_finish[1:]):
                    basic_info.append(info1[x:y])
                market_value = basic_info[0]
                kospi_rank = basic_info[1]

                # 투자의견 (info2)
                comment = info2[4]
                goal_price = info2[6]
                high_52week = info2[-6]
                low_52week = info2[-4]

                # PER, EPS, 추정PER,EPS,
                PER = info3.find_all('em')[0].text
                EPS = info3.find_all('em')[1].text
                est_PER = info3.find_all('em')[2].text
                est_EPS = info3.find_all('em')[3].text
                PBR = info3.find_all('em')[4].text
                BPS = info3.find_all('em')[5].text
                DIV = info3.find_all('em')[6].text

                # 동일 업종 PER, 예상 등락률
                same_ind_per = info4.text.replace('\t', '').split('\n')[5]
                same_ind_per_percentage = info4.text.replace('\t', '').split('\n')[-4]

                # close_diff 값 차이 수정
                i = today_close_diff
                try:
                    if i[0] == '하락':
                        close_diff = -1 * float(i[1].replace(",", ''))
                        today_close_diff = close_diff
                    elif i[0] == '상승':
                        close_diff = float(i[1].replace(",", ''))
                        today_close_diff = close_diff
                    else:
                        close_diff = float(i[1].replace(",", ''))
                        today_close_diff = close_diff
                except:
                    today_close_diff = close_diff

                # close_change 값 수정
                j = today_close_percent
                try:
                    if j[0] == '마이너스':
                        close_change = -1 * float(j[1].replace(",", ''))
                        today_close_percent = close_change
                    elif i[0] == '플러스':
                        close_change = float(j[1].replace(",", ''))
                        today_close_percent = close_change
                    else:
                        today_close_percent = j[1]
                except:
                    today_close_percent = close_change

                final_value = [code, '2020-09-04', today_close, today_close_diff, today_close_percent, today_open, today_high,
                               today_low, today_vol, market_value,
                               kospi_rank, comment, goal_price, high_52week, low_52week, PER, EPS, est_PER, est_EPS, PBR,
                               BPS, DIV, same_ind_per,
                               same_ind_per_percentage]
            except:
                final_value = [code,'2020-09-04', 'NAN']

            final_set.append(final_value)
        data = pd.DataFrame(columns=['code', 'date', 'close', 'close_diff', 'close_percent', 'open', 'high', 'low', 'vol',
                                     'market_value', 'kospi_rank', 'comment', 'goal_price', 'high_52week', 'low_52week',
                                     'PER',
                                     'EPS', 'est_PER', 'est_EPS', 'PBR', 'BPS', 'DIV', 'same_ind_per',
                                     'same_ind_per_percentage'])
        for i in range(len(final_set)):
            if len(final_set[i]) == 24:
                data.loc[i] = final_set[i]
            else:
                data.loc[i] = final_set[i] + ['NAN', 'NAN', 'NAN', 'NAN', 'NAN', 'NAN', 'NAN', 'NAN', 'NAN', 'NAN', 'NAN',
                                              'NAN', 'NAN', 'NAN', 'NAN', 'NAN',
                                              'NAN', 'NAN', 'NAN', 'NAN', 'NAN']
        data.columns = ['kr_stock_code', 'date','kr_stock_close','kr_stock_close_diff', 'kr_stock_close_percent',
             'kr_stock_open', 'kr_stock_high', 'kr_stock_low', 'kr_stock_vol', 'kr_stock_market_value', 'kr_stock_kospi_rank',
             'kr_stock_comment', 'kr_stock_goal_price', 'kr_stock_high_52week', 'kr_stock_low_52week','kr_stock_PER','kr_stock_EPS',
             'kr_stock_est_PER', 'kr_stock_est_EPS', 'kr_stock_PBR', 'kr_stock_BPS', 'kr_stock_DIV', 'kr_stock_same_ind_per',
             'kr_stock_same_ind_per_percentage']
        return data

    def weekly_data_to_db(self):
        data = kr_stock_weekly().weekly_data()
        # DB 엔진
        engine = create_engine("mysql+pymysql://root:" + "0000" + "@127.0.0.1/web_db?charset=utf8",
                               encoding='utf-8')
        conn = engine.connect()
        data.to_sql(name='kr_stock_weekly', con=engine, if_exists='append', index=False)

    def weekly_data_to_python(self):
        connection = None
        try:
            connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password='0000',
                                         db='web_db',
                                         port=3306,
                                         charset='utf8')

            with connection.cursor() as cursor:
                sql = "SELECT * " \
                      "FROM kr_stock_weekly " \
                      "WHERE DATE = (select DATE " \
                      "FROM kr_stock_weekly " \
                      "group BY DATE " \
                      "order by date DESC " \
                      "LIMIT 1);"
                cursor.execute(sql)
                data = cursor.fetchall()

        except Exception as e:
            print('->', e)

        finally:
            if connection:
                connection.close()

        return data