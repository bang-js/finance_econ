###
# 1% rule 가설
# ror의 분포에서 하위1% 수익률(Value at Risk)에 수익률이 도달할 경우 이후에 강한 하락세가 온다는 가설
###

# import matplotlib
import pandas as pd
# import matplotlib.pyplot as plt
# %matplotlib inline

# ETF 선택
etf_ticker = 'TQQQ'

# csv 파일 불러오기
df = pd.read_csv('C:/etf/{}.csv'.format(etf_ticker))

# 변동률 계산 및 하위 1% 충격값 찾기
df['ror'] = df['close']/df['close'].shift(1) - 1
print(df['ror'].describe(percentiles=[0.01,0.1,0.5,0.9])) # percentile 조정
# TQQQ의 경우 -10%가 하위1%의 경계값

# 변동률의 히스토그램 그리기
# plt.hist(df['ror'], bins=100)
# plt.xlabel('ror')
# plt.ylabel('frequency')
# print(plt.show())

# 1% 충격 발생 시 5일, 10일, 20일, 30일, 45일, 60일, 90일, 120일, 180일 뒤 어떤 total change를 보였는지
threshold = -0.1 ### -x% 기준 ###  

shock_date = []
shock_day_open = []
shock_day_close = []
shock_day_5 = []
shock_day_10 = []
shock_day_20 = []
shock_day_30 = []
shock_day_45 = []
shock_day_60 = []
shock_day_90 = []
shock_day_120 = []
day_no_list = [5,10,20,30,45,60,90,120]     # len = 8
shock_day_list = [shock_day_5, shock_day_10, shock_day_20, shock_day_30, shock_day_45, shock_day_60, shock_day_90, shock_day_120]

for idx in range(2,df.shape[0]):
    if df.iloc[idx][8] <= threshold :                    # 8:ror
        shock_date.append(df.iloc[idx][0])          # 0:date
        shock_day_open.append(df.iloc[idx][1])      # 1:open
        shock_day_close.append(df.iloc[idx][4])     # 4:close
        for j in range(8) :                         # 8 : length
            if idx+day_no_list[j] < df.shape[0]  :   # df 밖으로 나가는 경우 제외 (오류 방지)
                add = (df.iloc[idx+day_no_list[j]][4]/df.iloc[idx][4])-1   # 종가 대비 변화율
                shock_day_list[j].append(add)
            else :
                shock_day_list[j].append(math.nan)

ROR = pd.DataFrame([ x for x in zip(
    shock_date, shock_day_open, shock_day_close, shock_day_5, shock_day_10, shock_day_20, \
        shock_day_30, shock_day_45, shock_day_60, shock_day_90, shock_day_120
)])
ROR.rename(columns={0:'shock_date', 1:'shock_day_open', 2:'shock_day_close', 3:'shock_day_5', 4:'shock_day_10', 5:'shock_day_20', \
        6:'shock_day_30', 7:'shock_day_45', 8:'shock_day_60', 9:'shock_day_90', 10:'shock_day_120'}
, inplace=True)

filename = '{}_{}_1percent_rule.csv'.format(etf_ticker,threshold)
file = open(filename, "w", encoding="utf-8-sig")  
ROR.to_csv('C:/etf/'+filename, index=None)

# 투자 전략 
# 매수점 : (이전 매도 이후) MA60 < MA5 시
# 매도점(손절이자 익절, unique) : 전날 VaR 발생 시
# 재매수점(큰 폭으로 하락하지 않고 다시 올라온 경우) : 2주 뒤(10일)에도 종가가 MA60 위에 올라가있으면 매수 vs 매도가 < 현재가 면 매수

# 1% 뒤의 약 반 년 간의 시계열 데이터들을 모아 특정 함수(A-exp(-at) 등)에 대해 regression해서 유의성 검토하기
