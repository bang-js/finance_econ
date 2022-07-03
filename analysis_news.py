import pandas as pd
import numpy as np
# df = pd.read_excel('C:/Users/bes55/Downloads/상장법인목록 ({}).xls'.format(i), engine='openpyxl', header=None)

# KOSPI100 종목 리스트
df = pd.read_csv('C:/ESG/data/KOSPI100.csv')
stocks = df['종목명'].to_list() 

# 뉴스 excel 파일 C:\ESG\data\기업별 기사 논란
df = pd.read_excel('C:/ESG/data/지배구조/BGF리테일.xlsx', engine='openpyxl')
df['기업'] = 'BGF리테일' # 기업명 입력 
for stock in stocks :
    if stock == 'BGF리테일' :
        continue 
        # elif stock == 'KT' : # 키워드에 KT&G가 있으면 기업명 바꾸기
        #     df_temp = pd.read_excel('C:/ESG/data/기업별 기사 논란/{}.xlsx'.format(stock), engine='openpyxl')
        #     for row in df_temp.iterrows() : 
        #         kw_lst = row['키워드'].split(',')
        #         if 'KT&G' in kw_lst :
        #             df_temp['기업'] = 'KT&G'
        #     df = pd.concat([df, df_temp],ignore_index=True)
    else :  
        df_temp = pd.read_excel('C:/ESG/data/지배구조/{}.xlsx'.format(stock), engine='openpyxl')
        df_temp['기업'] = stock # 기업명 입력
        df = pd.concat([df, df_temp],ignore_index=True)

# print(df.head(10))
# print(df.tail(10))
print(df.shape)

###
# 기업 이름이 중복되는 경우 ex. KT-KT&G
# 따로 상장된 계열사의 경우 ex. GS, GS리테일
###

LGs = ['LG', 'LG디스플레이', 'LG생활건강', 'LG에너지솔루션', 'LG유플러스', 'LG이노텍', 'LG전자', 'LG헬로비전', 'LG화학']
GSs = ['GS', 'GS건설', 'GS글로벌', 'GS리테일']
SKs = ['SK', 'SK가스', 'SK네트웍스', 'SK이노베이션', 'SKC', 'SK디스커버리', 'SK디앤디', 'SK렌터카', 'SK리츠', 'SK바이오사이언스', 'SK바이오팜', 'SK스퀘어', 'SK시그넷', 'SK아이이테크놀로지']

###
# 키워드 찾아내기
###

Ewords_lst = []
Swords_lst = []
Gwords_lst = []
df['E'] = ''
df['S'] = ''
df['G'] = ''

Ewords = '환경파괴, 미세먼지, 오염, 대기오염, 수질오염, 토지오염, 누출, 불법매립'.split(', ') # 띄어쓰기!!!!
Swords = '안전, 개인정보, 보안, 우롱, 사기, 제품, 품질, 리콜, 안정성, 독성, 유해성, 허위광고, 착취, 아동착취, 성폭력, 성차별, 독점, 불공정, 반경쟁, 과로, 근로환경, 산재, 산업안전, 파업, 노조, 분쟁, 노사, 폭로, 내부고발'.split(', ')
Gwords = '불공정거래, 시세조종, 주가조작, 미공개정보, 내부거래, 내부자거래, 부정거래, 보고의무, 공시의무, 리베이트, 물적분할, 유상증자, 분식회계, 낙하산, 부실경영, 성과급'.split(', ')
# Gwords = '부정채용, 채용비리, 로비, 리베이트, 뇌물, 횡령, 배임, 비자금, 비리, 분식회계, 주가조작, 주주'.split(', ')
# 공급망 : 갑질, 갑을, 일감, 협력사, 갈취, 내부거래
# 독점 vs (골목)상권 : 독점은 시장 점유율 문제 vs 상권은 타 부문으로의 확장과정에서 영세사업장의 이익을 빼앗는가의 문제(상생 이슈)
# 보수 : 임원, 이사진 성과급 문제
# 경영권분쟁 : 경영진 내부, 노동권 개입
# 안전 근로환경
# 가장 큰 문제는 부정 단어가 포함된 긍정 뉴스가 존재

# def ESGwords(words):
#     lst = []
    # for idx, row in df.iterrows():
    #     act = 0
        # keywords = df['키워드'][idx].split(',')
        # for keyword in keywords :
        #     if keyword in words :
        #         act = 1
        # if act == 1 :
        #     lst.append(','.join(list(set(keywords) & set(words))))
        # else : # act == 0
        #     lst.append('')

    # return lst

# 제목에 해당 단어가 있는지
def ESGwords(words):
    lst = []
    for i in range(df.shape[0]):
        words_lst = []
        title = df.iloc[i]['제목']
        for word in words :
            if word in title :
                words_lst.append(word)
        if len(words_lst) > 0:
            lst.append(','.join(list(set(words_lst) & set(words))))
        else :
            lst.append('')    
    return lst
    
# df['E'] = ESGwords(Ewords)
# df['S'] = ESGwords(Swords)
df['G'] = ESGwords(Gwords)

df.to_excel('C:/ESG/DF_지배구조.xlsx', index=None)
