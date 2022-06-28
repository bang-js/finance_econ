from operator import index
import pandas as pd
import numpy as np
from pykrx import stock
import datetime 

# 이름-종목코드 엑셀파일 불러오기
df_kospi = pd.read_csv('C:/ESG/data/KOSPI100.csv')
# 종목코드 앞에 0으로 padding
df_kospi['종목코드'] = df_kospi['종목코드'].astype(str).str.zfill(6)

# dataset 호출
file_name = 'DF_최종_1'
df = pd.read_excel('C:/ESG/'+file_name+'.xlsx', engine='openpyxl')
# 제목 없으면 삭제
df['제목'].replace('', np.nan, inplace=True) # 비어있는셀->np.nan
df.dropna(subset=['제목'], inplace=True)
# 제목 중복 시 삭제
df.drop_duplicates(subset=['제목'],inplace=True)
print(df.shape)
# 날짜, 기업, 키워드 중복 시 count 후 제거
dups = []
for j in range(df.shape[0]-1) :
    dup = 0
    while (df.iloc[j]['일자'] == df.iloc[j+1+dup]['일자']) & (df.iloc[j]['기업'] == df.iloc[j+1+dup]['기업']) & \
            (df.iloc[j]['ESG'] == df.iloc[j+1+dup]['ESG']) : 
            dup += 1
    dups.append(dup)
dups.append(0)
df['중복 횟수'] = dups
df.drop_duplicates(subset=['일자','기업','ESG'], keep='first', inplace=True)

# ESG 키워드가 있는 row만 살리기
df['ESG'].replace('', np.nan, inplace=True)
df.dropna(subset=['ESG'], inplace=True)
df.reset_index(drop=True, inplace=True) # row index 초기화 (concat상 중요!)
print(df.head())
print(df.shape)
# df.to_excel('C:/ESG/'+file_name+'_정리.xlsx', index=None)

# ESG 키워드별 뉴스 수
print(df['ESG'].value_counts())

## 해당 종목의 해당 날짜 -5~+10일 간의 daily return을 df에 저장
## 날짜 계산 시 장이 안 열리는 날도 고려해야 함
# # df에 빈 컬럼 생성
# column_names = ['ror_{}'.format(i) for i in range(0,16)] 
# for i in range(16):
#     df['ror_{}'.format(i)] = np.NaN

ticker_dict = dict(zip(df_kospi['종목명'].to_list(),df_kospi['종목코드'].to_list())) # 종목명-종목코드 dict화
# 0~+15일
ror = []
for i in range(30) : #df.shape[0]
    ticker = ticker_dict.get(df.iloc[i]['기업']) # 해당 기업의 종목코드 찾기
    date = str(int(df.iloc[i]['일자']))
    date0 = datetime.date(int(date[:4]),int(date[4:6]),int(date[6:8]))
    date1 = date0 - datetime.timedelta(days=7)
    date2 = date0 + datetime.timedelta(days=30)
    date_dash = date[:4]+'-'+date[4:6]+'-'+date[6:8]
    
    df_stock_temp = stock.get_market_ohlcv(date1.strftime('%Y%m%d'), date2.strftime('%Y%m%d'),ticker,'d')
    df_stock_temp = df_stock_temp.reset_index() # inplace = True 가 default
    if df_stock_temp.shape[0] > 0 :
        df_stock_temp['날짜'] = pd.to_datetime(df_stock_temp['날짜'])
        df_stock_temp['ror'] = df_stock_temp['종가']/df_stock_temp['종가'].shift(1) - 1 # 수익률 생성
        df_stock_temp = df_stock_temp[df_stock_temp['날짜'] >= date_dash]
        ror_temp = list(np.array(df_stock_temp['ror'].tolist()))
        ror_temp = ror_temp[:16]
    else : # 비어있다면
        ror_temp = [0 for i in range(16)]
    ror.append(ror_temp) # ror이라는 이중list
ror = np.array(ror) # list를 np로 바꾸기
column_names = ['ror_{}'.format(i) for i in range(0,16)] 
df_ror = pd.DataFrame(ror, columns=column_names) 
df = pd.concat([df, df_ror], axis=1)  # 그대로 axis=1 방향으로 붙이기

# -5~0일
ror = []
for i in range(30) : #df.shape[0]
    ticker = ticker_dict.get(df.iloc[i]['기업']) # 해당 기업의 종목코드 찾기
    date = str(int(df.iloc[i]['일자']))
    date0 = datetime.date(int(date[:4]),int(date[4:6]),int(date[6:8]))
    date1 = date0 - datetime.timedelta(days=15) # 넉넉히 가져오기 
    date_dash = date[:4]+'-'+date[4:6]+'-'+date[6:8]

    df_stock_temp = stock.get_market_ohlcv(date1.strftime('%Y%m%d'), date, ticker,'d')
    df_stock_temp = df_stock_temp.reset_index()
    if df_stock_temp.shape[0] > 0 :
        df_stock_temp['날짜'] = pd.to_datetime(df_stock_temp['날짜'])
        df_stock_temp['ror'] = df_stock_temp['종가']/df_stock_temp['종가'].shift(1) - 1 # 수익률 생성
        ror_temp = list(np.array(df_stock_temp['ror'].tolist()))
        ror_temp = ror_temp[-5:0] # 5개만큼 추리기, 이때 t=0는 제외해야 중복안됨
    else : # 비어있다면
        ror_temp = [0 for i in range(5)]
    ror.append(ror_temp) # ror이라는 이중list
ror = np.array(ror) # list를 np로 바꾸기
column_names = ['ror_{}'.format(i) for i in range(-5,0)]
df_ror = pd.DataFrame(ror, columns=column_names) 
df = pd.concat([df, df_ror], axis=1)

print(df.shape)
print(df.head())
df.to_excel('C:/ESG/'+file_name+'_정리.xlsx', index=None)
