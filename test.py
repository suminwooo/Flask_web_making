##################################################################
# 라이브러리
from flask import Flask, render_template, request # 플라스트 라이브러리
from flask_restful import Resource, Api
from flask import jsonify

from etc.date import date_method
from web_engine.web_engine import web_engine

from data.naver_news_crolling import naver_news
from data.stock_change_calculate import kr_page_data
from data.mysql_to_python_api import total_stock_list, korea_detail_information
from data.mysql_to_python_straight import main_page_information, detail_serach_page_imformation
from data.forigner_institution import foreinger_institurion
from data.low_value_stock_code import low_value_stock
##################################################################

app = Flask(__name__)
api = Api(app)
app.config['JSON_AS_ASCII'] = False

class api_data(Resource):

    def get(self):
        kospi_rank_data = kr_page_data().rank('kospi')
        kosdaq_rank_data = kr_page_data().rank('kosdaq')
        kospi_low_value_data = low_value_stock().final_data_to_df('kospi')[0]
        kosdaq_low_value_data = low_value_stock().final_data_to_df('kosdaq')[0]
        total_stock_price = total_stock_list().stock_information()

        message = {
            'total_price_data': total_stock_price,
            'kospi_rank_data' : kospi_rank_data,
            'kosdaq_rank_data' : kosdaq_rank_data,
            'kospi_low_value_data' : kospi_low_value_data,
            'kosdaq_low_value_data' : kosdaq_low_value_data
        }
        resp = jsonify(message)
        resp.status_code = 200
        return resp

api.add_resource(api_data, '/api_data')

###################################################################
# 검색 부분


@app.route('/search_detail', methods=['POST'])
def search_stock():
    # try:
    search = request.form['input']
    search_word = web_engine().search('{}'.format(search)) # 검색 엔진
    search_word_code = str(search_word[0]).zfill(6)
    institution_foriegner = foreinger_institurion().show_seach_page_foreigner_instition(
        search_word_code)
    news_data = naver_news().news_information(search_word_code)
    financial_data = korea_detail_information().kr_financial_data(search_word_code)
    main_page_value = main_page_information().main_page_data()
    stock_information = detail_serach_page_imformation().main_information(search_word_code)
    nonprice_data = korea_detail_information().kr_detail_data(search_word_code)
    price_data = korea_detail_information().kr_price_data(search_word_code)
    price_diff_data = kr_page_data().change_rate_calculate()[int(search_word_code)]

    return render_template('kr_search_detail.html',
                           search_word_code = search_word_code,
                           main_page_value = main_page_value,
                           news_data = news_data,
                           nonprice_data = nonprice_data,
                           price_data = price_data,
                           financial_data = financial_data,
                           institution_foriegner = institution_foriegner,
                           stock_information = stock_information,
                           price_diff = price_diff_data,
                           current_time = date_method())

    # except:
    #     return render_template('error_search_detail.html')
###################################################################
# 개별 페이지

@app.route('/')
def main_page():

    main_page_value = main_page_information().main_page_data()
    kospi_kosdaq_sum = main_page_information().main_page_calculate()

    kospi_change_data = kr_page_data().volatilty('kospi')
    kosdaq_change_data = kr_page_data().volatilty('kosdaq')

    kospi_low_value_data = low_value_stock().final_data_to_df('kospi')[1]
    kosdaq_low_value_data = low_value_stock().final_data_to_df('kosdaq')[1]

    return render_template('main_page.html',
                           main_page_value = main_page_value,
                           kospi_kosdaq_sum = kospi_kosdaq_sum,
                           kospi_change_data=kospi_change_data,
                           kosdaq_change_data = kosdaq_change_data,
                           current_time = date_method().time(),
                           kospi_low_value_data = kospi_low_value_data,
                           kosdaq_low_value_data = kosdaq_low_value_data
                           )


@app.route('/korea_stock')
def korea_stock():

    main_page_value = main_page_information().main_page_data()
    foreinger_institurion_data = foreinger_institurion().daily_data_db_to_python()
    kospi_change_data = kr_page_data().volatilty('kospi')
    kosdaq_change_data = kr_page_data().volatilty('kosdaq')
    kospi_volume_data = kr_page_data().volume('kospi')
    kosdaq_volume_data = kr_page_data().volume('kosdaq')
    return render_template('korea_stock.html',
                           main_page_value = main_page_value,
                           current_time = date_method(),
                           foreinger_institurion_data=foreinger_institurion_data,
                           kospi_change_data = kospi_change_data,
                           kosdaq_change_data = kosdaq_change_data,
                           kospi_volume_data = kospi_volume_data,
                           kosdaq_volume_data = kosdaq_volume_data
                           )


@app.route('/sales_log')
def sales_log():
    return render_template('sales_log.html')

@app.route('/twit') # 게시판 : 추후 타임라인처럼 해보기
def twit():
    return render_template('twit.html')

if __name__ == '__main__':
    app.run()