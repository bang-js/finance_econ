import pandas as pd

#####
# database 받기
#####
# ETF 선택
etf_ticker = 'TQQQ'

# csv 파일 불러오기
df = pd.read_csv('C:/etf/{}.csv'.format(etf_ticker))

# 이동평균 계산
df['MA60'] = df['close'].rolling(60).mean()
df['MA20'] = df['close'].rolling(20).mean()
df['MA5'] = df['close'].rolling(5).mean()

# 변동률 계산
df['ror'] = df['close']/df['close'].shift(1) - 1
print(df['ror'].head(20))

#####
# nx1 series의 mean, var(std), skewedness, kurtosis 계산
#####

# describe : count, mean, std, min, 25%, median, 75%, max
print(df.describe())

# mean of ror
mean_df = df['ror'].mean()
print("mean: ",mean_df)

# var, std of ror
df['ror_sq'] = df['ror'].pow(2) 
var_df = df['ror_sq'].mean() - pow(mean_df,2) 
print("var: ", var_df)
print("std: ", pow(var_df, 0.5))

# skewedness = E(x-mean)^3/std^3
# 방법1 : E(x^3) - 3*mean*E(x^2) + 2*mean^3
df['ror_cube'] = df['ror'].pow(3)
skew_df = (df['ror_cube'].mean() - 3*mean_df*(df['ror_sq'].mean()) + 2*pow(mean_df,3)) / pow(var_df, 1.5)
print("skew: ", skew_df)

# 방법2 : ((x-mean)^3의 평균)/std^3
df['ror_dv'] = df['ror']-mean_df
skew_df_2  = (df['ror_dv'].pow(3).mean()) / pow(var_df, 1.5)
print(skew_df_2)

# kurtosis = E(x-mean)^4/std^4
kurt_df = df['ror_dv'].pow(4).mean() / pow(var_df, 2)
print("kurtosis: ", kurt_df)

# 정규성 검정
