# -*- coding: utf-8 -*-

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
	return "웹사이트 만들기"

@app.route('/한국주식')
def korea():
    return '국내주식 만드는 곳'

@app.route('/한국주식/<kr_stock>')
def get_kr_stock(kr_stock):
    return 'profile : ' + kr_stock

@app.route('/미국주식')
def america():
    return '해외주식 만드는 곳'

@app.route('/미국주식/<us_stock>')
def get_us_stock(us_stock):
    return 'profile : ' + us_stock

@app.route('/코인')
def coin():
    return '코인 만드는 곳'

@app.route('/코인/<coin_name>')
def get_coin(coin_name):
    return 'profile : ' + coin_name

if __name__ == '__main__':
    app.run()

