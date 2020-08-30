# 외국인, 기관 투자 정보 크롤링

import pymysql
import pandas as pd

class foreigener_institution_info():

    def foreigener_institution_data(self):
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
                               "FROM kr_stock_invest_value " \
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

                    sql = "SELECT kr_stock_list.kr_stock_code, kr_stock_list.kr_stock_name, kr_stock_invest_value.institution,kr_stock_invest_value.foreigner, kr_stock_invest_value.foreigner_owned,kr_stock_invest_value.foreigner_percent " \
                          "FROM kr_stock_list " \
                          "JOIN kr_stock_invest_value " \
                          "ON kr_stock_list.kr_stock_code = kr_stock_invest_value.kr_stock_code " \
                          "WHERE DATE = '{}';".format(date)
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
