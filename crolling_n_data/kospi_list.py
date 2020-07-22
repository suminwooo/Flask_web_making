import pandas as pd
data = pd.read_csv('kospi_code.csv')
print(data[data.columns[1:]])