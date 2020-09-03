#API가 아닌 DB에서 바로 전송

import pymysql
import re
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


class main_page_information:

    def main_page_data(self):
        connection = None
        row = None
        try:
            connection = pymysql.connect(host = 'localhost',
                                     user = 'root',
                                     password = '0000',
                                     db = 'web_db',
                                     port = 3306,
                                     charset = 'utf8',
                                     cursorclass = pymysql.cursors.DictCursor)

            with connection.cursor() as cursor:
                sql = "SELECT * " \
                      "FROM main_page_data " \
                      "ORDER BY DATE DESC LIMIT 1;"
                cursor.execute(sql)
                row = cursor.fetchall()

        except Exception as e:
            print('->', e)

        finally:
            if connection:
                connection.close()
        return row[0]

    def main_page_calculate(self):

        kospi_sum = int(re.sub('[^0-9]', '', main_page_information().main_page_data()['kospi_individual'])) \
                    + int(re.sub('[^0-9]', '', main_page_information().main_page_data()['kospi_foreigner'])) \
                    + int(re.sub('[^0-9]', '', main_page_information().main_page_data()['kospi_Institutional']))
        kosdaq_sum = int(re.sub('[^0-9]', '', main_page_information().main_page_data()['kosdaq_individual'])) \
                     + int(re.sub('[^0-9]', '', main_page_information().main_page_data()['kosdaq_foreigner'])) \
                     + int(re.sub('[^0-9]', '', main_page_information().main_page_data()['kosdaq_Institutional']))
        kospi_kosdaq_sum = [kospi_sum, kosdaq_sum]

        return kospi_kosdaq_sum


class kr_stock_page_imformation:

    def kospi_rank(self):
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
                sql = "SELECT a.kr_stock_code, a.kr_stock_name, b.kr_stock_code, b.kr_stock_kospi_rank ,b.kr_stock_market_value " \
                      "FROM kr_stock_list AS a " \
                      "JOIN (SELECT * " \
                      "FROM kr_stock_weekly " \
                      "WHERE DATE IN (SELECT MAX(DATE)" \
                      " FROM kr_stock_weekly)) AS b " \
                      "ON a.kr_stock_code = b.kr_stock_code;"
                cursor.execute(sql)
                row = pd.DataFrame(cursor.fetchall())
                df = row[row.columns[1:]]
                edit_df = pd.DataFrame()
                for i in range(len(df)):
                    if len(df.loc[i]['kr_stock_kospi_rank']) < 5:
                        continue
                    else:
                        edit_df = pd.concat([edit_df,pd.DataFrame(list(df.loc[i]))], axis=1)
                edit_df = edit_df.T
                edit_df.columns = ['code', 'name', 'rank','value']
                edit_df['rank'] = [int(i[i.find(' ')+1:i.find('위')]) for i in list(edit_df['rank'])]
                edit_df = edit_df.sort_values(by='rank')
                edit_df = edit_df.reset_index()
                edit_df = edit_df[:10]
                edit_df = edit_df[['rank','code','name','value']]
                fianl_dic = {}
                for i in range(len(edit_df)):
                    fianl_dic[i] = list(edit_df.loc[i])
        except Exception as e:
            print('->', e)

        finally:
            if connection:
                connection.close()
        return fianl_dic



class detail_serach_page_imformation:

    def main_information(self, code):
        connection = None
        try:
            connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password='0000',
                                         db='web_db',
                                         port=3306,
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)

            with connection.cursor() as cursor:
                sql = "SELECT * " \
                      "FROM kr_stock_list " \
                      "WHERE kr_stock_code = {} " \
                      "OR kr_stock_name ={};".format(code, code)
                cursor.execute(sql)
                data = cursor.fetchall()
                data = data[0]
                if len(str(data['kr_stock_code'])) != 6:
                    data['kr_stock_code'] = str(data['kr_stock_code']).zfill(6)
        except Exception as e:
            print('->', e)

        finally:
            if connection:
                connection.close()
        return data
