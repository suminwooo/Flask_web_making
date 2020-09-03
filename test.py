##################################################################
# 라이브러리

from flask import Flask, render_template, request # 플라스트 라이브러리
from flask_restful import Resource, Api
from flask import jsonify

from etc.date import date_method
from web_engine.web_engine import web_engine

from data.naver_news_crolling import naver_news
from data.stock_change_calculate import kr_page_data
from data.mysql_to_python_api import total_stock_list, stock_all_info, korea_detail_information
from data.mysql_to_python_straight import main_page_information, kr_stock_page_imformation, detail_serach_page_imformation
from data.forigner_institution import foreinger_institurion
from data.low_value_stock_code import low_value_stock
##################################################################


app = Flask(__name__)
api = Api(app)
app.config['JSON_AS_ASCII'] = False

class api_data(Resource):

    def get(self):

        test_data = total_stock_list().stock_information()
        rank_data = kr_page_data().rank()
        all_price_data = stock_all_info().price()
        low_value_data = low_value_stock().final_data_to_df()[0]
        message = {
            'kr_stock_list': test_data,
            'rank_data' : rank_data,
            'all_price_data' : all_price_data,
            'low_value_data' : low_value_data
        }

        resp = jsonify(message)
        resp.status_code = 200
        return resp

api.add_resource(api_data, '/api_data')

###################################################################
# 검색 부분


@app.route('/search_detail', methods=['POST'])
def search_stock():
    try:
        search = request.form['input']
        search_word = web_engine().search('{}'.format(search)) # 검색 엔진
        search_word_code = str(search_word[0]).zfill(6)
        institution_foriegner = foreinger_institurion().show_seach_page_foreigner_instition(
            search_word_code)
        news_data = naver_news().news_information(search_word_code)
        financial_data = korea_detail_information().kr_financial_data(search_word_code)
        main_page_value = main_page_information().main_page_data()
        stock_information = detail_serach_page_imformation().main_information(search_word_code)

        return render_template('kr_search_detail.html',
                               main_page_value = main_page_value,
                               news_data = news_data,
                               financial_data = financial_data,
                               institution_foriegner = institution_foriegner,
                               stock_information = stock_information,
                               current_time = date_method())

    except:

        return render_template('error_search_detail.html')
###################################################################
# 개별 페이지

@app.route('/')
def main_page():

    main_page_value = main_page_information().main_page_data()
    kospi_kosdaq_sum = main_page_information().main_page_calculate()
    change_data = kr_page_data().volatilty()
    low_value_data = low_value_stock().final_data_to_df_sample()

    return render_template('main_page.html',
                           main_page_value = main_page_value,
                           kospi_kosdaq_sum = kospi_kosdaq_sum,
                           change_data=change_data,
                           current_time = date_method().time(),
                           low_value_data = low_value_data
                           )


@app.route('/korea_stock')
def korea_stock():

    main_page_value = main_page_information().main_page_data()
    foreinger_institurion_data = foreinger_institurion().daily_data_db_to_python()
    change_data = kr_page_data().volatilty()
    volume_data = kr_page_data().volume()
    kospi_value_rank = kr_stock_page_imformation().kospi_rank()
    return render_template('korea_stock.html',
                           main_page_value = main_page_value,
                           current_time = date_method(),
                           foreinger_institurion_data=foreinger_institurion_data,
                           change_data = change_data,
                           kospi_value_rank=kospi_value_rank,
                           volume_data = volume_data
                           )


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