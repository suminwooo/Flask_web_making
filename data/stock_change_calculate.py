# 주가 변화율 계산

import pymysql
import pandas as pd
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

                recently_data_raw = [i.strip() for i in
                                     str(date[0])[str(date[0]).find('(') + 1:str(date[0]).find(')')].split(',')]
                if len(recently_data_raw[1]) == 1:
                    recently_data_raw[1] = '0' + recently_data_raw[1]
                if len(recently_data_raw[2]) == 1:
                    recently_data_raw[2] = '0' + recently_data_raw[2]
                recently_data = recently_data_raw[0] + '-' + recently_data_raw[1] + '-' + recently_data_raw[2]

                nonrecently_raw = [i.strip() for i in
                                   str(date[1])[str(date[1]).find('(') + 1:str(date[1]).find(')')].split(',')]
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

        return recently_data, nonrecently_date

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
        # try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='0000',
                                     db='web_db',
                                     port=3306,
                                     charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)
        if connection:

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
                        if recent[j] - non_recent[j] == 0:
                            value_list.append('0')
                            value_list.append('0' + '%')
                        else:
                            try:
                                value_diff = recent[j] - non_recent[j]
                                value_percentage = round(((recent[j] - non_recent[j]) / recent[j]) * 100, 2)
                                value_list.append(value_diff)
                                value_list.append(str(value_percentage) + '%')
                            except:
                                value_list.append('error')
                                value_list.append('error')
                    price_diff.append(value_list)

                final_dic = {}
                for i in range(len(code_list)):
                    final_dic[code_list[i]] = price_diff[i]

        return final_dic

    def rank(self, market_type):
        connection = None
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='0000',
                                     db='web_db',
                                     port=3306,
                                     charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)

        with connection.cursor() as cursor:
            data_sql = "SELECT * " \
                       "FROM kr_stock_weekly " \
                       "WHERE DATE = (select DATE " \
                       "FROM kr_stock_weekly " \
                       "group BY DATE " \
                       "order by date DESC " \
                       "LIMIT 1);"
            cursor.execute(data_sql)
            data = cursor.fetchall()
            data = pd.DataFrame(data)
            data = data.reset_index()
            data = data[data.columns[1:]]

            kospi_rank_list = []
            kosdaq_rank_list = []
            for num, i in enumerate(list(data['kr_stock_kospi_rank'])):
                if i.split()[0] == '코스피':
                    kospi_rank_list.append(num)
                elif i.split()[0] == '코스닥':
                    kosdaq_rank_list.append(num)
                else:
                    continue

            code_name_dic = kr_page_data().code_name()
            if market_type == 'kospi':
                # 코스피 df 정리후 dic
                kospi_rank_df = data.loc[kospi_rank_list][
                    ['kr_stock_code', 'kr_stock_kospi_rank', 'kr_stock_market_value']]
                kospi_rank_df = kospi_rank_df.reset_index()
                kospi_rank_df = kospi_rank_df[kospi_rank_df.columns[1:]]
                kospi_rank_df['kr_stock_name'] = [code_name_dic[int(i)] for i in kospi_rank_df['kr_stock_code']]
                kospi_new_df = pd.DataFrame()
                for i in range(len(kospi_rank_df)):
                    each_df = kospi_rank_df.loc[i]
                    code = each_df['kr_stock_code']
                    name = each_df['kr_stock_name']
                    rank = each_df['kr_stock_kospi_rank'][each_df['kr_stock_kospi_rank'].find('피 ') + 2:
                                                          each_df['kr_stock_kospi_rank'].find('위')]
                    capital = each_df['kr_stock_market_value']
                    if int(rank) < 60:
                        each_new_df = pd.DataFrame([code, name, rank, capital]).T
                        kospi_new_df = pd.concat([kospi_new_df, each_new_df], axis=0)
                kospi_new_df.columns = ['kr_stock_code', 'kr_stock_name', 'kr_stock_kospi_rank',
                                        'kr_stock_market_value']
                kospi_new_df['kr_stock_kospi_rank'] = [int(i) for i in kospi_new_df['kr_stock_kospi_rank']]
                kospi_new_df = kospi_new_df.sort_values(by='kr_stock_kospi_rank')
                kospi_new_df = kospi_new_df.reset_index().loc[:50]
                kospi_new_df = kospi_new_df[kospi_new_df.columns[1:]]
                kospi_new_df = kospi_new_df[
                    ['kr_stock_kospi_rank', 'kr_stock_code', 'kr_stock_name', 'kr_stock_market_value']]
                kospi_new_df.columns = ['1rank', '2code', '3name', '4capital']
                kospi_new_df['2code'] = [str(i).zfill(6) for i in kospi_new_df['2code']]
                kospi_rank_final_dic = kospi_new_df.to_dict('index')

                return kospi_rank_final_dic


            elif market_type == 'kosdaq':
                # 코스닥 df 정리후 dic
                kosdaq_rank_df = data.loc[kosdaq_rank_list][
                    ['kr_stock_code', 'kr_stock_kospi_rank', 'kr_stock_market_value']]
                kosdaq_rank_df = kosdaq_rank_df.reset_index()
                kosdaq_rank_df = kosdaq_rank_df[kosdaq_rank_df.columns[1:]]
                kosdaq_rank_df['kr_stock_name'] = [code_name_dic[int(i)] for i in kosdaq_rank_df['kr_stock_code']]
                kosdaq_new_df = pd.DataFrame()
                for i in range(len(kosdaq_rank_df)):
                    each_df = kosdaq_rank_df.loc[i]
                    code = each_df['kr_stock_code']
                    name = each_df['kr_stock_name']
                    rank = each_df['kr_stock_kospi_rank'][each_df['kr_stock_kospi_rank'].find('닥 ') + 2:
                                                          each_df['kr_stock_kospi_rank'].find('위')]
                    capital = each_df['kr_stock_market_value']
                    if int(rank) < 60:
                        each_new_df = pd.DataFrame([code, name, rank, capital]).T
                        kosdaq_new_df = pd.concat([kosdaq_new_df, each_new_df], axis=0)
                kosdaq_new_df.columns = ['kr_stock_code', 'kr_stock_name', 'kr_stock_kosdaq_rank',
                                         'kr_stock_market_value']
                kosdaq_new_df['kr_stock_kosdaq_rank'] = [int(i) for i in kosdaq_new_df['kr_stock_kosdaq_rank']]
                kosdaq_new_df = kosdaq_new_df.sort_values(by='kr_stock_kosdaq_rank')
                kosdaq_new_df = kosdaq_new_df.reset_index().loc[:50]
                kosdaq_new_df = kosdaq_new_df[kosdaq_new_df.columns[1:]]
                kosdaq_new_df = kosdaq_new_df[
                    ['kr_stock_kosdaq_rank', 'kr_stock_code', 'kr_stock_name', 'kr_stock_market_value']]
                kosdaq_new_df.columns = ['1rank', '2code', '3name', '4capital']
                kosdaq_new_df['2code'] = [str(i).zfill(6) for i in kosdaq_new_df['2code']]
                kosdaq_rank_final_dic = kosdaq_new_df.to_dict('index')

                return kosdaq_rank_final_dic

    def volatilty(self, market_type):
        connection = None
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='0000',
                                     db='web_db',
                                     port=3306,
                                     charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)

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

            kospi_sql = "SELECT kr_stock_code, kr_stock_name FROM kr_stock_list WHERE market = 'KOSPI';"
            cursor.execute(kospi_sql)
            kospi_list = cursor.fetchall()
            kospi_list = list(pd.DataFrame(kospi_list)['kr_stock_code'])

            kosdaq_sql = "SELECT kr_stock_code, kr_stock_name FROM kr_stock_list WHERE market = 'KOSDAQ';"
            cursor.execute(kosdaq_sql)
            kosdaq_list = cursor.fetchall()
            kosdaq_list = list(pd.DataFrame(kosdaq_list)['kr_stock_code'])

            code_list = [i['kr_stock_code'] for i in nonrecently_data]
            change_rate_list = []
            for recently, nonrecently in zip([j['kr_stock_close'] for j in recently_data],
                                             [j['kr_stock_close'] for j in nonrecently_data]):
                try:
                    change_rate = round((recently - nonrecently) / nonrecently * 100, 2)
                    change_rate_list.append(change_rate)
                except:
                    change_rate_list.append(0)

            code_name_dic = kr_page_data().code_name()

            rate_df = pd.DataFrame([code_list, change_rate_list]).T
            rate_df.columns = ['code', 'rate']
            rate_df['code'] = [int(i) for i in rate_df['code']]
            rate_df = rate_df.set_index('code')

            if market_type == 'kospi':

                rate_df = rate_df.loc[list(set(rate_df.index) - set(kosdaq_list))]
                rate_df = rate_df.reset_index()
                rate_df.columns = ['code', 'rate']

                # top, down 순위
                top_rate_df = rate_df.sort_values(by='rate').reset_index().loc[:9][['code', 'rate']]
                down_rate_df = rate_df.sort_values(by='rate', ascending=False).reset_index().loc[:9][['code', 'rate']]

                top_rate_list = []
                down_rate_list = []
                for i, j in zip(top_rate_df['code'], down_rate_df['code']):
                    top_rate_list.append(code_name_dic[i])
                    down_rate_list.append(code_name_dic[j])

                top_rate_df['name'] = top_rate_list
                top_rate_df = top_rate_df[['code', 'name', 'rate']]

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
                down_rate_df = down_rate_df[['code', 'name', 'rate']]

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
                rate_df_edit = rate_df_edit[['code', 'name', 'rate']]

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

                connection.close()

                return [top_final_dic, down_final_dic, abs_final_dic]


            elif market_type == 'kosdaq':
                rate_df = rate_df.loc[list(set(rate_df.index) - set(kospi_list))]
                rate_df = rate_df.reset_index()
                rate_df.columns = ['code', 'rate']

                # top, down 순위
                top_rate_df = rate_df.sort_values(by='rate').reset_index().loc[:9][['code', 'rate']]
                down_rate_df = rate_df.sort_values(by='rate', ascending=False).reset_index().loc[:9][['code', 'rate']]

                top_rate_list = []
                down_rate_list = []
                for i, j in zip(top_rate_df['code'], down_rate_df['code']):
                    top_rate_list.append(code_name_dic[i])
                    down_rate_list.append(code_name_dic[j])

                top_rate_df['name'] = top_rate_list
                top_rate_df = top_rate_df[['code', 'name', 'rate']]

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
                down_rate_df = down_rate_df[['code', 'name', 'rate']]

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
                rate_df_edit = rate_df_edit[['code', 'name', 'rate']]

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

                connection.close()

                return [top_final_dic, down_final_dic, abs_final_dic]

    def volume(self, market_type):
        connection = None

        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='0000',
                                     db='web_db',
                                     port=3306,
                                     charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)

        with connection.cursor() as cursor:

            recently_data_sql = "SELECT kr_stock_code, kr_stock_volume " \
                                "FROM kr_stock_daily " \
                                "WHERE DATE = '{}';".format(kr_page_data().date()[0])
            cursor.execute(recently_data_sql)
            recently_data = cursor.fetchall()

            kospi_sql = "SELECT kr_stock_code, kr_stock_name FROM kr_stock_list WHERE market = 'KOSPI';"
            cursor.execute(kospi_sql)
            kospi_list = cursor.fetchall()
            kospi_list = list(pd.DataFrame(kospi_list)['kr_stock_code'])
            kospi_list = [int(i) for i in kospi_list]

            kosdaq_sql = "SELECT kr_stock_code, kr_stock_name FROM kr_stock_list WHERE market = 'KOSDAQ';"
            cursor.execute(kosdaq_sql)
            kosdaq_list = cursor.fetchall()
            kosdaq_list = list(pd.DataFrame(kosdaq_list)['kr_stock_code'])
            kosdaq_list = [int(i) for i in kosdaq_list]

            code_list = []
            volume_list = []
            for i in range(len(recently_data)):
                code_list.append(int(recently_data[i]['kr_stock_code']))
                volume_list.append(recently_data[i]['kr_stock_volume'])

            code_name_dic = kr_page_data().code_name()

            volume_df = pd.DataFrame([code_list, volume_list]).T
            volume_df.columns = ['code', 'volume']
            volume_df['code'] = [int(i) for i in volume_df['code']]

            if market_type == 'kospi':

                volume_df = volume_df.set_index('code').loc[list(set(list(volume_df['code'])) - set(kosdaq_list))]
                volume_df = volume_df.sort_values(by='volume', ascending=False)
                volume_df = volume_df.reset_index().loc[:9]
                name_volume_list = []
                for i in volume_df['code']:
                    name_volume_list.append(code_name_dic[i])
                volume_df['name'] = name_volume_list
                volume_df = volume_df[['code', 'name', 'volume']]

                vol_final_dic = {}
                for i in range(len(volume_df)):
                    final_data = volume_df.loc[i]
                    code = str(final_data['code']).zfill(6)
                    name = final_data['name']
                    volume = final_data['volume']
                    value_dic = {}
                    for name, value in zip(['code', 'name', 'volume'], [code, name, volume]):
                        value_dic[name] = value
                    vol_final_dic[i] = value_dic
                connection.close()

                return vol_final_dic
            elif market_type == 'kosdaq':

                volume_df = volume_df.set_index('code').loc[list(set(list(volume_df['code'])) - set(kospi_list))]
                volume_df = volume_df.sort_values(by='volume', ascending=False)
                volume_df = volume_df.reset_index().loc[:9]
                name_volume_list = []
                for i in volume_df['code']:
                    name_volume_list.append(code_name_dic[i])
                volume_df['name'] = name_volume_list
                volume_df = volume_df[['code', 'name', 'volume']]

                vol_final_dic = {}
                for i in range(len(volume_df)):
                    final_data = volume_df.loc[i]
                    code = str(final_data['code']).zfill(6)
                    name = final_data['name']
                    volume = final_data['volume']
                    value_dic = {}
                    for name, value in zip(['code', 'name', 'volume'], [code, name, volume]):
                        value_dic[name] = value
                    vol_final_dic[i] = value_dic
                connection.close()

                return vol_final_dic