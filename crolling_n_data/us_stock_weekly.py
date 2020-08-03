from etc.date import date_num
import yfinance as yf
import pandas as pd

data = pd.read_csv('C:/Users/wsm26/Desktop/Flask_web_making/crolling_n_data/raw_data/us_stock_list.csv')
stock_name = list(data['us_stock_code'])


class us_stock_weekly:
    def weekly_data(self):

        final_list = []
        for code in stock_name[:2]:
            test = yf.Ticker(code)
            value_list= []
            value_list.append(code)
            value_list.append(date_num())
            for i in ['regularMarketOpen','twoHundredDayAverage','payoutRatio','regularMarketDayHigh','averageDailyVolume10Day','totalAssets',
                          'regularMarketPreviousClose','trailingAnnualDividendRate','averageVolume10days','dividendRate','exDividendDate','beta',
                          'regularMarketDayLow','regularMarketVolume','averageVolume','fiftyTwoWeekHigh','fiveYearAvgDividendYield','fiftyTwoWeekLow',
                          'bid','dividendYield','lastDividendValue','enterpriseValue','threeYearAverageReturn','fiveYearAverageReturn',
                          'regularMarketPrice']:
                try:
                    value_list.append(test.info[i])
                except:
                    value_list.append('NO_DATA')
            final_list.append(value_list)

        data = pd.DataFrame(columns = ['code','date','regularMarketOpen','twoHundredDayAverage','payoutRatio','regularMarketDayHigh','averageDailyVolume10Day','totalAssets',
                          'regularMarketPreviousClose','trailingAnnualDividendRate','averageVolume10days','dividendRate','exDividendDate','beta',
                          'regularMarketDayLow','regularMarketVolume','averageVolume','fiftyTwoWeekHigh','fiveYearAvgDividendYield','fiftyTwoWeekLow',
                          'bid','dividendYield','lastDividendValue','enterpriseValue','threeYearAverageReturn','fiveYearAverageReturn',
                          'regularMarketPrice'])
        for i in range(len(final_list)):
            if len(final_list[i]) == 27:
                data.loc[i] = final_list[i]
            else:
                new_value = final_list[i]+['NO_DATA','NO_DATA','NO_DATA','NO_DATA','NO_DATA','NO_DATA','NO_DATA','NO_DATA','NO_DATA','NO_DATA','NO_DATA','NO_DATA','NO_DATA','NO_DATA','NO_DATA','NO_DATA','NO_DATA','NO_DATA','NO_DATA','NO_DATA','NO_DATA','NO_DATA','NO_DATA','NO_DATA']
                data.loc[i] = new_value

        return data
