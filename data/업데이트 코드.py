from data.code_data.code_data_update_add import code_add_update
from data.main_data_daily_crolling import main_page_data_crolling
from data.forigner_institution import foreinger_institurion
from data.main_page_weekly_crolling import kr_stock_weekly

class data_update:

    def daily_update(self):

        print('코드 체크 및 데일리 업데이트 시작')
        code_add_update().code_list_update()
        print('완료')
        print('데일리 메인 데이터 업데이트 시작')
        main_page_data_crolling().input_main_page_data()
        print('완료')
        print('데일리 외국인 & 기관 부분 업데이트 시작')
        foreinger_institurion().daily_data_to_mysql()
        print('완료')

        return '업데이트 완료'

    def weekly_update(self):
        print('daily update 시작')
        data_update().daily_update()
        print('daily update 끝 & weekly update 시작')
        kr_stock_weekly().weekly_data_to_db()
        print('weekly update 끝')

        return '업데이트 완료'

data_update().weekly_update()