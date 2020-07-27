import pymysql
from crolling_n_data.main_page_data import main_page_data

# connection = pymysql.connect(host='localhost', user='root', password='0000', charset='utf8', db='web_db')
# cur = connection.cursor()
# sql = "INSERT INTO main_page_data (date_time,kospi_close,kospi_close_diff,kospi_close_rate,kosdaq_close,kosdaq_close_diff,kosdaq_close_rate,nasdaq_close,nasdaq_close_diff,nasdaq_close_rate,nasdaq100_close,nasdaq100_close_diff,nasdaq100_close_rate,dow_close,dow_close_diff,dow_close_rate,snp500_close,snp500_close_diff,snp500_close_rate,usd_close,usd_close_diff,usd_close_rate,eur_close,eur_close_diff,eur_close_rate,jpy_close,jpy_close_diff,jpy_close_rate,dollorindex_close,dollorindex_close_diff,dollorindex_close_rate,gold_close,gold_close_diff,gold_close_rate,wti_close,wti_close_diff,wti_close_rate,kospi_individual,kospi_foreigner,kospi_Institutional,kosdaq_individual,kosdaq_foreigner,kosdaq_Institutional) VALUES {};".format("("+str(main_page_data().final_value())[1:-1]+")")
# print(sql)
# cur.execute(sql)
# connection.commit()
# connection.close()



connection = pymysql.connect(host='localhost', user='root', password='0000', charset='utf8', db='web_db')
cur = connection.cursor()
sql = "INSERT INTO us_stock_list (us_stock_code,us_stock_name,us_stock_kind VALUES {};".format()
print(sql)
cur.execute(sql)
connection.commit()
connection.close()