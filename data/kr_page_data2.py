import pymysql
import pandas as pd
import numpy as np
import re
import warnings
warnings.filterwarnings('ignore')

class low_value_stock():
    def one(self):

        connection = None
        row = None
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
                    sql = "SELECT * FROM kr_stock_statements WHERE DATE ='2019.12' OR DATE = '2020.03';"
                    cursor.execute(sql)
                    data = pd.read_sql_query(sql, connection)
        except Exception as e:
            print('->', e)

        finally:
            if connection:
                connection.close()
                # print(value)
        return data

    def two(self):

        connection = None
        row = None
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
                    date_data = str(cursor.fetchall())
                    first_index = date_data.find('(') + 1  # 형태가 이상해서 (,)위치 활용해 날짜 추출
                    second_index = date_data.find(')')
                    date_data = [i.strip() for i in date_data[first_index:second_index].split(',')]
                    if len(date_data[1]) == 1:
                        date_data[1] = '0' + date_data[1]
                    if len(date_data[2]) == 1:
                        date_data[2] = '0' + date_data[2]
                    recently_date = date_data[0] + '-' + date_data[1] + '-' + date_data[2]

                    sql = "SELECT * FROM kr_stock_weekly WHERE DATE = '{}';".format(recently_date)
                    cursor.execute(sql)
                    data = pd.read_sql_query(sql, connection)
        except Exception as e:
            print('->', e)

        finally:
            if connection:
                connection.close()

        return data

    def three(self):

        connection = None
        row = None
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
                    date_data = str(cursor.fetchall())
                    first_index = date_data.find('(') + 1  # 형태가 이상해서 (,)위치 활용해 날짜 추출
                    second_index = date_data.find(')')
                    date_data = [i.strip() for i in date_data[first_index:second_index].split(',')]
                    if len(date_data[1]) == 1:
                        date_data[1] = '0' + date_data[1]
                    if len(date_data[2]) == 1:
                        date_data[2] = '0' + date_data[2]
                    recently_date = date_data[0] + '-' + date_data[1] + '-' + date_data[2]

                    sql = "SELECT kr_stock_code, kr_stock_high_52week, kr_stock_low_52week, kr_stock_close FROM kr_stock_weekly WHERE DATE = '{}';".format(
                        recently_date)
                    cursor.execute(sql)
                    data = pd.read_sql_query(sql, connection)
        except Exception as e:
            print('->', e)

        finally:
            if connection:
                connection.close()

        return data

    def value(self):

        data = pd.DataFrame(low_value_stock().one())
        data2 = pd.DataFrame(low_value_stock().two())
        data3 = pd.DataFrame(low_value_stock().three())

        # 1. PER 구분 10이하, PBS 1 이하

        data_PER = data

        per = data_PER[['kr_stock_code', 'date', 'kind', 'PER']].fillna('999')
        per['PER'] = [float(i.replace(',', '')) for i in per['PER']]

        data_same_ind_per = data2[['kr_stock_code', 'kr_stock_same_ind_per']]
        data_same_ind_per['kr_stock_code'] = [int(i) for i in data_same_ind_per['kr_stock_code']]
        data_same_ind_per['kr_stock_same_ind_per'] = [re.sub('[^0-9.]', '', i) for i in
                                                      data_same_ind_per['kr_stock_same_ind_per']]
        ##1. 연간 PER 저평가
        per_10_1 = per[per['PER'] <= 10][per[per['PER'] <= 10]['kind'] == 1]
        per_10_1 = per_10_1.reset_index()[['kr_stock_code', 'kind', 'PER']]

        PER_1 = pd.merge(per_10_1, data_same_ind_per, on='kr_stock_code').drop_duplicates('kr_stock_code')
        PER_1['kr_stock_same_ind_per'] = [float(i) for i in PER_1['kr_stock_same_ind_per']]
        PER_1 = PER_1[PER_1['PER'] < PER_1['kr_stock_same_ind_per']]
        PER_1 = PER_1[['kr_stock_code', 'PER', 'kr_stock_same_ind_per']]

        ##2. 분기 PER 저평가
        per_10_2 = per[per['PER'] <= 10][per[per['PER'] <= 10]['kind'] == 2]
        per_10_2 = per_10_2[per_10_2['date'] == '2020.03']
        per_10_2 = per_10_2.reset_index()[['kr_stock_code', 'kind', 'PER']]

        PER_2 = pd.merge(per_10_2, data_same_ind_per, on='kr_stock_code').drop_duplicates('kr_stock_code')
        PER_2['kr_stock_same_ind_per'] = [float(i) for i in PER_2['kr_stock_same_ind_per']]
        PER_2 = PER_2[PER_2['PER'] < PER_2['kr_stock_same_ind_per']]
        PER_2 = PER_2[['kr_stock_code', 'PER', 'kr_stock_same_ind_per']]

        ##3. 연간 PBR 저평가
        data_PBR = data

        data_PBR_1 = data_PBR[data_PBR['kind'] == 1]
        data_PBR_1 = data_PBR_1[data_PBR_1['date'] == '2019.12']
        PBR_1 = data_PBR_1[['kr_stock_code', 'kind', 'PBR']].fillna('999.0')
        PBR_1['PBR'] = [float(i.replace('-', '0')) for i in PBR_1['PBR']]
        PBR_1 = PBR_1.drop_duplicates('kr_stock_code')
        PBR_1 = PBR_1[PBR_1['PBR'] < 1]

        ##4. 분기 PBR 저평가
        data_PBR_2 = data_PBR[data_PBR['kind'] == 2]
        data_PBR_2 = data_PBR_2[data_PBR_2['date'] == '2020.03']
        PBR_2 = data_PBR_2[['kr_stock_code', 'kind', 'PBR']].fillna('999.0')
        PBR_2['PBR'] = [float(i.replace('-', '0')) for i in PBR_2['PBR']]
        PBR_2 = PBR_2.drop_duplicates('kr_stock_code')
        PBR_2 = PBR_2[PBR_2['PBR'] < 1]

        ##5. 분기별 연간별 합치기
        PER_PBR_1 = pd.merge(PER_1, PBR_1, on='kr_stock_code')
        PER_PBR_2 = pd.merge(PER_2, PBR_2, on='kr_stock_code')
        PER_PBR = pd.merge(PER_PBR_1, PER_PBR_2, on='kr_stock_code')
        PER_PBR = PER_PBR.sort_values(by='kr_stock_same_ind_per_y').reset_index()
        PER_PBR = PER_PBR[PER_PBR.columns[1:]]
        PER_PBR_list = set(PER_PBR[PER_PBR['PER_x'] < PER_PBR['PER_y']]['kr_stock_code'])

        #2. ROE활용
        data_ROE = data

        ROE = data_ROE[['kr_stock_code', 'date', 'kind', 'ROE']].fillna('999')
        ROE['ROE'] = [float(i.replace(',', '')) for i in ROE['ROE']]

        ##1. 연간 ROE
        ROE_1 = ROE[ROE['kind'] == 1]
        ROE_1 = ROE_1[(ROE_1['ROE'] > 10) & (ROE_1['ROE'] < 998)].drop_duplicates('kr_stock_code')

        ##2. 분기 ROE
        ROE_2 = ROE[ROE['kind'] == 2]
        ROE_2 = ROE_2[ROE_2['date'] == '2020.03']
        ROE_2 = ROE_2[(ROE_2['ROE'] > 10) & (ROE_2['ROE'] < 998)].drop_duplicates('kr_stock_code')

        ##3. 합치기
        ROE = pd.merge(ROE_1, ROE_2, on='kr_stock_code').sort_values(by='ROE_y', ascending=False)
        ROE_list = set(list(ROE['kr_stock_code']))

        #3. 3년간 당기 순이익 => 이코드 내에서만 활용할것
        net_Income = data[['kr_stock_code', 'date', 'kind', 'net_Income']].fillna('-999')
        net_Income_list = []
        for i in net_Income['net_Income']:
            if i == '-':
                i = -999
                net_Income_list.append(i)
            else:
                net_Income_list.append(float(i.replace(',', '')))
        net_Income['net_Income'] = net_Income_list
        only_this_code = set(list(net_Income[net_Income['net_Income'] > 0]['kr_stock_code']))

        #4. 부채비율(100%이하), 당좌비율(100%이상), 유보비율(700%~1000%)
        three_ratio = data[['kr_stock_code', 'date', 'kind', 'debt_ratio', 'quick_ratio', 'resesrvation_ratio']].fillna(
            '-999')
        three_ratio['debt_ratio'] = [float(i.replace(',', '')) for i in three_ratio['debt_ratio']]
        three_ratio['quick_ratio'] = [float(i.replace(',', '')) for i in three_ratio['quick_ratio']]
        three_ratio['resesrvation_ratio'] = [float(i.replace(',', '')) for i in three_ratio['resesrvation_ratio']]
        three_ratio = three_ratio[(three_ratio['debt_ratio'] < 100) & (three_ratio['quick_ratio'] > 100) & (
                    three_ratio['resesrvation_ratio'] > 700)]
        three_ratio_list = set(list(three_ratio['kr_stock_code']))

        #########
        final_list = list(set(list(ROE_list & PER_PBR_list) + list(ROE_list & three_ratio_list) + list(
            three_ratio_list & PER_PBR_list)) - set(set(
            list(ROE_list & PER_PBR_list) + list(ROE_list & three_ratio_list) + list(
                three_ratio_list & PER_PBR_list)) - only_this_code))
        final_list.sort()
        return final_list


    def final_data_to_df(self):
        connection = None
        row = None
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
                    sql = "SELECT * FROM kr_stock_list;"
                    cursor.execute(sql)
                    data = cursor.fetchall()
                    data = pd.read_sql_query(sql, connection)[['kr_stock_code',
                                                               'kr_stock_name']].set_index('kr_stock_code')
                    col = low_value_stock().value()
                    data = data.loc[col].reset_index()
                    data = data.reset_index()
                    data.columns = ['1num','2kr_stock_code','3kr_stock_name']
                    data["1num"] = [i+1 for i in data['1num']]
                    data_dic = data.to_dict('index')

        except Exception as e:
            print('->', e)

        finally:
            if connection:
                connection.close()
                # print(value)
        return data_dic

    # 일부만 표시 , 메인페이지 내용
    def final_data_to_df_sample(self):
        connection = None
        row = None
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
                    sql = "SELECT * FROM kr_stock_list;"
                    cursor.execute(sql)
                    data = cursor.fetchall()
                    data = pd.read_sql_query(sql, connection)[['kr_stock_code',
                                                               'kr_stock_name']].set_index('kr_stock_code')
                    col = low_value_stock().value()
                    data = data.loc[col].reset_index()
                    data_dic = data[:10].to_dict('index')

        except Exception as e:
            print('->', e)

        finally:
            if connection:
                connection.close()
                # print(value)
        return data_dic
class foreigener_institution_info():
    def foreigener_institution_data(self):
        connection = None
        row = None
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
                    date_data = str(cursor.fetchall())
                    first_index = date_data.find('(') + 1  # 형태가 이상해서 (,)위치 활용해 날짜 추출
                    second_index = date_data.find(')')
                    date_data = [i.strip() for i in date_data[first_index:second_index].split(',')]
                    if len(date_data[1]) == 1:
                        date_data[1] = '0' + date_data[1]
                    if len(date_data[2]) == 1:
                        date_data[2] = '0' + date_data[2]
                    date = date_data[0] + '-' + date_data[1] + '-' + date_data[2]

                    sql = "SELECT kr_stock_list.kr_stock_code, kr_stock_list.kr_stock_name, kr_stock_invest_value.institution,kr_stock_invest_value.foreigner, kr_stock_invest_value.foreigner_owned,kr_stock_invest_value.foreigner_percent FROM kr_stock_list JOIN kr_stock_invest_value ON kr_stock_list.kr_stock_code = kr_stock_invest_value.kr_stock_code WHERE DATE = '{}';".format(
                        date)
                    cursor.execute(sql)
                    data = pd.read_sql_query(sql, connection)

                    # 기관 숫자 변경
                    institution_list = []
                    for i in list(data['institution']):
                        i = i.replace('+', '')
                        if ',' in i:
                            i = i.replace(',', '')
                            institution_list.append(int(i))
                        else:
                            institution_list.append(int(i))
                    data['institution'] = institution_list

                    # 외국인 열 숫자 변환
                    foreigner_list = []
                    for i in list(data['foreigner']):
                        i = i.replace('+', '')
                        if ',' in i:
                            i = i.replace(',', '')
                            foreigner_list.append(int(i))
                        else:
                            foreigner_list.append(int(i))
                    data['foreigner'] = foreigner_list

                    # 기관 상위 10개
                    institution_top = data.sort_values(by='institution').reset_index()[:10][
                        ['kr_stock_code', 'kr_stock_name', 'institution']]
                    institution_top_dic = institution_top[:10].to_dict('index')
                    # 기관 하위 10개
                    institution_down = data.sort_values(by='institution', ascending=False).reset_index()[:10][
                        ['kr_stock_code', 'kr_stock_name', 'institution']]
                    institution_down_dic = institution_down[:10].to_dict('index')

                    # 외국인 상위 10개
                    foreigner_top = data.sort_values(by='foreigner').reset_index()[:10][
                        ['kr_stock_code', 'kr_stock_name', 'foreigner']]
                    foreigner_top_dic = foreigner_top[:10].to_dict('index')

                    # 외국인 하위 10개
                    foreigner_down = data.sort_values(by='foreigner', ascending=False).reset_index()[:10][
                        ['kr_stock_code', 'kr_stock_name', 'foreigner']]
                    foreigner_down_dic = foreigner_down[:10].to_dict('index')

        except Exception as e:
            print('->', e)

        finally:
            if connection:
                connection.close()
                # print(value)
        return [institution_top_dic, institution_down_dic, foreigner_top_dic, foreigner_down_dic]
