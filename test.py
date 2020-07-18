from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('main_page.html')

# @app.route('/korea_stock')
# def korea_stock():
#     return '국내주식 만드는 곳'
#
# @app.route('/korea_stock/<kr_stock>')
# def get_kr_stock(kr_stock):
#     return 'profile : ' + kr_stock
#
# @app.route('/us_stock')
# def us_stock():
#     return '해외주식 만드는 곳'
#
# @app.route('/us_stock/<us_stock>')
# def get_us_stock(us_stock):
#     return 'profile : ' + us_stock
#
# @app.route('/coin')
# def coin():
#     return '코인 만드는 곳'
#
# @app.route('/coin/<coin_name>')
# def get_coin(coin_name):
#     return 'profile : ' + coin_name
#
# @app.route('/daily')
# def daily():
#     return '매매일지'
#
# @app.route('/add_check')
# def add_check():
#     return '관심 종목 + 종목 추가'
#
# @app.route('/etc')
# def etc():
#     return '기타'


if __name__ == '__main__':
    app.run()
