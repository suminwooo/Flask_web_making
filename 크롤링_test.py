from flask import Flask, render_template
from main_data import main_page_value

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('main_page.html', main_page_value = main_page_value())
@app.route('/korea_stock')
def korea_stock():
    return render_template('korea_stock.html')

@app.route('/korea_stock/<kr_stock>')
def get_kr_stock(kr_stock):
    return 'profile : '+kr_stock

@app.route('/us_stock')
def us_stock():
    return render_template('us_stock.html')

@app.route('/us_stock/<us_stock>')
def get_us_stock(us_stock):
    return 'profile : ' + us_stock

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