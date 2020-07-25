def dividend_list():
    f = open('data/dividend_list.txt','r')
    line = f.readline()

    div_code = []

    while line:
        code = line.strip()
        if (len(code) <= 6) & (len(code) >= 1) :
            div_code.append(code)
            line = f.readline()
        else:
            line = f.readline()
    f.close()

    total_list = list(set(div_code))
    return total_list

import requests
from bs4 import BeautifulSoup

error_code = []
for num,i in enumerate(dividend_list()[100:]):
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
        try:
            URL = "https://finance.yahoo.com/quote/{}?p={}&.tsrc=fin-srch"
            index = requests.get(URL.format(i,i))
            html = index.text
            soup = BeautifulSoup(html, 'html.parser')
            basic_inf = soup.find('div', id='quote-summary').find('table', class_='W(100%)').text
            print(basic_inf)
            detail_inf = soup.find('div', id='quote-summary').find('table', class_="W(100%) M(0) Bdcl(c)").text
            print(detail_inf)
        except:
            print('error')
            error_code.append(i)