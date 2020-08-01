from flask import Flask, render_template, request
from crolling_n_data.main_page_data import main_page_data
from etc.date import time
from DB.db_test import main_page_data, korea_code_data
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def main_page():
    return render_template('main_page.html', main_page_value = main_page_data('2020-07-27'),
                           current_time = time())

@app.route('/korea_stock')
def korea_stock():
    return render_template('korea_stock.html', main_page_value = main_page_data('2020-07-27'),
                           current_time = time(), korea_code_list = korea_code_data())

@app.route('/search_detail',methods=['POST'])
def search_stock():
    value = request.form['input']
    msg = '{}'.format(value)
    return render_template('search_detail.html', seaching_value = msg,
                           main_page_value = main_page_data('2020-07-27'))


@app.route('/us_stock')
def us_stock():
    return render_template('us_stock.html',current_time = time(),
                           main_page_value = main_page_data('2020-07-27'))


###################################################################

# API 페이지
from data_api import test
from flask import jsonify

class RegisterUser(Resource):
    def get(self):
        test_data = test().test()
        message = {
            'status': 200,
            'message': 'OK',
            'scores': test_data
        }
        resp = jsonify(message)
        resp.status_code = 200
        print(resp)
        return resp

api.add_resource(RegisterUser, '/test')

###################################################################
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