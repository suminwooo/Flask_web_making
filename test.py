from flask import Flask, render_template, request
from data.main_page_data import main_page_data
from etc.date import time
from data.db_test import main_page_data, korea_code_data
from flask_restful import Resource, Api

##################################################################

app = Flask(__name__)
api = Api(app)
app.config['JSON_AS_ASCII'] = False

##################################################################

# API 페이지
from db.data_api import stock_list_api
from flask import jsonify
from data.kr_seach_page import stock_all_info

class api_data(Resource):
    def get(self):
        test_data = stock_list_api().api()
        rank_data = kr_page_data().rank()
        low_value_data = low_value_stock().final_data_to_df()
        all_price_data = stock_all_info().price()

        message = {
            'kr_stock_list': test_data,
            'rank_data' : rank_data,
            'low_value_data' : low_value_data,
            'all_price_data' : all_price_data

        }
        resp = jsonify(message)
        resp.status_code = 200
        print(resp)
        return resp

api.add_resource(api_data, '/test')

###################################################################

date = '2020-08-28'

###################################################################

from web_engine.web_engine import web_engine
from data.naver_news import naver_news
from data.db_test import korea_detail_information
from data.kr_page_data import kr_page_data

@app.route('/search_detail', methods=['POST'])
def search_stock():
    search = request.form['input']
    # try:
    search_word = web_engine().search('{}'.format(search)) # 검색 엔진
    search_word_code = search_word[0] # db관리 개판으로 해서 숫자 길이 안맞음 아래는 0 채우면 됨
    STOCK = stock_list_api().api()[search_word_code] # 주식 이름, 코드 띄어줌
    # price_diff_info = kr_page_data().change_rate_calculate()[int(search_word_code)] # 가격차이
    search_word_code = search_word[0].zfill(6)
    news_data = naver_news().news_information(search_word_code)
    # nonprice_info = korea_detail_information().kr_detail_data(search_word_code)
    price_info = korea_detail_information().kr_price_data(search_word_code)
    financial_data = korea_detail_information().kr_financial_data(search_word_code)
    institution_foriegner = korea_detail_information().kr_institution_foriegner_data(search_word_code)
    return render_template('kr_search_detail.html',
                           main_page_value = main_page_data(date),
                           STOCK = STOCK,
                           # nonprice_data = nonprice_info,
                           price_data = price_info,
                           news_data = news_data,
                           # price_diff = price_diff_info,
                           financial_data = financial_data,
                           institution_foriegner = institution_foriegner,
                           current_time = time())
    # except:
    #     return render_template('error_search_detail.html')

###################################################################
import re

@app.route('/')
def main_page():

    kospi_sum = int(re.sub('[^0-9]', '',main_page_data(date)['kospi_individual']))\
                +int(re.sub('[^0-9]', '',main_page_data(date)['kospi_foreigner']))\
                +int(re.sub('[^0-9]', '',main_page_data(date)['kospi_Institutional']))
    kosdaq_sum = int(re.sub('[^0-9]', '',main_page_data(date)['kosdaq_individual']))\
                 +int(re.sub('[^0-9]', '',main_page_data(date)['kosdaq_foreigner']))\
                 +int(re.sub('[^0-9]', '',main_page_data(date)['kosdaq_Institutional']))
    kospi_kosdaq_sum = [kospi_sum,kosdaq_sum]

    change_data = kr_page_data().volatilty()
    low_value_data_sample = low_value_stock().final_data_to_df_sample()

    return render_template('main_page.html',
                           main_page_value = main_page_data(date),
                           kospi_kosdaq_sum = kospi_kosdaq_sum,
                           change_data=change_data,
                           low_value_data = low_value_data_sample,
                           current_time = time())

from data.kr_page_data2 import low_value_stock,foreigener_institution_info

@app.route('/korea_stock')
def korea_stock():
    foreigener_institution_data = foreigener_institution_info().foreigener_institution_data()
    change_data = kr_page_data().volatilty()
    volume_data = kr_page_data().volume()
    return render_template('korea_stock.html',
                           main_page_value = main_page_data(date),
                           current_time = time(),
                           change_data = change_data,
                           volume_data = volume_data,
                           foreigener_institution_data = foreigener_institution_data,
                           korea_code_list = korea_code_data())


@app.route('/sales_log')
def sales_log():
    return render_template('sales_log.html')

@app.route('/add_check')
def add_check():
    return render_template('add_check.html')

@app.route('/twit') # 게시판 : 추후 타임라인처럼 해보기
def twit():
    rank_data = kr_page_data().rank()

    return render_template('twit.html',rank_data=rank_data)

@app.route('/etc')
def etc():
    return render_template('etc.html')

if __name__ == '__main__':
    app.run()