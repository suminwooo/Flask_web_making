# 네이버 재무제표 크롤링

from sqlalchemy import create_engine
import requests
from bs4 import BeautifulSoup
import pymysql

# 리스트 출력
connection = None
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='0000',
                             db='web_db',
                             port=3306,
                             charset='utf8')
with connection.cursor() as cursor:
    sql = "SELECT DISTINCT kr_stock_code FROM kr_stock_list;"
    cursor.execute(sql)
    kr_stock_list = cursor.fetchall()
kr_stock_list = [i[0] for i in kr_stock_list]


# DB열기

engine = create_engine("mysql+pymysql://root:"+"0000"+"@127.0.0.1/web_db?charset=utf8",
                        encoding='utf-8')
conn = engine.connect()

for code in kr_stock_list:
    code = str(code).zfill(6)
    print(code)
    URL = "https://finance.naver.com/item/main.nhn?code={}".format(code)

    samsung_electronic = requests.get(URL)
    html = samsung_electronic.text

    soup = BeautifulSoup(html, 'html.parser')

    finance_html = soup.select('div.section.cop_analysis div.sub_section')[0]

    th_data = [item.get_text().strip() for item in finance_html.select('thead th')]
    annual_date = th_data[3:7]
    quarter_date = th_data[7:13]

    finance_index = [item.get_text().strip() for item in finance_html.select('th.h_th2')][3:]

    finance_data = [item.get_text().strip() for item in finance_html.select('td')]

    import numpy as np

    finance_data = np.array(finance_data)
    finance_data.resize(len(finance_index), 10)

    finance_date = annual_date + quarter_date

    import pandas as pd

    finance = pd.DataFrame(data=finance_data[0:, 0:], index=finance_index, columns=finance_date)

    annual_finance = finance.iloc[:, :4]
    annual_finance = annual_finance.T
    annual_finance['kind'] = 1
    annual_finance['kr_stock_code'] = code
    annual_finance = annual_finance.reset_index()
    annual_finance = annual_finance[
        ['kr_stock_code', 'index', 'kind', '매출액', '영업이익', '당기순이익', '영업이익률', '순이익률', 'ROE(지배주주)', '부채비율',
         '당좌비율', '유보율', 'EPS(원)', 'PER(배)', 'BPS(원)', 'PBR(배)', '주당배당금(원)', '시가배당률(%)', '배당성향(%)']]
    annual_finance.columns = ['kr_stock_code', 'date', 'kind', 'sales', 'operating_profit', 'net_Income',
                              'operating_margin', 'net_margin',
                              'ROE', 'debt_ratio', 'quick_ratio', 'resesrvation_ratio', 'EPS', 'PER', 'BPS',
                              'PBR', 'dividend_per_share',
                              'market_div_ratio', 'payout_ratio']

    quarter_finance = finance.iloc[:, 4:]
    quarter_finance = quarter_finance.T
    quarter_finance['kind'] = 2
    quarter_finance['kr_stock_code'] = code
    quarter_finance = quarter_finance.reset_index()
    quarter_finance = quarter_finance[
        ['kr_stock_code', 'index', 'kind', '매출액', '영업이익', '당기순이익', '영업이익률', '순이익률', 'ROE(지배주주)', '부채비율',
         '당좌비율', '유보율', 'EPS(원)', 'PER(배)', 'BPS(원)', 'PBR(배)', '주당배당금(원)', '시가배당률(%)', '배당성향(%)']]
    quarter_finance.columns = ['kr_stock_code', 'date', 'kind', 'sales', 'operating_profit', 'net_Income',
                               'operating_margin', 'net_margin',
                               'ROE', 'debt_ratio', 'quick_ratio', 'resesrvation_ratio', 'EPS', 'PER', 'BPS',
                               'PBR', 'dividend_per_share',
                               'market_div_ratio', 'payout_ratio']

    annual_finance.to_sql(name='kr_stock_statements', con=engine, if_exists='append', index=False)
    quarter_finance.to_sql(name='kr_stock_statements', con=engine, if_exists='append', index=False)
