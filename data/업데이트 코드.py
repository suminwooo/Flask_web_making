from data.code_data.code_data_update_add import code_add_update
import pymysql
from data.main_data_daily_crolling import main_page_data_crolling
from data.daily_stock_forigner_data_colling import foreigner_instituion_crolling

def daily_update():

    print('코드 체크 및 데일리 업데이트 시작')
    code_add_update().code_list_update()
    print('완료')
    print('데일리 메인 데이터 업데이트 시작')
    main_page_data_crolling().input_main_page_data()
    print('완료')
    print('외국인 및 기관 데이터 업데이트 시작')
    foreigner_instituion_crolling().crolling_naver()
    print('완료;')

    return '업데이트 완료'



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