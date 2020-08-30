# 현재 상장되어있는 코스피, 코스닥 목록 출력
# code_data_update_add 와 연결

import FinanceDataReader as fdr

class code_information():

    def code_data(self):

        df_krx = fdr.StockListing('KRX')
        kospi_kosdaq = df_krx[(df_krx['Market'] == 'KOSDAQ') | (df_krx['Market'] == 'KOSPI')].dropna()
        kospi_kosdaq = kospi_kosdaq[
            ['Symbol', 'Market', 'Name', 'Sector', 'Industry', 'ListingDate', 'SettleMonth', 'HomePage', 'Region']]
        kospi_kosdaq.columns = ['kr_stock_code', 'market', 'kr_stock_name', 'sector', 'industry', 'listingdate',
                                'settledate', 'homepage', 'region']

        return kospi_kosdaq

