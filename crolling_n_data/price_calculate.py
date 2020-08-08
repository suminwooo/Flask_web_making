import pymysql

class price_diff_calculate:
    def calculate(self):

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
                          "FROM kr_stock_daily " \
                          "group BY DATE " \
                          "order by date DESC " \
                          "LIMIT 2;"
                    cursor.execute(date_sql)
                    date = cursor.fetchall()

                    recently_data_raw = [i.strip() for i in str(date[0])[str(date[0]).find('(')+1:str(date[0]).find(')')].split(',')]
                    if len(recently_data_raw[1]) == 1:
                        recently_data_raw[1] = '0'+ recently_data_raw[1]
                    if len(recently_data_raw[2]) == 1:
                        recently_data_raw[2] = '0'+ recently_data_raw[2]
                    recently_data = recently_data_raw[0]+'-'+recently_data_raw[1]+'-'+recently_data_raw[2]

                    nonrecently_raw = [i.strip() for i in str(date[1])[str(date[1]).find('(')+1:str(date[1]).find(')')].split(',')]
                    if len(nonrecently_raw[1]) == 1:
                        nonrecently_raw[1] = '0' + nonrecently_raw[1]
                    if len(nonrecently_raw[2]) == 1:
                        nonrecently_raw[2] = '0' + nonrecently_raw[2]
                    nonrecently_date = nonrecently_raw[0] + '-' + nonrecently_raw[1] + '-' + nonrecently_raw[2]

                    recently_data_sql = "SELECT kr_stock_code, DATE, kr_stock_close, kr_stock_open, kr_stock_high, kr_stock_low, kr_stock_volume " \
                                        "FROM kr_stock_daily " \
                                        "WHERE DATE = '{}';".format(recently_data)
                    cursor.execute(recently_data_sql)
                    recently_data = cursor.fetchall()
                    recently_data = [j.values() for j in recently_data]


                    nonrecently_data_sql = "SELECT kr_stock_code, DATE, kr_stock_close, kr_stock_open, kr_stock_high, kr_stock_low, kr_stock_volume " \
                                        "FROM kr_stock_daily " \
                                        "WHERE DATE = '{}';".format(nonrecently_date)
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


print(price_diff_calculate().calculate()[660])