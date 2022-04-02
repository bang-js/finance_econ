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


###
# 상관계수 계산
###

# 난수로 두 series 만들기 
lst1 = []
lst2 = []
for i in range(100) :
    lst1.append(random.random())
    lst2.append(random.random())
series1 = pd.Series(lst1)
series2 = pd.Series(lst2)

# 평균 및 표준편차 계산
mean_1 = series1.mean()
mean_2 = series2.mean()

series1_sq = series1.pow(2) 
series2_sq = series2.pow(2) 
std_1 = pow(series1_sq.mean() - pow(mean_1,2) ,0.5)
std_2 = pow(series2_sq.mean() - pow(mean_2,2) ,0.5)
print(mean_1, mean_2, std_1,std_2)

# 공분산 및 상관계수 
mul_series1_2 = (series1 - mean_1)*(series2 - mean_2)
cov = mul_series1_2.mean()
print("공분산: ",cov)
corr_ef = cov/(std_1*std_2)
print("상관계수: ", corr_ef)


