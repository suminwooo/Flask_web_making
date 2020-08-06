from flask import Flask, render_template, request
from crolling_n_data.main_page_data import main_page_data
from etc.date import time,date_num
from DB.db_test import main_page_data, korea_code_data
from flask_restful import Resource, Api
import requests

##################################################################

app = Flask(__name__)
api = Api(app)
app.config['JSON_AS_ASCII'] = False

##################################################################

# API 페이지
from data_api import test
from flask import jsonify

class api_data(Resource):
    def get(self):
        test_data = test().test()
        message = {
            'kr_stock_list': test_data
        }
        resp = jsonify(message)
        resp.status_code = 200
        print(resp)
        return resp

api.add_resource(api_data, '/test')
date = date_num()

###################################################################

from web_engine.web_engine import web_engine
from crolling_n_data.naver_news import naver_news


@app.route('/search_detail',methods=['POST'])
def search_stock():
    search_word = request.form['input']
    data = web_engine().search('{}'.format(search_word))
    news_data = naver_news().news_information('005930')
    return render_template('search_detail.html',
                           main_page_value = main_page_data(date),
                           main_data = data,
                           news_data = news_data)


###################################################################


@app.route('/')
def main_page():
    return render_template('main_page.html', main_page_value = main_page_data(date),
                           current_time = time())

@app.route('/korea_stock')
def korea_stock():
    return render_template('korea_stock.html', main_page_value = main_page_data(date),
                           current_time = time(), korea_code_list = korea_code_data())



@app.route('/us_stock')
def us_stock():
    return render_template('us_stock.html',current_time = time(),
                           main_page_value = main_page_data(date))



@app.route('/coin')
def coin():
    return render_template('coin.html')

@app.route('/coin/<coin_name>')
def get_coin(coin_name):
    return 'profile : ' + coin_name

@app.route('/sales_log')
def sales_log():
    return render_template('sales_log.html')

@app.route('/add_check')
def add_check():
    return render_template('add_check.html')

@app.route('/twit') # 게시판 : 추후 타임라인처럼 해보기
def twit():
    return render_template('twit.html')

@app.route('/etc')
def etc():
    return render_template('etc.html')

if __name__ == '__main__':
    app.run()