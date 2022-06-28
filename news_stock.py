
df = pd.read_excel('C:/ESG/'+file_name+'_정리.xlsx', engine='openpyxl')

ticker_dict = dict(zip(df_kospi['종목명'].to_list(),df_kospi['종목코드'].to_list())) # 종목명-종목코드 dict화
# 0~+15일
ror = []
for i in range(df.shape[0]) : #df.shape[0]
    ticker = ticker_dict.get(df.iloc[i]['기업']) # 해당 기업의 종목코드 찾기
    date = str(int(df.iloc[i]['일자']))
    date0 = datetime.date(int(date[:4]),int(date[4:6]),int(date[6:8]))
    date1 = date0 - datetime.timedelta(days=7)
    date2 = date0 + datetime.timedelta(days=60) # 무러 2달이나 넉넉하게 잡음....
    date_dash = date[:4]+'-'+date[4:6]+'-'+date[6:8]
    
    df_stock_temp = stock.get_market_ohlcv(date1.strftime('%Y%m%d'), date2.strftime('%Y%m%d'),ticker,'d')
    df_stock_temp = df_stock_temp.reset_index() # inplace = True 가 default
    if df_stock_temp.shape[0] > 0 :
        df_stock_temp['날짜'] = pd.to_datetime(df_stock_temp['날짜'])
        df_stock_temp['ror'] = df_stock_temp['종가']/df_stock_temp['종가'].shift(1) - 1 # 수익률 생성
        df_stock_temp = df_stock_temp[df_stock_temp['날짜'] >= date_dash] # 날짜 조정 : 보도일자 이후만 살리기
        ror_temp = list(np.array(df_stock_temp['ror'].tolist()))
        if len(ror_temp) >= 16 :
            ror_temp = ror_temp[:16]
        else : # 넉넉히 잡았는데도 개수가 부족하면 NaN 처리
            ror_temp = [np.NaN for j in range(16)]
    else : # 비어있다면
        ror_temp = [np.NaN for j in range(16)]
    
    # kospi 자료 추가 (ticker 1001)
    df_kospi_temp = stock.get_index_ohlcv(date1.strftime('%Y%m%d'), date2.strftime('%Y%m%d'), '1001' ,'d')
    df_kospi_temp = df_kospi_temp.reset_index()
    if df_kospi_temp.shape[0] > 0 :
        df_kospi_temp['날짜'] = pd.to_datetime(df_kospi_temp['날짜'])
        df_kospi_temp['ror'] = df_kospi_temp['종가']/df_kospi_temp['종가'].shift(1) - 1 # 수익률 생성
        df_kospi_temp = df_kospi_temp[df_kospi_temp['날짜'] >= date_dash] # 날짜 조정 : 보도일자 이후만 살리기
        ror_kospi_temp = list(np.array(df_kospi_temp['ror'].tolist()))
        if len(ror_kospi_temp) >= 16 :
            ror_kospi_temp = ror_kospi_temp[:16]
        else : # 넉넉히 잡았는데도 개수가 부족하면 NaN 처리
            ror_kospi_temp = [np.NaN for j in range(16)]
    else : # 비어있다면
        ror_kospi_temp = [np.NaN for j in range(16)]
    
    # ror_temp와 ror_kospi_temp 연결
    ror_temp.extend(ror_kospi_temp)

    # ror이라는 이중list
    ror.append(ror_temp) 

    if i%100 == 0:
        print(i)

for k in range(len(ror)) : # 16+16이 아니면 nan으로 변환
    if len(ror[k]) < 32 :
        ror[k] = [np.NaN for j in range(32)]
        print(k)

ror = np.array(ror) # list를 np로 바꾸기
column_names = ['ror_{}'.format(i) for i in range(0,16)] 
column_names_k = ['kopsi_{}'.format(i) for i in range(0,16)] 
column_names.extend(column_names_k)
df_ror = pd.DataFrame(ror, columns=column_names) 
df = pd.concat([df, df_ror], axis=1)  # 그대로 axis=1 방향으로 붙이기

# ValueError: Shape of passed values is (4095, 1), indices imply (4095, 16)
# => 이 Error는 지금 16개 다 못채워서 나오는 error

#######
# -5~0일
ror = []
ror_temp = [np.NaN for i in range(5)] # ror_temp 초기화
for i in range(df.shape[0]) : 
    ticker = ticker_dict.get(df.iloc[i]['기업']) # 해당 기업의 종목코드 찾기
    date = str(int(df.iloc[i]['일자']))
    date0 = datetime.date(int(date[:4]),int(date[4:6]),int(date[6:8]))
    date1 = date0 - datetime.timedelta(days=20) # 넉넉히 가져오기 
    date_dash = date[:4]+'-'+date[4:6]+'-'+date[6:8]

    df_stock_temp = stock.get_market_ohlcv(date1.strftime('%Y%m%d'), date0.strftime('%Y%m%d'), ticker,'d')
    df_stock_temp = df_stock_temp.reset_index()
    if df_stock_temp.shape[0] > 0 :
        df_stock_temp['날짜'] = pd.to_datetime(df_stock_temp['날짜'])
        df_stock_temp['ror'] = df_stock_temp['종가']/df_stock_temp['종가'].shift(1) - 1 # 수익률 생성
        ror_temp = list(np.array(df_stock_temp['ror'].tolist()))
        if len(ror_temp) >= 5 :
            ror_temp = ror_temp[-6:-1] # 5개만큼 추리기, 이때 t=0는 제외해야 중복안됨
        else : # 넉넉히 잡았는데도 개수가 부족하면 NaN 처리
            ror_temp = [np.NaN for j in range(5)]
    else : # 비어있다면
        ror_temp = [np.NaN for j in range(5)]

    # kospi 자료 추가 (ticker 1001)
    df_kospi_temp = stock.get_index_ohlcv(date1.strftime('%Y%m%d'), date0.strftime('%Y%m%d'), '1001' ,'d')
    df_kospi_temp = df_kospi_temp.reset_index()
    if df_kospi_temp.shape[0] > 0 :
        df_kospi_temp['날짜'] = pd.to_datetime(df_kospi_temp['날짜'])
        df_kospi_temp['ror'] = df_kospi_temp['종가']/df_kospi_temp['종가'].shift(1) - 1 # 수익률 생성
        ror_kospi_temp = list(np.array(df_kospi_temp['ror'].tolist()))
        if len(ror_kospi_temp) >= 5 :
            ror_kospi_temp = ror_kospi_temp[-6:-1]    
        else : # 넉넉히 잡았는데도 개수가 부족하면 NaN 처리
            ror_kospi_temp = [np.NaN for j in range(5)]
    else : # 비어있다면
        ror_kospi_temp = [np.NaN for j in range(5)]
    
    ror_temp.extend(ror_kospi_temp)

    # ror이라는 이중list
    ror.append(ror_temp) 

    if i%100 == 0:
        print(i)    

for k in range(len(ror)) :
    if len(ror[k]) < 10 :
        ror[k] = [np.NaN for j in range(10)]
        print(k)

ror = np.array(ror) # list를 np로 바꾸기
column_names = ['ror_{}'.format(i) for i in range(-5,0)]
column_names_k = ['kopsi_{}'.format(i) for i in range(-5,0)] 
column_names.extend(column_names_k)
df_ror = pd.DataFrame(ror, columns=column_names) 
df = pd.concat([df, df_ror], axis=1)

print(df.shape)
print(df.head())
df.to_excel('C:/ESG/'+file_name+'_정리.xlsx', index=None)
