# import requests
# from bs4 import BeautifulSoup
#
URL = "https://www.dividend.com/dividend-stocks/high-dividend-yield-stocks/#tm=3-high-yield-stocks&r=Webpage%231281&f_35=true&f_9_min=2&f_9_max=100&only=meta%2Cdata%2Cthead&"\
      +"page=1"+"&sort_by=latest_yield&sort_direction=desc"
#
# index1 = requests.get(URL)
# html = index1.text
# soup = BeautifulSoup(html, 'html.parser')
# test = soup.find('section', class_='tm').find('tbody').find_all('td')
#
# print([test[i].text for i in range(1,181,9)])
