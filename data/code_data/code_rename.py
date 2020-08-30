import pandas as pd

class code_rename():
    def code_name(self):
        data = pd.read_csv('kospi_code.csv')
        code_list = []
        for i in data['code']:
            code = str(i)
            if len(code) == 2:
                code = '0000' + code
                code_list.append(code)
            elif len(code) == 3:
                code = '000' + code
                code_list.append(code)
            elif len(code) == 4:
                code = '00' + code
                code_list.append(code)
            elif len(code) == 5:
                code = '0' + code
                code_list.append(code)
            else:
                code_list.append(code)

        return code_list