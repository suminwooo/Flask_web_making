#API가 아닌 DB에서 바로 전송

import pymysql

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
                      "ORDER BY DATE DESC LIMIT 1;;"
                cursor.execute(sql)
                row = cursor.fetchall()

        except Exception as e:
            print('->', e)

        finally:
            if connection:
                connection.close()
        return row[0]

