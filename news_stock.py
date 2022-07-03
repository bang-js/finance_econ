import pandas as pd
import numpy as np
from pykrx import stock
import datetime 

# 이름-종목코드 엑셀파일 불러오기
df_kospi = pd.read_csv('C:/ESG/data/KOSPI100.csv')
# 종목코드 앞에 0으로 padding
df_kospi['종목코드'] = df_kospi['종목코드'].astype(str).str.zfill(6)

################
# dataset 호출
file_name = 'DF_최종_2' 
################
# df = pd.read_excel('C:/ESG/'+file_name+'.xlsx', engine='openpyxl')

# # 제목 없으면 삭제
# df['제목'].replace('', np.nan, inplace=True) # 비어있는셀->np.nan
# df.dropna(subset=['제목'], inplace=True)
# # 제목 중복 시 삭제
# df.drop_duplicates(subset=['제목'],inplace=True)
# # ESG 키워드가 있는 row만 살리기
# df['ESG'].replace('', np.nan, inplace=True)
# df.dropna(subset=['ESG'], inplace=True)
# print(df.shape)

# # 날짜, 기업, 키워드 중복 시 count 후 제거
# dups = []
# for j in range(df.shape[0]-2) :
#     dup = 0
#     while (df.iloc[j]['일자'] == df.iloc[j+1+dup]['일자']) & (df.iloc[j]['기업'] == df.iloc[j+1+dup]['기업']) & \
#             (df.iloc[j]['ESG'] == df.iloc[j+1+dup]['ESG']) : 
#             dup += 1
#     dups.append(dup)
# dups.extend([0,0])
# df['중복 횟수'] = dups
# df.drop_duplicates(subset=['일자','기업','ESG'], keep='first', inplace=True)

# # GS, LG, SK, 롯데지주 제외
# except_list = ['GS', 'LG', 'SK', '롯데지주']
# for ex in except_list :
#     is_ex = df['기업']==ex
#     df = df[~is_ex]

# df.reset_index(drop=True, inplace=True) # row index 초기화 (concat상 중요!)
# print(df.shape)
# df.to_excel('C:/ESG/'+file_name+'_정리.xlsx', index=None)

# # ESG 키워드별 뉴스 수
# print(df['ESG'].value_counts())

# ##############
# ## 해당 종목의 해당 날짜 -5~+10일 간의 daily return을 df에 저장
# ## 날짜 계산 시 장이 안 열리는 날도 고려해야 함
# ##############

# df = pd.read_excel('C:/ESG/'+file_name+'_정리.xlsx', engine='openpyxl')

# ticker_dict = dict(zip(df_kospi['종목명'].to_list(),df_kospi['종목코드'].to_list())) # 종목명-종목코드 dict화
# # 0~+15일
# ror = []
# for i in range(df.shape[0]) : #df.shape[0]
#     ticker = ticker_dict.get(df.iloc[i]['기업']) # 해당 기업의 종목코드 찾기
#     date = str(int(df.iloc[i]['일자']))
#     date0 = datetime.date(int(date[:4]),int(date[4:6]),int(date[6:8]))
#     date1 = date0 - datetime.timedelta(days=7)
#     date2 = date0 + datetime.timedelta(days=60) # 무러 2달이나 넉넉하게 잡음....
#     date_dash = date[:4]+'-'+date[4:6]+'-'+date[6:8]
    
#     df_stock_temp = stock.get_market_ohlcv(date1.strftime('%Y%m%d'), date2.strftime('%Y%m%d'),ticker,'d')
#     df_stock_temp = df_stock_temp.reset_index() # inplace = True 가 default
#     if df_stock_temp.shape[0] > 0 :
#         df_stock_temp['날짜'] = pd.to_datetime(df_stock_temp['날짜'])
#         df_stock_temp['ror'] = df_stock_temp['종가']/df_stock_temp['종가'].shift(1) - 1 # 수익률 생성
#         df_stock_temp = df_stock_temp[df_stock_temp['날짜'] >= date_dash] # 날짜 조정 : 보도일자 이후만 살리기
#         ror_temp = list(np.array(df_stock_temp['ror'].tolist()))
#         if len(ror_temp) >= 16 :
#             ror_temp = ror_temp[:16]
#         else : # 넉넉히 잡았는데도 개수가 부족하면 NaN 처리
#             ror_temp = [np.NaN for j in range(16)]
#     else : # 비어있다면
#         ror_temp = [np.NaN for j in range(16)]
    
#     # kospi 자료 추가 (ticker 1001)
#     df_kospi_temp = stock.get_index_ohlcv(date1.strftime('%Y%m%d'), date2.strftime('%Y%m%d'), '1001' ,'d')
#     df_kospi_temp = df_kospi_temp.reset_index()
#     if df_kospi_temp.shape[0] > 0 :
#         df_kospi_temp['날짜'] = pd.to_datetime(df_kospi_temp['날짜'])
#         df_kospi_temp['ror'] = df_kospi_temp['종가']/df_kospi_temp['종가'].shift(1) - 1 # 수익률 생성
#         df_kospi_temp = df_kospi_temp[df_kospi_temp['날짜'] >= date_dash] # 날짜 조정 : 보도일자 이후만 살리기
#         ror_kospi_temp = list(np.array(df_kospi_temp['ror'].tolist()))
#         if len(ror_kospi_temp) >= 16 :
#             ror_kospi_temp = ror_kospi_temp[:16]
#         else : # 넉넉히 잡았는데도 개수가 부족하면 NaN 처리
#             ror_kospi_temp = [np.NaN for j in range(16)]
#     else : # 비어있다면
#         ror_kospi_temp = [np.NaN for j in range(16)]
    
#     # ror_temp와 ror_kospi_temp 연결
#     ror_temp.extend(ror_kospi_temp)

#     # ror이라는 이중list
#     ror.append(ror_temp) 

#     if i%100 == 0:
#         print(i)

# for k in range(len(ror)) : # 16+16이 아니면 nan으로 변환
#     if len(ror[k]) < 32 :
#         ror[k] = [np.NaN for j in range(32)]
#         print(k)

# ror = np.array(ror) # list를 np로 바꾸기
# column_names = ['ror_{}'.format(i) for i in range(0,16)] 
# column_names_k = ['kospi_{}'.format(i) for i in range(0,16)] 
# column_names.extend(column_names_k)
# df_ror = pd.DataFrame(ror, columns=column_names) 
# df = pd.concat([df, df_ror], axis=1)  # 그대로 axis=1 방향으로 붙이기

# # ValueError: Shape of passed values is (4095, 1), indices imply (4095, 16)
# # => 이 Error는 지금 16개 다 못채워서 나오는 error

# #######
# # -5~0일
# ror = []
# ror_temp = [np.NaN for i in range(5)] # ror_temp 초기화
# for i in range(df.shape[0]) : 
#     ticker = ticker_dict.get(df.iloc[i]['기업']) # 해당 기업의 종목코드 찾기
#     date = str(int(df.iloc[i]['일자']))
#     date0 = datetime.date(int(date[:4]),int(date[4:6]),int(date[6:8]))
#     date1 = date0 - datetime.timedelta(days=20) # 넉넉히 가져오기 
#     date_dash = date[:4]+'-'+date[4:6]+'-'+date[6:8]

#     df_stock_temp = stock.get_market_ohlcv(date1.strftime('%Y%m%d'), date0.strftime('%Y%m%d'), ticker,'d')
#     df_stock_temp = df_stock_temp.reset_index()
#     if df_stock_temp.shape[0] > 0 :
#         df_stock_temp['날짜'] = pd.to_datetime(df_stock_temp['날짜'])
#         df_stock_temp['ror'] = df_stock_temp['종가']/df_stock_temp['종가'].shift(1) - 1 # 수익률 생성
#         ror_temp = list(np.array(df_stock_temp['ror'].tolist()))
#         if len(ror_temp) >= 5 :
#             ror_temp = ror_temp[-6:-1] # 5개만큼 추리기, 이때 t=0는 제외해야 중복안됨
#         else : # 넉넉히 잡았는데도 개수가 부족하면 NaN 처리
#             ror_temp = [np.NaN for j in range(5)]
#     else : # 비어있다면
#         ror_temp = [np.NaN for j in range(5)]

#     # kospi 자료 추가 (ticker 1001)
#     df_kospi_temp = stock.get_index_ohlcv(date1.strftime('%Y%m%d'), date0.strftime('%Y%m%d'), '1001' ,'d')
#     df_kospi_temp = df_kospi_temp.reset_index()
#     if df_kospi_temp.shape[0] > 0 :
#         df_kospi_temp['날짜'] = pd.to_datetime(df_kospi_temp['날짜'])
#         df_kospi_temp['ror'] = df_kospi_temp['종가']/df_kospi_temp['종가'].shift(1) - 1 # 수익률 생성
#         ror_kospi_temp = list(np.array(df_kospi_temp['ror'].tolist()))
#         if len(ror_kospi_temp) >= 5 :
#             ror_kospi_temp = ror_kospi_temp[-6:-1]    
#         else : # 넉넉히 잡았는데도 개수가 부족하면 NaN 처리
#             ror_kospi_temp = [np.NaN for j in range(5)]
#     else : # 비어있다면
#         ror_kospi_temp = [np.NaN for j in range(5)]
    
#     ror_temp.extend(ror_kospi_temp)

#     # ror이라는 이중list
#     ror.append(ror_temp) 

#     if i%100 == 0:
#         print(i)    

# for k in range(len(ror)) :
#     if len(ror[k]) < 10 :
#         ror[k] = [np.NaN for j in range(10)]
#         print(k)

# ror = np.array(ror) # list를 np로 바꾸기
# column_names = ['ror_{}'.format(i) for i in range(-5,0)]
# column_names_k = ['kospi_{}'.format(i) for i in range(-5,0)] 
# column_names.extend(column_names_k)
# df_ror = pd.DataFrame(ror, columns=column_names) 
# df = pd.concat([df, df_ror], axis=1)

# print(df.shape)
# print(df.head())
# print(df['ESG'].value_counts())

# df.to_excel('C:/ESG/'+file_name+'_정리.xlsx', index=None)



####################
# AR, CAR 계산
# CAPM을 믿을 수 없으니 3종으로
# r_i
# AR1 = r_i - r_m 
# AR2 = r_i - (a+b*r_m) (CAPM)
####################

# df = pd.read_excel('C:/ESG/'+file_name+'_정리.xlsx', engine='openpyxl')

# # ror_0가 비어있으면 삭제
# df.dropna(subset=['ror_0'], inplace=True)
# # 5일 이상 거래정지 : ror에서 0이 5개 이상이면 삭제
# zeros = []
# for i in range(df.shape[0]) :
#     zero = 0
#     for j in range(16) :
#         if df.iloc[i]['ror_{}'.format(j)] == 0 :
#             zero += 1
#     zeros.append(zero)
# df['ror=0'] = zeros
# index_zero = df[df['ror=0'] >= 5].index
# df.drop(index_zero, inplace=True)
# df.drop(['ror=0'], axis=1, inplace=True)

# #######
# # AR1
# for i in range(-5,16) :
#     df['AR_{}'.format(i)] = df['ror_{}'.format(i)] - df['kospi_{}'.format(i)]

# # CAR1_1 : -5~+5 # CAR1_2 : -5~+10 # CAR1_3 : -5~+15
# # CAR1_4 : 0~+5 # CAR1_5 : 0~+10 # CAR1_6 : 0~+15
# # CAR1_7 : -1~+1

# def car(start, end) :
#     # 59: AR_-5, ..., 64: AR_0, ..., 79: AR_15
#     df_car = df.iloc[:, start+64:end+64+1]
#     df_car['car'] = df_car.sum(axis=1)
#     return df_car['car'].to_list()

starts = [-5,0]
ends = [5,10,15]
s_e = []
for s in starts:
    for e in ends :
        s_e.append((s,e))
s_e.append((-1,1))

# cars = []
# for s,e in s_e :
#     df['CAR_{}_{}'.format(s,e)] = car(s,e)

# df.to_excel('C:/ESG/'+file_name+'_AR.xlsx', index=None)
#######
# AR2 : 300일치 데이터




#################
# 키워드별 분류
#################

# df = pd.read_excel('C:/ESG/'+file_name+'_AR.xlsx', engine='openpyxl')

### 중복5 : 
df = pd.read_excel('C:/ESG/'+file_name+'_AR_15일중복.xlsx', engine='openpyxl')

ESGs = df['ESG'].unique().tolist() # ESG 키워드들을 list로

for i, j in s_e :
    column_names = ['CAR_{}_{}'.format(i,j)]
df_keyword = pd.DataFrame(columns=column_names)

for s, e in s_e :
    ESGs_CAR = []
    for esg in ESGs :  
        ESGs_keyword = [] # keyword별 CAR_s_e 값
        for i,row in df.iterrows() :
            if row['ESG'] == esg :
                ESGs_keyword.append(row['CAR_{}_{}'.format(s,e)])
        ESGs_keyword_avg = sum(ESGs_keyword)/len(ESGs_keyword)
        ESGs_CAR.append(ESGs_keyword_avg)         
    print(ESGs_CAR)
    df_keyword['CAR_{}_{}'.format(s,e)] = ESGs_CAR


df_keyword.insert(0, 'ESG_keyword', ESGs)

# df_keyword.to_excel('C:/ESG/'+file_name+'_CAR_keywords.xlsx', index=None)

### 중복5 : 
df_keyword.to_excel('C:/ESG/'+file_name+'_AR_15일중복_CAR_keywords.xlsx', index=None)




