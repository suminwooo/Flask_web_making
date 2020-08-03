import pymysql
from crolling_n_data.main_page_data import main_page_data
from crolling_n_data.us_stock_daily import us_stock_daily
from crolling_n_data.kr_stock_weekly import kr_stock_weekly
# from crolling_n_data.kr_stock_daily import kr_stock_daily
from crolling_n_data.us_stock_weekly import us_stock_weekly

# # 메인 페이지 DB 보내기
# connection = pymysql.connect(host='localhost', user='root', password='0000', charset='utf8', db='web_db')
# cur = connection.cursor()
# sql = "INSERT INTO main_page_data (date,kospi_close,kospi_close_diff,kospi_close_rate,kosdaq_close,kosdaq_close_diff,kosdaq_close_rate,nasdaq_close,nasdaq_close_diff,nasdaq_close_rate,nasdaq100_close,nasdaq100_close_diff,nasdaq100_close_rate,dow_close,dow_close_diff,dow_close_rate,snp500_close,snp500_close_diff,snp500_close_rate,usd_close,usd_close_diff,usd_close_rate,eur_close,eur_close_diff,eur_close_rate,jpy_close,jpy_close_diff,jpy_close_rate,dollorindex_close,dollorindex_close_diff,dollorindex_close_rate,gold_close,gold_close_diff,gold_close_rate,wti_close,wti_close_diff,wti_close_rate,kospi_individual,kospi_foreigner,kospi_Institutional,kosdaq_individual,kosdaq_foreigner,kosdaq_Institutional) VALUES {};".format("("+str(main_page_data().final_value())[1:-1]+")")
# print(sql)
# cur.execute(sql)
# connection.commit()
# connection.close()


# # 한국 주식 업데이트 코드 (하루 짜리)
# connection = pymysql.connect(host='localhost', user='root', password='0000', charset='utf8', db='web_db')
# cur = connection.cursor()
# for i in range(len(kr_stock_daily().daily_data())):
#     value = '(' + str(list(kr_stock_daily().daily_data().loc[i]))[1:-1] + ')'
#     sql = "INSERT INTO kr_stock_daily (kr_stock_code,date,kr_stock_close, kr_stock_close_diff, kr_stock_open, kr_stock_high, kr_stock_low, kr_stock_volume) VALUES {};".format(value)
#     cur.execute(sql)
#     connection.commit()
# connection.close()


# # 미국 주식 업데이트 코드 (하루 짜리)
# connection = pymysql.connect(host='localhost', user='root', password='0000', charset='utf8', db='web_db')
# cur = connection.cursor()
# for i in range(len(us_stock_daily().daily_data())):
#     value = '(' + str(list(us_stock_daily().daily_data().loc[i]))[1:-1] + ')'
#     sql = "INSERT INTO us_stock_daily (us_stock_code,date,us_stock_close, us_stock_close_diff, us_stock_open, us_stock_high, us_stock_low, us_stock_volume) VALUES {};".format(value)
#     cur.execute(sql)
#     connection.commit()
# connection.close()

############### 체크해보기
# # 미국 주식 업데이트 코드 (1주일 짜리)
# connection = pymysql.connect(host='localhost', user='root', password='0000', charset='utf8', db='web_db')
# cur = connection.cursor()
# for i in range(len(us_stock_weekly().weekly_data())):
#     value = '(' + str(list(us_stock_weekly().weekly_data().loc[i]))[1:-1] + ')'
#     print(value)
#     sql = "INSERT INTO us_stock_weekly (us_stock_code, date, us_stock_regularMarketOpen, us_stock_twoHundredDayAverage , us_stock_payoutRatio , us_stock_regularMarketDayHigh , us_stock_averageDailyVolume10Day , us_stock_totalAssets , us_stock_regularMarketPreviousClose , us_stock_trailingAnnualDividendRate , us_stock_averageVolume10days , us_stock_dividendRate , us_stock_exDividendDate , us_stock_beta , us_stock_regularMarketDayLow , us_stock_regularMarketVolume , us_stock_averageVolume , us_stock_fiftyTwoWeekHigh , us_stock_fiveYearAvgDividendYield , us_stock_fiftyTwoWeekLow , us_stock_bid , us_stock_dividendYield , us_stock_lastDividendValue , us_stock_enterpriseValue , us_stock_threeYearAverageReturn , us_stock_fiveYearAverageReturn , us_stock_regularMarketPrice ) VALUES {};".format(value)
#     cur.execute(sql)
#     connection.commit()
# connection.close()


# # 한국 주식 업데이트 코드 (1주일 짜리)
# connection = pymysql.connect(host='localhost', user='root', password='0000', charset='utf8', db='web_db')
# cur = connection.cursor()
# for i in range(len(kr_stock_weekly().weekly_data())):
#     value = '('+str(list(kr_stock_weekly().weekly_data().loc[i]))[1:-1]+')'
#     sql = "INSERT INTO kr_stock_weekly (kr_stock_code,date,kr_stock_close,kr_stock_close_diff,kr_stock_close_percent,kr_stock_open,kr_stock_high,kr_stock_low,kr_stock_vol,kr_stock_market_value,kr_stock_kospi_rank,kr_stock_comment,kr_stock_goal_price,kr_stock_high_52week,kr_stock_low_52week,kr_stock_PER,kr_stock_EPS,kr_stock_est_PER,kr_stock_est_EPS,kr_stock_PBR,kr_stock_BPS,kr_stock_DIV,kr_stock_same_ind_per,kr_stock_same_ind_per_percentage) VALUES {};".format(value)
#     cur.execute(sql)
#     connection.commit()
# connection.close()