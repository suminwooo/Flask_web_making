import pymysql.cursors


class web_engine:
    def search(self, search):

        word = search

        # 한국 전체 리스트 보내기
        connection = pymysql.connect(host='localhost', user='root', password='0000', charset='utf8', db='web_db')
        cur = connection.cursor()

        sql = "(" \
              "SELECT kr_stock_code, kr_stock_name " \
              "FROM kr_stock_list " \
              "WHERE kr_stock_code ='{}' " \
              "OR kr_stock_name ='{}' ) " \
              "UNION ALL ( " \
              "SELECT us_stock_code, us_stock_name " \
              "FROM us_stock_list " \
              "WHERE us_stock_code ='{}'" \
              "OR us_stock_name ='{}' );".format(word, word, word, word)

        cur.execute(sql)
        db_data = cur.fetchall()
        connection.close()
        return db_data[0]

