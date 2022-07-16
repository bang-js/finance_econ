###################
# AR까지 계산 완료한 상태
# 비슷한 기사가 며칠 간 쏟아져 나오는 경우 분석에 오류
# 15일 동안 같은 키워드 / 같은 기업 이면 제외

# 추가로 같은 window에 여러 키워드가 섞여있는 경우 제거해야함
###################

import pandas as pd 
import datetime as dt

file_name = 'DF_최종_5'


# # 키워드별 분류
# df = pd.read_excel('C:/ESG/'+file_name+'_AR.xlsx', engine='openpyxl')
# df['일자'] = df['일자'].astype(str)
# df['일자'].str[-8:]
# df['일자'] = pd.to_datetime(df['일자'])

# # 정렬
# df.sort_values(by=['기업','ESG','일자'], ascending=[True,True,False] ,inplace=True)
# df.reset_index(drop=True, inplace=True) # index 초기화

# overlap = []
# for i in range(df.shape[0]):
#     overlap_temp = [] # 각 i마다 iter에 사용
#     if i < df.shape[0]-15 :
#         for j in range(1,15) :
#             if (df.iloc[i]['일자'] - dt.timedelta(days=10) <= df.iloc[i+j]['일자'] < df.iloc[i]['일자']) & \
#             (df.iloc[i]['ESG'] == df.iloc[i+j]['ESG']) & (df.iloc[i]['기업'] == df.iloc[i+j]['기업']) :
#                 overlap_temp.append(True) 
#             else :
#                 overlap_temp.append(False)
#         if True in overlap_temp : # 하나라도 T가 있으면 중복되는 기사가 있으므로 T로 overlap에 저장
#             overlap.append(True)
#         else : # 전부 F
#             overlap.append(False)
        
#     else :
#         j = 1
#         while i+j < df.shape[0] :
#             if (df.iloc[i]['일자'] - dt.timedelta(days=10) <= df.iloc[i+j]['일자'] < df.iloc[i]['일자'])  & (df.iloc[i]['ESG'] == df.iloc[i+j]['ESG']) \
#                 & (df.iloc[i]['기업'] == df.iloc[i+j]['기업']) :
#                 overlap_temp.append(True)
#             else :
#                 overlap_temp.append(False)
#             j +=1 
#         if True in overlap_temp : 
#             overlap.append(True)
#         else :
#             overlap.append(False)
    
#     if i%100 == 0:
#         print(i)

# df['OVERLAP'] = overlap # T/F

# # overlap 횟수
# df.sort_values(by=['기업','ESG','일자'], ascending=[True,True,True] ,inplace=True)
# df.reset_index(drop=True, inplace=True)

# over_nums =[]
# for i in range(df.shape[0]):
#     over_num = df.iloc[i]['중복 횟수']
#     if i < df.shape[0]-15 :
#         for j in range(1,15) :
#             if (df.iloc[i]['일자'] < df.iloc[i+j]['일자'] <= df.iloc[i]['일자'] + dt.timedelta(days=10)) & (df.iloc[i]['ESG'] == df.iloc[i+j]['ESG']) \
#                 & (df.iloc[i]['기업'] == df.iloc[i+j]['기업']) :
#                 over_num += df.iloc[i+j]['중복 횟수']+1 # 해당 row도 포함
#     else :
#         j = 1
#         while i+j < df.shape[0] :
#             if (df.iloc[i]['일자'] < df.iloc[i+j]['일자'] <= df.iloc[i]['일자'] + dt.timedelta(days=10))  & (df.iloc[i]['ESG'] == df.iloc[i+j]['ESG']) \
#                 & (df.iloc[i]['기업'] == df.iloc[i+j]['기업']) :
#                 over_num += df.iloc[i+j]['중복 횟수']+1 # 해당 row도 포함
#             j +=1 
#     over_nums.append(over_num)
    
#     if i%100 == 0:
#         print(i)
# df['중복 횟수(10일)'] = over_nums

# # True 제거
# df = df[df['OVERLAP']==False]

# print(df.head())
# print(df.shape)
# df.to_excel('C:/ESG/'+file_name+'_AR_10일중복.xlsx', index=None)



# ##############
# # sorting
# ##############

# df = pd.read_excel('C:/ESG/'+file_name+'_AR_15일중복.xlsx', engine='openpyxl')
# print(df['ESG'].value_counts())


###############
# 중복3 
# 중복5
# 중복10
###############


ov = [0,4,9]
for i in ov :
    df = pd.read_excel('C:/ESG/'+file_name+'_AR_10일중복_anounce.xlsx', engine='openpyxl')
    df = df[df['중복 횟수(10일)']>i]
    df.to_excel('C:/ESG/'+file_name+'_AR_10일중복_중복{}_anounce.xlsx'.format(i+1), index=None)


