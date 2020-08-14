from etc.date import date_num
import pandas as pd
import FinanceDataReader as fdr

data = pd.read_csv('C:/Users/wsm26/Desktop/Flask_web_making/data/raw_data/kospi_code.csv')

code_list = []
for i in data['code']:
    code = str(i)
    if len(code) == 2:
        code = '0000' + code
        code_list.append(code)
    elif len(code) == 3:
        code = '000' + code
        code_list.append(code)
    elif len(code) == 4:
        code = '00' + code
        code_list.append(code)
    elif len(code) == 5:
        code = '0' + code
        code_list.append(code)
    else:
        code_list.append(code)

class kr_stock_daily:

    def daily_data(self):
        dataframe_test = pd.DataFrame()

        for code in code_list:
            df = fdr.DataReader(code, date_num())
            df = df.reset_index()
            df.columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'close_diff']
            df['code'] = code
            df = df[['code', 'date', 'close', 'close_diff', 'open', 'high', 'low', 'volume']]
            dataframe_test = pd.concat([dataframe_test, df], axis=0)

        final_data = dataframe_test.dropna(axis=0).reset_index()[
            ['code', 'close', 'close_diff', 'open', 'high', 'low', 'volume']]
        final_data.columns = ['kr_stock_code', 'kr_stock_close', 'kr_stock_close_diff', 'kr_stock_open',
                              'kr_stock_high', 'kr_stock_low', 'kr_stock_volume']

        final_data['date'] = date_num()
        final_data = final_data[['kr_stock_code', 'date', 'kr_stock_open', 'kr_stock_close_diff','kr_stock_high', 'kr_stock_low', 'kr_stock_close',
             'kr_stock_volume']]

        return final_data
