import pymysql
import pandas as pd
import numpy as np
import re
import warnings
warnings.filterwarnings('ignore')

class kr_page_data:

    def date(self):
        connection = None
        try:
            connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password='0000',
                                         db='web_db',
                                         port=3306,
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)
            if connection:

                with connection.cursor() as cursor:
                    date_sql = "select DATE " \
                          "FROM kr_stock_daily " \
                          "group BY DATE " \
                          "order by date DESC " \
                          "LIMIT 2;"
                    cursor.execute(date_sql)
                    date = cursor.fetchall()

                recently_data_raw = [i.strip() for i in str(date[0])[str(date[0]).find('(') + 1:str(date[0]).find(')')].split(',')]
                if len(recently_data_raw[1]) == 1:
                    recently_data_raw[1] = '0' + recently_data_raw[1]
                if len(recently_data_raw[2]) == 1:
                    recently_data_raw[2] = '0' + recently_data_raw[2]
                recently_data = recently_data_raw[0] + '-' + recently_data_raw[1] + '-' + recently_data_raw[2]

                nonrecently_raw = [i.strip() for i in str(date[1])[str(date[1]).find('(') + 1:str(date[1]).find(')')].split(',')]
                if len(nonrecently_raw[1]) == 1:
                    nonrecently_raw[1] = '0' + nonrecently_raw[1]
                if len(nonrecently_raw[2]) == 1:
                    nonrecently_raw[2] = '0' + nonrecently_raw[2]
                nonrecently_date = nonrecently_raw[0] + '-' + nonrecently_raw[1] + '-' + nonrecently_raw[2]

        except Exception as e:
            print('->', e)

        finally:
            if connection:
                connection.close()
                # print(value)

        return recently_data,nonrecently_date

    def code_name(self):
        connection = None
        try:
            connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password='0000',
                                         db='web_db',
                                         port=3306,
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)
            if connection:

                with connection.cursor() as cursor:
                    code_sql = "SELECT kr_stock_code, kr_stock_name " \
                               "FROM kr_stock_list;"
                    cursor.execute(code_sql)
                    code_name_data = cursor.fetchall()

                    code_name_dic = {}
                    for i in range(len(code_name_data)):
                        code_name_dic[code_name_data[i]['kr_stock_code']] = code_name_data[i]['kr_stock_name']

        except Exception as e:
            print('->', e)

        finally:
            if connection:
                connection.close()
                # print(value)

        return code_name_dic

    def change_rate_calculate(self):
        connection = None
        try:
            connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password='0000',
                                         db='web_db',
                                         port=3306,
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)
            if connection:
                # print('DB 오픈')

                with connection.cursor() as cursor:

                    recently_data_sql = "SELECT kr_stock_code, DATE, kr_stock_close, kr_stock_open, kr_stock_high, " \
                                        "kr_stock_low, kr_stock_volume " \
                                        "FROM kr_stock_daily " \
                                        "WHERE DATE = '{}';".format(kr_page_data().date()[0])
                    cursor.execute(recently_data_sql)
                    recently_data = cursor.fetchall()
                    recently_data = [j.values() for j in recently_data]


                    nonrecently_data_sql = "SELECT kr_stock_code, DATE, kr_stock_close, kr_stock_open, kr_stock_high, " \
                                           "kr_stock_low, kr_stock_volume " \
                                        "FROM kr_stock_daily " \
                                        "WHERE DATE = '{}';".format(kr_page_data().date()[1])
                    cursor.execute(nonrecently_data_sql)
                    nonrecently_data = cursor.fetchall()
                    nonrecently_data = [j.values() for j in nonrecently_data]
                    code_list = [list(i)[0] for i in nonrecently_data]

                    price_diff = []
                    for i in range(len(recently_data)):
                        recent = list(recently_data[i])[2:]
                        non_recent = list(nonrecently_data[i])[2:]
                        value_list = []
                        for j in range(len(recent)):
                            if recent[j]-non_recent[j] == 0:
                                value_list.append('0')
                                value_list.append('0'+'%')
                            else:
                                value_diff = recent[j] - non_recent[j]
                                value_percentage = round(((recent[j] - non_recent[j]) / recent[j]) * 100, 2)
                                value_list.append(value_diff)
                                value_list.append(str(value_percentage)+'%')
                        price_diff.append(value_list)

                    final_dic={}
                    for i in range(len(code_list)):
                        final_dic[code_list[i]] = price_diff[i]

        except Exception as e:
            print('->', e)

        finally:
            if connection:
                connection.close()
                # print(value)
        return final_dic

    def rank(self):
        connection = None
        try:
            connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password='0000',
                                         db='web_db',
                                         port=3306,
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)
            if connection:
                # print('DB 오픈')

                with connection.cursor() as cursor:
                    date_sql = "select DATE " \
                               "FROM kr_stock_weekly " \
                               "group BY DATE " \
                               "order by date DESC " \
                               "LIMIT 1;"
                    cursor.execute(date_sql)
                    date = cursor.fetchall()
                    recently_data_raw = [i.strip() for i in
                                         str(date[0])[str(date[0]).find('(') + 1:str(date[0]).find(')')].split(',')]
                    if len(recently_data_raw[1]) == 1:
                        recently_data_raw[1] = '0' + recently_data_raw[1]
                    if len(recently_data_raw[2]) == 1:
                        recently_data_raw[2] = '0' + recently_data_raw[2]
                    date = recently_data_raw[0] + '-' + recently_data_raw[1] + '-' + recently_data_raw[2]

                    date_sql = "SELECT * " \
                               "FROM ( SELECT kr_stock_weekly.kr_stock_code, kr_stock_weekly.DATE, " \
                               "kr_stock_weekly.kr_stock_kospi_rank, kr_stock_weekly.kr_stock_market_value, " \
                               "kr_stock_list.kr_stock_name " \
                               "FROM kr_stock_weekly " \
                               "JOIN kr_stock_list " \
                               "ON kr_stock_list.kr_stock_code = kr_stock_weekly.kr_stock_code ) C " \
                               "WHERE C.DATE = '{}';".format(date)
                    cursor.execute(date_sql)
                    data = cursor.fetchall()
                    rank_list = []
                    for i in data:
                        try:
                            rank = i['kr_stock_kospi_rank']
                            rank_list.append(int(rank[rank.find('피') + 1:rank.find('위')]))
                        except:
                            rank_list.append(999)
                    rank_index = []
                    for j in range(1,21,1):
                        try:
                            rank_index.append(rank_list.index(j))
                        except:
                            continue
                    rank_final_dic = {}
                    for num,index in enumerate(rank_index):
                        final_data = data[index]
                        code = final_data['kr_stock_code']
                        name = final_data['kr_stock_name']
                        rank = final_data['kr_stock_kospi_rank'][final_data['kr_stock_kospi_rank'].find('피 ')+2:]
                        capital = final_data['kr_stock_market_value']
                        value_dic = {}
                        for name,value in zip(['code','name','rank','capital'],[code, name, rank, capital]):
                            value_dic[name] = value
                        rank_final_dic[num] = value_dic

        # except Exception as e:
        #     print('->', e)

        finally:
            if connection:
                connection.close()
        return rank_final_dic

    def volatilty(self):
        connection = None
        try:
            connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password='0000',
                                         db='web_db',
                                         port=3306,
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)
            if connection:
                # print('DB 오픈')

                with connection.cursor() as cursor:

                    recently_data_sql = "SELECT kr_stock_code, kr_stock_close " \
                                        "FROM kr_stock_daily " \
                                        "WHERE DATE = '{}';".format(kr_page_data().date()[0])
                    cursor.execute(recently_data_sql)
                    recently_data = cursor.fetchall()


                    nonrecently_data_sql = "SELECT kr_stock_code, kr_stock_close " \
                                        "FROM kr_stock_daily " \
                                        "WHERE DATE = '{}';".format(kr_page_data().date()[1])
                    cursor.execute(nonrecently_data_sql)
                    nonrecently_data = cursor.fetchall()

                    code_list = [i['kr_stock_code'] for i in nonrecently_data]
                    change_rate_list = []
                    for recently, nonrecently in zip([j['kr_stock_close'] for j in recently_data],[j['kr_stock_close'] for j in nonrecently_data]):
                        try:
                            change_rate = round((recently - nonrecently)/nonrecently * 100,2)
                            change_rate_list.append(change_rate)
                        except:
                            change_rate_list.append(0)

                    code_name_dic = kr_page_data().code_name()

                    rate_df = pd.DataFrame([code_list,change_rate_list]).T
                    rate_df.columns = ['code','rate']

                    # top, down 순위
                    top_rate_df = rate_df.sort_values(by='rate').reset_index().loc[:10][['code','rate']]
                    down_rate_df = rate_df.sort_values(by='rate', ascending=False).reset_index().loc[:10][['code','rate']]

                    top_rate_list = []
                    down_rate_list = []
                    for i,j in zip(top_rate_df['code'],down_rate_df['code']):
                        top_rate_list.append(code_name_dic[i])
                        down_rate_list.append(code_name_dic[j])

                    top_rate_df['name'] = top_rate_list
                    top_rate_df = top_rate_df[['code','name','rate']]

                    top_final_dic = {}
                    for i in range(len(top_rate_df)):
                        final_data = top_rate_df.loc[i]
                        code = final_data['code']
                        name = final_data['name']
                        top = final_data['rate']
                        top_dic = {}
                        for name, value in zip(['code', 'name', 'rate'], [code, name, top]):
                            top_dic[name] = value
                        top_final_dic[i] = top_dic


                    down_rate_df['name'] = down_rate_list
                    down_rate_df = down_rate_df[['code','name','rate']]

                    down_final_dic = {}
                    for i in range(len(down_rate_df)):
                        final_data = down_rate_df.loc[i]
                        code = final_data['code']
                        name = final_data['name']
                        down = final_data['rate']
                        down_dic = {}
                        for name, value in zip(['code', 'name', 'rate'], [code, name, down]):
                            down_dic[name] = value
                        down_final_dic[i] = down_dic

                    # 전체 절대값 순위
                    rate_df_edit = rate_df
                    rate_df_edit['abs_rate'] = [abs(i) for i in rate_df_edit['rate']]
                    rate_df_edit = rate_df_edit.sort_values(by='abs_rate', ascending=False)
                    name_rate_list = []
                    for i in rate_df_edit['code']:
                        name_rate_list.append(code_name_dic[i])
                    rate_df_edit['name'] = name_rate_list
                    rate_df_edit = rate_df_edit.reset_index().loc[:9]
                    rate_df_edit = rate_df_edit[['code', 'name','rate']]

                    abs_final_dic = {}
                    for i in range(len(rate_df_edit)):
                        final_data = rate_df_edit.loc[i]
                        code = final_data['code']
                        name = final_data['name']
                        abs_ = final_data['rate']
                        abs_dic = {}
                        for name, value in zip(['code', 'name', 'rate'], [code, name, abs_]):
                            abs_dic[name] = value
                        abs_final_dic[i] = abs_dic

        except Exception as e:
            print('->', e)

        finally:
            if connection:
                connection.close()
        return [top_final_dic, down_final_dic, abs_final_dic]

    def volume(self):
        connection = None
        try:
            connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password='0000',
                                         db='web_db',
                                         port=3306,
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)
            if connection:
                # print('DB 오픈')

                with connection.cursor() as cursor:

                    recently_data_sql = "SELECT kr_stock_code, kr_stock_volume " \
                                        "FROM kr_stock_daily " \
                                        "WHERE DATE = '{}';".format(kr_page_data().date()[0])
                    cursor.execute(recently_data_sql)
                    recently_data = cursor.fetchall()

                    code_list = []
                    volume_list = []
                    for i in range(len(recently_data)):
                        code_list.append(int(recently_data[i]['kr_stock_code']))
                        volume_list.append(recently_data[i]['kr_stock_volume'])

                    code_name_dic = kr_page_data().code_name()

                    volume_df = pd.DataFrame([code_list,volume_list]).T
                    volume_df.columns = ['code','volume']
                    volume_df = volume_df.sort_values(by='volume', ascending=False)
                    volume_df = volume_df.reset_index().loc[:10]
                    name_volume_list = []
                    for i in volume_df['code']:
                        name_volume_list.append(code_name_dic[i])
                    volume_df['name'] = name_volume_list
                    volume_df = volume_df[['code', 'name','volume']]
                    vol_final_dic = {}
                    for i in range(len(volume_df)):
                        final_data = volume_df.loc[i]
                        code = final_data['code']
                        name = final_data['name']
                        volume = final_data['volume']
                        value_dic = {}
                        for name, value in zip(['code', 'name', 'volume'], [code, name, volume]):
                            value_dic[name] = value
                        vol_final_dic[i] = value_dic
        except Exception as e:
            print('->', e)

        finally:
            if connection:
                connection.close()
        return vol_final_dic


def low_value_stock():
    connection = None
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='0000',
                                     db='web_db',
                                     port=3306,
                                     charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)
        if connection:
            # print('DB 오픈')

            with connection.cursor() as cursor:

                recently_data_sql = "SELECT kr_stock_code, kr_stock_volume " \
                                    "FROM kr_stock_daily " \
                                    "WHERE DATE = '{}';".format(kr_page_data().date()[0])
                cursor.execute(recently_data_sql)
                recently_data = cursor.fetchall()

                code_list = []
                volume_list = []
                for i in range(len(recently_data)):
                    code_list.append(int(recently_data[i]['kr_stock_code']))
                    volume_list.append(recently_data[i]['kr_stock_volume'])

                code_name_dic = kr_page_data().code_name()

                volume_df = pd.DataFrame([code_list, volume_list]).T
                volume_df.columns = ['code', 'volume']
                volume_df = volume_df.sort_values(by='volume', ascending=False)
                volume_df = volume_df.reset_index().loc[:10]
                name_volume_list = []
                for i in volume_df['code']:
                    name_volume_list.append(code_name_dic[i])
                volume_df['name'] = name_volume_list
                volume_df = volume_df[['code', 'name', 'volume']]
                vol_final_dic = {}
                for i in range(len(volume_df)):
                    final_data = volume_df.loc[i]
                    code = final_data['code']
                    name = final_data['name']
                    volume = final_data['volume']
                    value_dic = {}
                    for name, value in zip(['code', 'name', 'volume'], [code, name, volume]):
                        value_dic[name] = value
                    vol_final_dic[i] = value_dic
    except Exception as e:
        print('->', e)

    finally:
        if connection:
            connection.close()
    return vol_final_dic