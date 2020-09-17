import pymysql
import FinanceDataReader as fdr
from data.code_data.code_list import code_information
from etc.date import date_method
from sqlalchemy import create_engine
import pandas_datareader as wb
import datetime

class code_add_update():

    def code_list(self):  # 현재 DB에 저장되어 있는 전체 코드 리스트 출력

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

        return self.kr_stock_list

    def code_list_update(self): # DB에서 실제 정보가 있는 데이터가 없을때 새롭게 DB에 추가해주기

        code_list = self.code_list()
        total_code_list = code_information().code_data()['kr_stock_code']
        non_list_code = list(set([int(i) for i in total_code_list]) - set(code_list))

        # DB 엔진
        engine = create_engine("mysql+pymysql://root:" + "0000" + "@127.0.0.1/web_db?charset=utf8",
                               encoding='utf-8')
        conn = engine.connect()

        if len(non_list_code) != 0:

            # 우선 없는 데이터 추가
            df_krx = fdr.StockListing('KRX')
            kospi_kosdaq = df_krx[(df_krx['Market'] == 'KOSDAQ') | (df_krx['Market'] == 'KOSPI')].dropna()
            kospi_kosdaq = kospi_kosdaq[
                ['Symbol', 'Market', 'Name', 'Sector', 'Industry', 'ListingDate', 'SettleMonth', 'HomePage', 'Region']]
            kospi_kosdaq.columns = ['kr_stock_code', 'market', 'kr_stock_name', 'sector', 'industry', 'listingdate',
                                    'settledate', 'homepage', 'region']
            kospi_kosdaq['kr_stock_code'] = [int(i) for i in kospi_kosdaq['kr_stock_code']]
            kospi_kosdaq = kospi_kosdaq.set_index('kr_stock_code')
            add_df = kospi_kosdaq.loc[non_list_code]
            add_df = add_df.reset_index()
            add_df.columns = ['kr_stock_code', 'market', 'kr_stock_name', 'sector', 'industry', 'listingdate',
                                    'settledate', 'homepage', 'region']

            # DB kr_stock_list 추가
            add_df.to_sql(name='kr_stock_list', con=engine, if_exists='append', index=False)
            # DB kr_stock_daily 추가
            for i in non_list_code:
                code = str(i).zfill(6)
                df = fdr.DataReader(code, date_method().date_num())
                df = df.reset_index()
                df['code'] = code
                df.columns = ['date','kr_stock_open','kr_stock_high','kr_stock_low','kr_stock_close',
                              'kr_stock_volume','kr_stock_close_diff','kr_stock_code']
                df = df[['kr_stock_code','date','kr_stock_open','kr_stock_close_diff','kr_stock_high','kr_stock_low',
                         'kr_stock_close','kr_stock_volume']]

                df.to_sql(name='kr_stock_daily', con=engine, if_exists='append', index=False)

            # 존재하는 데이터 업데이트
            for i in code_list:
                code = str(i).zfill(6)
                df = fdr.DataReader(code, '2020-09-14')
                df = df.reset_index()
                df['code'] = code
                df.columns = ['date', 'kr_stock_open', 'kr_stock_high', 'kr_stock_low', 'kr_stock_close',
                              'kr_stock_volume', 'kr_stock_close_diff', 'kr_stock_code']

                df = df[
                    ['kr_stock_code', 'date', 'kr_stock_open', 'kr_stock_close_diff', 'kr_stock_high', 'kr_stock_low',
                     'kr_stock_close', 'kr_stock_volume']]

                df.to_sql(name='kr_stock_daily', con=engine, if_exists='append', index=False)
            conn.close()

        else:
            #차이가 없을 경우 존재하는 데이터만 업데이트

            for i in code_list:
                code = str(i).zfill(6)
                df = fdr.DataReader(code, date_method().date_num())
                df = df.reset_index()
                df['code'] = code
                df.columns = ['date', 'kr_stock_open', 'kr_stock_high', 'kr_stock_low', 'kr_stock_close',
                              'kr_stock_volume', 'kr_stock_close_diff', 'kr_stock_code']

                df = df[
                    ['kr_stock_code', 'date', 'kr_stock_open', 'kr_stock_close_diff', 'kr_stock_high', 'kr_stock_low',
                     'kr_stock_close', 'kr_stock_volume']]

                df.to_sql(name='kr_stock_daily', con=engine, if_exists='append', index=False)

            conn.close()

class kospi_update:
    def daily_kospi_data_update(self):
        engine = create_engine("mysql+pymysql://root:" + "0000" + "@127.0.0.1/web_db?charset=utf8",
                               encoding='utf-8')
        conn = engine.connect()
        today_data = wb.DataReader("^KS11","yahoo",datetime.date.today())
        today_data.columns = ['high','low','open','close','volume','adj_close']
        today_data['type'] = 'kospi'
        today_data['date'] = date_method().date_num()
        today_data.to_sql(name='kr_index_data_daily', con=engine, if_exists='append', index=False)
        conn.close()
