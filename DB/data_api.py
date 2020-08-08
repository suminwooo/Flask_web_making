import pymysql

class stock_list_api:
    def api(self):

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
                    sql = "SELECT kr_stock_list.kr_stock_code, kr_stock_list.kr_ind_code, " \
                          "kr_stock_list.kr_stock_name, kr_ind_list.kr_ind_name " \
                          "FROM kr_stock_list " \
                          "JOIN kr_ind_list " \
                          "ON kr_stock_list.kr_ind_code = kr_ind_list.kr_ind_code;"
                    cursor.execute(sql)
                    data = cursor.fetchall()
                    code_dic ={}
                    for i in range(len(data)):
                        code_dic['{}'.format(data[i]['kr_stock_code'])]=data[i]
        except Exception as e:
            print('->', e)

        finally:
            if connection:
                connection.close()
                # print(value)
        return code_dic
