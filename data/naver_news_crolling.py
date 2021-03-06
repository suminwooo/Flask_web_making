# 개별 주식을 검색하였을때 보여지는 네이버 뉴스 부분 크롤링
# 추후 더보기로 네이버 뉴스와 연결 시키기

import requests
from bs4 import BeautifulSoup


class naver_news:

    def news_information(self,code):
        URL = "https://finance.naver.com/item/main.nhn?code={}"
        index = requests.get(URL.format(code))
        html = index.text
        soup = BeautifulSoup(html, 'html.parser')
        news_section = soup.find('div', class_='sub_section news_section')

        link_list = []
        news_list = []
        for i in news_section.find_all('span', class_='txt'):
            link = 'https://finance.naver.com/' + i.find('a')['href']
            link_list.append(link)
            news_list.append(i.text.split('\n')[1])

        news_dic ={}
        for i in range(len(link_list)):
            news_dic[link_list[i]] = news_list[i]
        return news_dic
