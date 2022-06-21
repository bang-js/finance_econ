from numpy import NaN
import pandas as pd
import numpy as np
# df = pd.read_excel('C:/Users/bes55/Downloads/상장법인목록 ({}).xls'.format(i), engine='openpyxl', header=None)

# KOSPI100 종목 리스트
df = pd.read_csv('C:/ESG/data/KOSPI100.csv')
stocks = df['종목명'].to_list() 

# 뉴스 excel 파일 C:\ESG\data\기업별 기사 논란
df = pd.read_excel('C:/ESG/data/기업별 기사 논란/BGF리테일.xlsx', engine='openpyxl')
for stock in stocks :
    if stock == 'BGF리테일' :
        continue 
    # elif stock == 'LG이노텍' :
    #     break
    else :  
        df_temp = pd.read_excel('C:/ESG/data/기업별 기사 논란/{}.xlsx'.format(stock), engine='openpyxl')
        df = pd.concat([df, df_temp],ignore_index=True)
    
print(df.shape)

###
# 키워드 찾아내기
###

# E : 환경파괴, 이물질, 오염, 검출, 방출, 독성, 폐기물, 폭발, 화학물질
# S : 안전, 프라이버시, 보안, 품질, 안정성, 광고, 허위광고, 과대광고, 고객
# 갑질, 
Ewords_lst = []
Swords_lst = []
Gwords_lst = []
df['E'] = ''
df['S'] = ''
df['G'] = ''
Ewords = '환경파괴, 이물질, 오염, 검출, 방출, 독성, 폐기물, 폭발, 화학물질'.split(', ') # 띄어쓰기!!!!
Swords = '안전, 프라이버시, 보안, 품질, 안정성, 허위광고, 고객'.split(', ')
Gwords = '분식회계, 주가조작, 주주권리'.split(', ')

def ESGwords(words):
    lst = []
    for idx, row in df.iterrows():
        act = 0
        keywords = df['특성추출(가중치순 상위 50개)'][idx].split(',')
        for keyword in keywords :
            if keyword in words :
                act = 1
        if act == 1 :
            lst.append(','.join(list(set(keywords) & set(words))))
        else : # act == 0
            lst.append('')
    return lst
df['E'] = ESGwords(Ewords)
df['S'] = ESGwords(Swords)
df['G'] = ESGwords(Gwords)

df.to_excel('C:/ESG/DF.xlsx', index=None)
