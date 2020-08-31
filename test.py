##################################################################
# 라이브러리

from flask import Flask, render_template, request # 플라스트 라이브러리
from flask_restful import Resource, Api
from flask import jsonify

from etc.date import date_method
from web_engine.web_engine import web_engine

import re

from data.naver_news_crolling import naver_news
from data.stock_change_calculate import kr_page_data
from data.mysql_to_python_api import total_stock_list, stock_all_info, korea_detail_information
from data.mysql_to_python_straight import main_page_information
from data.forigner_institution import foreinger_institurion
##################################################################


app = Flask(__name__)
api = Api(app)
app.config['JSON_AS_ASCII'] = False

class api_data(Resource):
    def get(self):
        test_data = total_stock_list().stock_information()
        rank_data = kr_page_data().rank()
        all_price_data = stock_all_info().price()

        message = {
            'kr_stock_list': test_data,
            'rank_data' : rank_data,
            'all_price_data' : all_price_data

        }
        resp = jsonify(message)
        resp.status_code = 200
        return resp

api.add_resource(api_data, '/api_data')

###################################################################
# 검색 부분


@app.route('/search_detail', methods=['POST'])
def search_stock():
    search = request.form['input']
    search_word = web_engine().search('{}'.format(search)) # 검색 엔진
    search_word_code = search_word[0] # db관리 개판으로 해서 숫자 길이 안맞음 아래는 0 채우면 됨
    # STOCK = stock_list_api().api()[search_word_code] # 주식 이름, 코드 띄어줌
    price_diff_info = kr_page_data().change_rate_calculate()[int(search_word_code)] # 가격차이
    search_word_code = str(search_word[0]).zfill(6)
    news_data = naver_news().news_information(search_word_code)
    nonprice_info = korea_detail_information().kr_detail_data(search_word_code)
    price_info = korea_detail_information().kr_price_data(search_word_code)
    financial_data = korea_detail_information().kr_financial_data(search_word_code)
    institution_foriegner = korea_detail_information().kr_institution_foriegner_data(search_word_code)

    return render_template('kr_search_detail.html',
                           main_page_value = main_page_information(),
                           # STOCK = STOCK,
                           nonprice_data = nonprice_info,
                           price_data = price_info,
                           news_data = news_data,
                           price_diff = price_diff_info,
                           financial_data = financial_data,
                           institution_foriegner = institution_foriegner,
                           current_time = date_method())

###################################################################
# 개별 페이지

@app.route('/')
def main_page():
    main_page_value = main_page_information().main_page_data()
    kospi_kosdaq_sum = main_page_information().main_page_calculate()
    change_data = kr_page_data().volatilty()

    return render_template('main_page.html',
                           main_page_value = main_page_value,
                           kospi_kosdaq_sum = kospi_kosdaq_sum,
                           change_data=change_data,
                           current_time = date_method().time())


@app.route('/korea_stock')
def korea_stock():
    main_page_value = main_page_information().main_page_data()
    foreinger_institurion_data = foreinger_institurion().show_seach_page_foreigner_instition()
    change_data = kr_page_data().volatilty()
    volume_data = kr_page_data().volume()

    return render_template('korea_stock.html',
                           main_page_value = main_page_value,
                           current_time = date_method(),
                           foreinger_institurion_data=foreinger_institurion_data,
                           change_data = change_data,
                           volume_data = volume_data,
                           korea_code_list = total_stock_list())


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