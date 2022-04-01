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

