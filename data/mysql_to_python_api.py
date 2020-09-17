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
                sql = " ;"
                cursor.execute(sql)
                row = cursor.fetchall()

        except Exception as e:
            print('->', e)

        finally:
            if connection:
                connection.close()
        return row

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
                               "AND kr_stock_code='{}'" \
                               "limit 1;".format(recently_date, code) # 추후 수정
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

import time
# 인덱스 추출
class index_detail_information:

    def kr_price_data(self):
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
                    date_sql = "select date,high,low,open,close,volume " \
                               "FROM kr_index_data_daily; "
                    cursor.execute(date_sql)
                    data = cursor.fetchall()
                    for i in data:
                        i['date'] = int(time.mktime(i['date'].timetuple()))
        except Exception as e:
            print('->', e)

        finally:
            if connection:
                connection.close()
                # print(value)
        return data

class total_stock_price_information:

    def kr_price_1000d_data(self): # 추후 code 추가
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
                    date_sql = "SELECT date,kr_stock_open,kr_stock_high," \
                               "kr_stock_low,kr_stock_close,kr_stock_volume " \
                               "FROM kr_stock_daily " \
                               "where kr_stock_code = 5930 " \
                               "order by date DESC;".format(5930)
                    cursor.execute(date_sql)
                    data = cursor.fetchall()
                    for i in data:
                        i['kr_stock_open'] = float(i['kr_stock_open'])
                        i['kr_stock_high'] = float(i['kr_stock_high'])
                        i['kr_stock_low'] = float(i['kr_stock_low'])
                        i['kr_stock_close'] = float(i['kr_stock_close'])
                        i['kr_stock_volume'] = float(i['kr_stock_volume'])
                        i['date1'] = int(time.mktime(i['date'].timetuple()))
                        i['date'] = i['date'].isoformat()
                    # print(data)
        except Exception as e:
            print('->', e)

        finally:
            if connection:
                connection.close()
                # print(value)
        return data

print(total_stock_price_information().kr_price_1000d_data())