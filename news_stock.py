import pandas as pd
import numpy as np
# from pykrx import stock

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

print(df.shape)
df.to_excel('C:/ESG/'+file_name+'_정리.xlsx', index=None)
