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
                sql = "SELECT * FROM main_page_data WHERE date_time='{}';".format(date)
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

