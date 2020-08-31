#API가 아닌 DB에서 바로 전송

import pymysql
import re
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


class foreinger_institution_data:

    def foreinger_institution(self):
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