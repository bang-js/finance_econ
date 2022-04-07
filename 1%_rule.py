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

# 1% 충격 발생 시 5일, 10일, 20일, 45일, 60일, 90일, 120일, 180일 뒤 어떤 total change를 보였는지  
# output : 1% 충격 발생 시점 - 5일, 10일, 20일, 45일, 60일, 90일, 120일, 180일별 total change
# total change = (N일 뒤 가격)/(1% 충격을 받은 날의 종가) - 1

# 1% 뒤의 약 반 년 간의 시계열 데이터들을 모아 특정 함수(A-exp(-at) 등)에 대해 regression해서 유의성 검토하기
