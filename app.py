
##################################################################
# 플라스크 실행 라이브러리

from __future__ import with_statement
import time
from flask_restful import Resource, Api
from flask import jsonify
from sqlite3 import dbapi2 as sqlite3
from hashlib import md5
from datetime import datetime
from contextlib import closing
from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash
from werkzeug.security import check_password_hash, generate_password_hash

##################################################################
# 데이터 라이브러리

from etc.date import date_method # 시간
from web_engine.web_engine import web_engine # 검색

from data.naver_news_crolling import naver_news
from data.stock_change_calculate import kr_page_data
from data.mysql_to_python_api import korea_detail_information
from data.mysql_to_python_straight import main_page_information, detail_serach_page_imformation
from data.forigner_institution import foreinger_institurion
from data.low_value_stock_code import low_value_stock

##################################################################

# configuration
DATABASE = 'database_test.db' # 실행되는 위치에 저장됨 / 위치 지정 가능
PER_PAGE = 30
DEBUG = True
SECRET_KEY = 'development key'

# 이 코드가 실행되면 자동으로 데이터 베이스를 초기화하여 데이트 베이스에 follower, message, user이라는 테이블이 생성됨

app = Flask(__name__) # 플라스크 인스턴스 생성
app.config.from_object(__name__)
app.config.from_envvar('MINITWIT_SETTINGS', silent=True)
# LASKR_SETTINGS라는 환경변수의 경로에 있는 파일에서 값을 가져와서 Config 객체에 설정

##################################################################
# 기본 셋팅 구현

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


def get_user_id(username):
    rv = g.db.execute('select user_id from user where username = ?',
                       [username]).fetchone()
    return rv[0] if rv else None


def format_datetime(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')

# add some filters to jinja
app.jinja_env.filters['datetimeformat'] = format_datetime

@app.before_request
def before_request():
    g.db = connect_db()
    g.user = None
    if 'user_id' in session:
        g.user = query_db('select * from user where user_id = ?',
                          [session['user_id']], one=True)


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


##################################################################
# 로그인 관련 구현

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Logs the user in."""
    if g.user:
        return redirect(url_for('sales_log'))
    error = None
    if request.method == 'POST':
        user = query_db('''select * from user where
            username = ?''', [request.form['username']], one=True)
        if user is None:
            error = 'Invalid username'
        elif not check_password_hash(user['pw_hash'],
                                     request.form['password']):
            error = 'Invalid password'
        else:
            flash('You were logged in')
            session['user_id'] = user['user_id']
            return redirect(url_for('transaction_list'))
    return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registers the user."""
    if g.user:
        return redirect(url_for('timeline'))
    error = None
    if request.method == 'POST':
        if not request.form['username']:
            error = 'You have to enter a username'
        elif not request.form['email'] or \
                 '@' not in request.form['email']:
            error = 'You have to enter a valid email address'
        elif not request.form['password']:
            error = 'You have to enter a password'
        elif request.form['password'] != request.form['password2']:
            error = 'The two passwords do not match'
        elif get_user_id(request.form['username']) is not None:
            error = 'The username is already taken'
        else:
            g.db.execute('''insert into user (
                username, email, pw_hash) values (?, ?, ?)''',
                [request.form['username'], request.form['email'],
                 generate_password_hash(request.form['password'])])
            g.db.commit()
            flash('You were successfully registered and can login now')
            return redirect(url_for('login'))
    return render_template('register.html', error=error)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('main_page'))

##################################################################
# 매매기록 관련 코드


@app.route('/add_search_stock', methods=['POST'])
def add_search_stock():
    if 'user_id' not in session:
        abort(401)
    g.db.execute('''insert into 
        message (author_id, add_stock_type, register_stock_name_code,
        register_stock_price,register_stock_reason, pub_date) 
        values (?, ?, ?, ?, ?, ?)''', (session['user_id'],
                                      request.form['add_stock_type'],
                                      request.form['register_stock_name_code'],
                                      request.form['register_stock_price'],
                                      request.form['register_stock_reason'],
                                      int(time.time())))

    g.db.commit()
    flash('Your message was recorded')
    return redirect(url_for('transaction_list'))

@app.route('/transaction_list')
def transaction_list():

    if not g.user:
        return redirect(url_for('user_transaction_list'))
    messages = query_db('''
        select message.*, user.* 
        from message, user
        where message.author_id = user.user_id and (
            user.user_id = ? or
            user.user_id in (select whom_id from follower
                                    where who_id = ?))
        order by message.pub_date desc limit ?''',
        [session['user_id'], session['user_id'], PER_PAGE])
    import pandas as pd
    print(pd.DataFrame(messages)[['add_stock_type','register_stock_name_code','register_stock_price',
                                  'register_stock_reason','pub_date']])

    return render_template('transaction_list.html',
                           messages=messages)

##################################################################

# API 관련
api = Api(app)
app.config['JSON_AS_ASCII'] = False

class api_data(Resource):

    def get(self):
        kospi_rank_data = kr_page_data().rank('kospi')
        kosdaq_rank_data = kr_page_data().rank('kosdaq')
        kospi_low_value_data = low_value_stock().final_data_to_df('kospi')[0]
        kosdaq_low_value_data = low_value_stock().final_data_to_df('kosdaq')[0]
        # total_stock_price = total_stock_list().stock_information()

        message = {
            # 'total_price_data': total_stock_price,
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
# 검색 관련


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
    price_data = korea_detail_information().kr_price_data(int(search_word_code))
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
# 데이터 관련 페이지

@app.route('/', methods=['GET', 'POST'])
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



@app.route('/twit') # 게시판 : 추후 타임라인처럼 해보기
def twit():
    return render_template('twit.html')


###################################################################
# 마무리

if __name__ == "__main__":
    init_db() # 데이터베이스 초기화
    app.run() # 서버 실행 코드