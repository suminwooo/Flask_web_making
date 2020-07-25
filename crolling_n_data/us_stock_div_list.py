# 미국 배당주 리스트 뽑기

def dividend_list():
    f = open('dividend_list.txt','r')
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
    for i in ['ADR','MLP','GBLIZ','ETF','REIT','Kroger','Target','BPR','Xerox','BP PLC','AT&T','RNST','HFWA']:
        total_list.remove(i)
    return total_list