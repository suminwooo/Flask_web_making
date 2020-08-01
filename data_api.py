import pandas as pd
class test:
    def test(self):
        data= pd.read_csv('crolling_n_data/raw_data/kospi_code.csv')
        data = data[data.columns[1:]]

        test_data_list = []
        for i in range(len(data)):
            test_data_list.append(list(data.loc[i]))

        key_list = []
        value_list = []
        for i in test_data_list:
            key_list.append('{}'.format(i[0]))
            value_list.append(['{},{},{}'.format(str(i[1]), str(i[2]), str(i[3]))])

        new_dic = {}
        for i, j in zip(key_list, value_list):
            new_dic[i] = j

        return new_dic

print(test().test())