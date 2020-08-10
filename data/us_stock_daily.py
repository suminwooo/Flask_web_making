## 완료

from etc.date import date_num
import pandas as pd
import FinanceDataReader as fdr

data = pd.read_csv('C:/Users/wsm26/Desktop/Flask_web_making/data/raw_data/us_stock_list.csv')
# data는 절대 경로로 표시해줘야함
code_list = list(data['us_stock_code'])

class us_stock_daily:

    def daily_data(self):
        dataframe_test = pd.DataFrame()

        for code in code_list:
            df = fdr.DataReader(code, date_num())
            df = df.reset_index()
            df.columns = ['date', 'close', 'open', 'high', 'low', 'volume', 'close_diff']
            df['code'] = code
            df = df[['code', 'date', 'close', 'close_diff', 'open', 'high', 'low', 'volume']]
            dataframe_test = pd.concat([dataframe_test, df], axis=0)

        final_data = dataframe_test.dropna(axis=0).reset_index()[
            ['code', 'close', 'close_diff', 'open', 'high', 'low', 'volume']]
        final_data.columns = ['us_stock_code', 'us_stock_close', 'us_stock_close_diff', 'us_stock_open',
                              'us_stock_high', 'us_stock_low', 'us_stock_volume']

        final_data['date'] = date_num()
        final_data = final_data[
            ['us_stock_code', 'date', 'us_stock_close', 'us_stock_close_diff', 'us_stock_open', 'us_stock_high',
             'us_stock_low', 'us_stock_volume']]

        return final_data
