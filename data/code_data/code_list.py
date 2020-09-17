# 현재 상장되어있는 코스피, 코스닥 목록 출력
# code_data_update_add 와 연결

import FinanceDataReader as fdr
import pymysql
import pandas as pd

class code_information():

    def code_data(self):

        df_krx = fdr.StockListing('KRX')
        kospi_kosdaq = df_krx[(df_krx['Market'] == 'KOSDAQ') | (df_krx['Market'] == 'KOSPI')].dropna()
        kospi_kosdaq = kospi_kosdaq[
            ['Symbol', 'Market', 'Name', 'Sector', 'Industry', 'ListingDate', 'SettleMonth', 'HomePage', 'Region']]
        kospi_kosdaq.columns = ['kr_stock_code', 'market', 'kr_stock_name', 'sector', 'industry', 'listingdate',
                                'settledate', 'homepage', 'region']

        return kospi_kosdaq

    def code_total_list(self):
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
                sql = "select *" \
                      "from kr_stock_list;"
                cursor.execute(sql)
                row = pd.DataFrame(cursor.fetchall())
                row = row.set_index('kr_stock_code')[['kr_stock_name', 'market']]
        except Exception as e:
            print('->', e)

        finally:
            if connection:
                connection.close()
        return row
