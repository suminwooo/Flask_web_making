import requests
from bs4 import BeautifulSoup
from crolling_n_data.dividend_list import dividend_list

error_code = []
for num,i in enumerate(dividend_list()):
    try:
        print(num,i)
        URL = "https://finance.yahoo.com/quote/{}?p={}&.tsrc=fin-srch"
        index = requests.get(URL.format(i,i))
        html = index.text
        soup = BeautifulSoup(html, 'html.parser')
        basic_inf = soup.find('div', id='quote-summary').find('table', class_='W(100%)').text
        print(basic_inf)
        detail_inf = soup.find('div', id='quote-summary').find('table', class_="W(100%) M(0) Bdcl(c)").text
        print(detail_inf)
    except :
        error_code.append(i)

#
# URL = "https://finance.yahoo.com/quote/Kroger?p=Kroger&.tsrc=fin-srch"
# index = requests.get(URL)
# html = index.text
# soup = BeautifulSoup(html, 'html.parser')
# basic_inf = soup.find('div', id='quote-summary').find('table', class_='W(100%)').text
# print(basic_inf)
# detail_inf = soup.find('div', id='quote-summary').find('table', class_="W(100%) M(0) Bdcl(c)").text
# print(detail_inf)