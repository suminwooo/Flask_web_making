import pymysql
import pandas as pd
import numpy as np
import re
import warnings
warnings.filterwarnings('ignore')

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
                    data_dic = data.to_dict('index')

        except Exception as e:
            print('->', e)

        finally:
            if connection:
                connection.close()
                # print(value)

        return data_dic

print(stock_all_info().price())