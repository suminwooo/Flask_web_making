# API 로 뿌려주는 데이터

import pymysql
import pandas as pd

# 메인 페이지 데이터
class total_stock_list:
    def stock_information(self):
        connection = None
        row = None
        try:
            connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password='0000',
                                         db='web_db',
                                         port=3306,
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)

            with connection.cursor() as cursor:
                sql = "SELECT kr_stock_code, kr_stock_name " \
                      "FROM kr_stock_list;"
                cursor.execute(sql)
                row = cursor.fetchall()

        except Exception as e:
            print('->', e)

        finally:
            if connection:
                connection.close()
        return row

# 개별 주식 정보 뿌려주기
class stock_all_info:
    def price(self):
        connection = None
        try:
            connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password='0000',
                                         db='web_db',
                                         port=3306,
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)
            if connection:

                with connection.cursor() as cursor:
                    sql = "SELECT kr_stock_code, DATE, kr_stock_open, kr_stock_high, kr_stock_low, kr_stock_close " \
                               "FROM kr_stock_daily " \
                               "WHERE kr_stock_code ='5930' " \
                               "ORDER BY DATE DESC " \
                               "LIMIT 100;"
                    cursor.execute(sql)
                    data = cursor.fetchall()
                    data = pd.read_sql_query(sql, connection)
                    data = data[['DATE','kr_stock_open','kr_stock_high','kr_stock_low','kr_stock_close']]
                    data['DATE'] = [str(i) for i in data['DATE']]
                    data_dic = data.to_dict('index')

        except Exception as e:
            print('->', e)

        finally:
            if connection:
                connection.close()

        return data_dic

# 한국 종목 상세 검색 부분
class korea_detail_information:

    def kr_price_data(self, code):

        connection = None
        try:
            connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password='0000',
                                         db='web_db',
                                         port=3306,
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)
            if connection:
                # print('DB 오픈')
                with connection.cursor() as cursor:
                    # 최신 date 출력
                    date_sql = "select DATE " \
                               "FROM kr_stock_daily " \
                               "group BY DATE " \
                               "order by date DESC " \
                               "LIMIT 1;"
                    cursor.execute(date_sql)
                    date_data = str(cursor.fetchall())
                    first_index = date_data.find('(') + 1  # 형태가 이상해서 (,)위치 활용해 날짜 추출
                    second_index = date_data.find(')')
                    date_data = [i.strip() for i in date_data[first_index:second_index].split(',')]
                    if len(date_data[1]) == 1:
                        date_data[1] = '0' + date_data[1]
                    if len(date_data[2]) == 1:
                        date_data[2] = '0' + date_data[2]
                    recently_date = date_data[0] + '-' + date_data[1] + '-' + date_data[2]

                    data_sql = "SELECT * " \
                               "FROM kr_stock_daily " \
                               "WHERE DATE ='{}' " \
                               "AND kr_stock_code='{}';".format(recently_date, code)
                    cursor.execute(data_sql)
                    data = cursor.fetchall()

        except Exception as e:
            print('->', e)

        finally:
            if connection:
                connection.close()
                # print(value)
        return data[0]

    def kr_detail_data(self, code):

        connection = None
        try:
            connection = pymysql.connect(host = 'localhost',
                                     user = 'root',
                                     password = '0000',
                                     db = 'web_db',
                                     port = 3306,
                                     charset = 'utf8',
                                     cursorclass = pymysql.cursors.DictCursor)
            if connection:
                # print('DB 오픈')

                with connection.cursor() as cursor:
                    # 최신 date 출력
                    date_sql = "select DATE " \
                          "FROM kr_stock_weekly " \
                          "group BY DATE " \
                          "order by date DESC " \
                          "LIMIT 1;"
                    cursor.execute(date_sql)
                    date_data = str(cursor.fetchall())
                    first_index = date_data.find('(')+1 # 형태가 이상해서 (,)위치 활용해 날짜 추출
                    second_index = date_data.find(')')
                    date_data = [i.strip() for i in date_data[first_index:second_index].split(',')]
                    if len(date_data[1]) == 1:
                        date_data[1] = '0'+ date_data[1]
                    if len(date_data[2]) == 1:
                        date_data[2] = '0'+ date_data[2]
                    recently_date = date_data[0]+'-'+date_data[1]+'-'+date_data[2]

                    data_sql = "SELECT * " \
                               "FROM kr_stock_weekly " \
                               "WHERE DATE ='{}' " \
                               "AND kr_stock_code='{}';".format(recently_date,code)
                    cursor.execute(data_sql)
                    data = cursor.fetchall()
        except Exception as e:
            print('->', e)

        finally:
            if connection:
                connection.close()
                # print(value)
        return data[0]

    def kr_financial_data(self, code):

        connection = None
        try:
            connection = pymysql.connect(host = 'localhost',
                                     user = 'root',
                                     password = '0000',
                                     db = 'web_db',
                                     port = 3306,
                                     charset = 'utf8',
                                     cursorclass = pymysql.cursors.DictCursor)
            if connection:
                # print('DB 오픈')

                with connection.cursor() as cursor:
                    # 최신 date 출력
                    sql_yearly = "SELECT * " \
                                 "FROM kr_stock_statements " \
                                 "WHERE DATE='2019.12' " \
                                 "AND kind='1'" \
                                 "AND kr_stock_code='{}';".format(code)
                    cursor.execute(sql_yearly)
                    data_yearly = cursor.fetchall()
                    data_yearly = list(data_yearly[0].values())

                    sql_quarter = "SELECT * " \
                                  "FROM kr_stock_statements " \
                                  "WHERE DATE='2020.03' " \
                                  "AND kind='2' " \
                                  "AND kr_stock_code={};".format(code)
                    cursor.execute(sql_quarter)
                    data_quarter = cursor.fetchall()
                    data_quarter = list(data_quarter[0].values())

                    final_data = data_yearly + data_quarter
        except Exception as e:
            print('->', e)

        finally:
            if connection:
                connection.close()
                # print(value)
        return final_data
