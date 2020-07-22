import pandas as pd

f = open('dividend_list.txt','r')
line_num = 1
line = f.readline()

div_code = []

while line:
    code = line.strip()
    if (len(code) <= 6) & (len(code) >= 2) :
        div_code.append(code)
        line = f.readline()
    else:
        line = f.readline()
f.close()

total_list = list(set(div_code))
for i in ['ADR','MLP','GBLIZ','ETF','REIT']:
    total_list.remove(i)
print(total_list)