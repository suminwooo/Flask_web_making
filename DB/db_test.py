import pymysql


def main_page_data(date):

    connection = None
    row = None
    try:
        connection = pymysql.connect(host = 'localhost',
                                 user = 'root',
                                 password = '0000',
                                 db = 'web_db',
                                 port = 3306,
                                 charset = 'utf8',
                                 cursorclass = pymysql.cursors.DictCursor)
        if connection:
            # print('DB 오픈')

            with connection.cursor() as cursor:
                sql = "SELECT * FROM main_page_data WHERE date='{}';".format(date)
                cursor.execute(sql)
                row = cursor.fetchall()
                # print(row)

    except Exception as e:
        print('->', e)

    finally:
        if connection:
            connection.close()
            # print('DB 닫기')
            # print(row)
    return row[0]


def korea_code_data():

    connection = None
    row = None
    try:
        connection = pymysql.connect(host = 'localhost',
                                 user = 'root',
                                 password = '0000',
                                 db = 'web_db',
                                 port = 3306,
                                 charset = 'utf8',
                                 cursorclass = pymysql.cursors.DictCursor)
        if connection:
            # print('DB 오픈')

            with connection.cursor() as cursor:
                sql = "SELECT kr_stock_code, kr_stock_name FROM kr_stock_list;"
                cursor.execute(sql)
                row = cursor.fetchall()
                code, name = [], []
                for i in row :
                    code.append(i['kr_stock_code'])
                    name.append(i['kr_stock_name'])
    except Exception as e:
        print('->', e)

    finally:
        if connection:
            connection.close()
            # print(value)
    return [code, name]

####################### 한국 종목 상세 검색 부분 #######################

class korea_detail_information:

    def kr_price_data(self, code):

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
                    # 최신 date 출력
                    date_sql = "select DATE " \
                               "FROM kr_stock_daily " \
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

                    data_sql = "SELECT * " \
                               "FROM kr_stock_daily " \
                               "WHERE DATE ='{}' " \
                               "AND kr_stock_code='{}';".format(recently_date, code)
                    cursor.execute(data_sql)
                    data = cursor.fetchall()

        except Exception as e:
            print('->', e)

        finally:
            if connection:
                connection.close()
                # print(value)
        return data[0]

    def kr_detail_data(self, code):

        connection = None
        try:
            connection = pymysql.connect(host = 'localhost',
                                     user = 'root',
                                     password = '0000',
                                     db = 'web_db',
                                     port = 3306,
                                     charset = 'utf8',
                                     cursorclass = pymysql.cursors.DictCursor)
            if connection:
                # print('DB 오픈')

                with connection.cursor() as cursor:
                    # 최신 date 출력
                    date_sql = "select DATE " \
                          "FROM kr_stock_weekly " \
                          "group BY DATE " \
                          "order by date DESC " \
                          "LIMIT 1;"
                    cursor.execute(date_sql)
                    date_data = str(cursor.fetchall())
                    first_index = date_data.find('(')+1 # 형태가 이상해서 (,)위치 활용해 날짜 추출
                    second_index = date_data.find(')')
                    date_data = [i.strip() for i in date_data[first_index:second_index].split(',')]
                    if len(date_data[1]) == 1:
                        date_data[1] = '0'+ date_data[1]
                    if len(date_data[2]) == 1:
                        date_data[2] = '0'+ date_data[2]
                    recently_date = date_data[0]+'-'+date_data[1]+'-'+date_data[2]

                    data_sql = "SELECT * " \
                               "FROM kr_stock_weekly " \
                               "WHERE DATE ='{}' " \
                               "AND kr_stock_code='{}';".format(recently_date,code)
                    cursor.execute(data_sql)
                    data = cursor.fetchall()
        except Exception as e:
            print('->', e)

        finally:
            if connection:
                connection.close()
                # print(value)
        return data[0]
