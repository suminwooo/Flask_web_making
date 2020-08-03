import pandas as pd
import pymysql

data = pd.read_csv('crolling_n_data/raw_data/kr_stock_price_total.csv')
connection = pymysql.connect(host='localhost', user='root', password='0000', charset='utf8', db='web_db')
cur = connection.cursor()
for i in range(len(data)):
    each_data = data.loc[i].fillna('NO_DATA')
    value = '('+str(list(each_data))[1:-1]+')'
    # print(value)
    sql = "INSERT INTO kr_stock_price_daily (kr_stock_code,date,kr_stock_close,kr_stock_close_diff, kr_stock_open, kr_stock_high, kr_stock_low, kr_stock_volume) VALUES {};".format(value)
    cur.execute(sql)
    connection.commit()
connection.close()

