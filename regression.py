import pandas as pd
import numpy as np

#ticker찾기
df_kospi = pd.read_csv('C:/ESG/data/KOSPI.csv',  encoding='cp949')
df_kospi['종목코드'] = df_kospi['종목코드'].astype(str).str.zfill(6) 
name_ticker = dict(zip(df_kospi['종목명'].to_list(),df_kospi['종목코드'].to_list())) # {종목명:tikcer}
ticker_name = dict(zip(df_kospi['종목코드'].to_list(),df_kospi['종목명'].to_list())) # {ticker:종목명}


df_fin = pd.read_excel('C:/ESG/data/kospi_fin_data.xlsx', header=[0,1], engine='openpyxl') 
df_fin.set_index(('종목코드','종목코드'), inplace = True) # ticker가 int로 바뀜
# multiindex는 튜플로 호출 df[('a','b')]

# 변수명 list 뽑아내기
# a = df_fin.columns.to_list()
# b = [i for i,j in a]
# b = list(set(b))
vars = ['KIS 신용평점','부채비율','유동성','MTB','mROA','LNmkt'] #,'영업이익증가율'
yrs = [i for i in range(2012,2022)]

# 데이터 정리
df_news = pd.read_excel('C:/ESG/DF_최종_5_AR_10일중복_anounce_reg.xlsx', engine='openpyxl') 
df_news['일자'] = pd.to_datetime(df_news['일자'])
df_news['연도'] = df_news['일자'].dt.year
stocks_name = df_news['기업'].value_counts().index.to_list() # 기업이름으로 되어있는 list
df_news['종목코드'] = df_news['기업'].apply(lambda x : name_ticker.get(x)) # 기업이름 -> ticker col추가
# print(df_news)

s_e = [(0,1),(0,3),(0,5),(-1,1),(-1,3),(-1,5),(-5,5)]
CARs = []
for s,e in s_e :
    CARs.append('CAR_{}_{}'.format(s,e))



# #############3
# # 원하는 자료 df
# #############
# column =[]
# for i in CARs:
#     column.append(i)
# column.append('#news')
# for i in vars:
#     column.append(i)

# df_seed = []
# stocks_ticker = [name_ticker.get(i) for i in stocks_name]
# for stock in stocks_ticker:
#     stock_name = ticker_name.get(stock)
#     print(stock, stock_name) # ticker와 해당이름
#     df_news_temp = df_news[df_news['종목코드']==stock]
#     tot_yr=[]
#     yrs_here =[]
#     for yr in yrs:
#         single_yr = []
#         df_news_eq_yr = df_news_temp[df_news_temp['연도']==yr] # 같은 기업, 같은 연도의 CAR값들
#         if df_news_eq_yr.shape[0] == 0: # 빈 df이면 넘어가기
#             continue
#         else:
#             yrs_here.append(yr)
#             for c in CARs :
#                 avg = df_news_eq_yr[c].mean()
#                 single_yr.append(avg)
#             sum_news = df_news_eq_yr['중복 횟수(10일)'].sum()
#             single_yr.append(sum_news)
#             # ESG분류는 더이상 담지 못함
#             for var in vars:
#                 a = df_fin.loc[int(stock)][(var,yr)] # 해당기업의 해당연도의 특정변수값
#                 single_yr.append(a)
#         tot_yr.append(single_yr)
        
#     tot_yr = np.array(tot_yr)
#     stock_name = pd.DataFrame(tot_yr, index=yrs_here, columns=column)
#     df_seed.append(stock_name)

# df = pd.concat(df_seed, keys=stocks_name)
# df.dropna(inplace=True)
# df.to_excel('C:/ESG/DF_최종_5_reg_prepro.xlsx', engine='openpyxl')



#############
# reg2: 뉴스별
#############

column = df_news.columns.to_list()
for i in vars:
    column.append(i)

for var in vars:
    df_news[var] = np.nan
print(df_news)

for i in range(df_news.shape[0]):
    for var in vars:
        stock = df_news.iloc[i]['종목코드']
        yr = df_news.iloc[i]['연도']
        df_news.loc[i,var] = df_fin.loc[int(stock)][(var,yr)] 
    print(df_news.iloc[i][:])

df_news.dropna(inplace=True)
df_news.to_excel('C:/ESG/DF_최종_5_reg_prepro_2.xlsx', engine='openpyxl')