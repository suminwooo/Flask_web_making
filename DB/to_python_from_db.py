import pymysql.cursors

# 한국 전체 리스트 보내기
connection = pymysql.connect(host='localhost', user='root', password='0000', charset='utf8', db='web_db')
cur = connection.cursor()
sql = "SELECT kr_stock_code,kr_stock_name FROM kr_stock_list;"
cur.execute(sql)
kr_stock_list = cur.fetchall()
connection.close()
print(kr_stock_list)