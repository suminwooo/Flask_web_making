import pymysql
from data.main_page_data import main_page_data
from data.kr_stock_weekly import kr_stock_weekly
from data.kr_stock_daily import kr_stock_daily
from sqlalchemy import create_engine

# 메인 페이지 DB 보내기
connection = pymysql   .connect(host='localhost', user='root', password='0000', charset='utf8', db='web_db')
cur = connection.cursor()
sql = "INSERT INTO main_page_data (date,kospi_close,kospi_close_diff,kospi_close_rate,kosdaq_close,kosdaq_close_diff,kosdaq_close_rate,nasdaq_close,nasdaq_close_diff,nasdaq_close_rate,nasdaq100_close,nasdaq100_close_diff,nasdaq100_close_rate,dow_close,dow_close_diff,dow_close_rate,snp500_close,snp500_close_diff,snp500_close_rate,usd_close,usd_close_diff,usd_close_rate,eur_close,eur_close_diff,eur_close_rate,jpy_close,jpy_close_diff,jpy_close_rate,dollorindex_close,dollorindex_close_diff,dollorindex_close_rate,gold_close,gold_close_diff,gold_close_rate,wti_close,wti_close_diff,wti_close_rate,kospi_individual,kospi_foreigner,kospi_Institutional,kosdaq_individual,kosdaq_foreigner,kosdaq_Institutional) VALUES {};".format("("+str(main_page_data().final_value())[1:-1]+")")
cur.execute(sql)
connection.commit()
connection.close()

# 한국 주식 업데이트 코드 (하루 짜리)
connection = pymysql.connect(host='localhost', user='root', password='0000', charset='utf8', db='web_db')
cur = connection.cursor()
kr_daily_data = kr_stock_daily().daily_data()
for i in range(len(kr_daily_data)):
    value = '(' + str(list(kr_daily_data.loc[i]))[1:-1] + ')'
    sql = "INSERT INTO kr_stock_daily (kr_stock_code,date,kr_stock_open, kr_stock_close_diff, kr_stock_high, kr_stock_low, kr_stock_close, kr_stock_volume) VALUES {};".format(value)
    cur.execute(sql)
    connection.commit()
connection.close()
print('완료')

# 외국인 기관 +++
data = kr_stock_daily().daily_data2()
engine = create_engine("mysql+pymysql://root:"+"0000"+"@127.0.0.1/web_db?charset=utf8",
                        encoding='utf-8')
conn = engine.connect()
data.to_sql(name='kr_stock_invest_value', con=engine, if_exists='append', index=False)
conn.close()

# 한국 주식 업데이트 코드 (1주일 짜리)
connection = pymysql.connect(host='localhost', user='root', password='0000', charset='utf8', db='web_db')
cur = connection.cursor()
kr_weekly_data = kr_stock_weekly().weekly_data()
print(kr_weekly_data)
for i in range(len(kr_weekly_data)):
    print(i)
    value = '('+str(list(kr_weekly_data.loc[i]))[1:-1]+')'
    sql = "INSERT INTO kr_stock_weekly (kr_stock_code,date,kr_stock_close,kr_stock_close_diff,kr_stock_close_percent,kr_stock_open,kr_stock_high,kr_stock_low,kr_stock_vol,kr_stock_market_value,kr_stock_kospi_rank,kr_stock_comment,kr_stock_goal_price,kr_stock_high_52week,kr_stock_low_52week,kr_stock_PER,kr_stock_EPS,kr_stock_est_PER,kr_stock_est_EPS,kr_stock_PBR,kr_stock_BPS,kr_stock_DIV,kr_stock_same_ind_per,kr_stock_same_ind_per_percentage) VALUES {};".format(value)
    cur.execute(sql)
    connection.commit()
connection.close()


