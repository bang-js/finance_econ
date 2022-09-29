##############
# t-stat 계산해야함
##############

import pandas as pd
import numpy as np
from scipy import stats

# results = ['_AR.xlsx' , '_AR_10일중복.xlsx', '_AR_10일중복_중복1.xlsx', '_AR_10일중복_중복5.xlsx', '_AR_10일중복_중복10.xlsx']
results = ['_AR_10일중복_anounce.xlsx', '_AR_10일중복_중복1_anounce.xlsx', '_AR_10일중복_중복5_anounce.xlsx', '_AR_10일중복_중복10_anounce.xlsx']

file_name = 'DF_최종_5'

for r in results :
    print(file_name+r)
    df = pd.read_excel('C:/ESG/'+file_name+r, engine='openpyxl')

    # ### 기사 수 분석
    print('기사 수',df.shape[0])
    esg_cate = df['ESG'].value_counts() 
    esg_lst = esg_cate.index.to_list() # ESG 종류
    print('기업종류', len(df['기업'].value_counts().index.to_list()))
    print('ESG 종류', len(esg_lst))
    print('ESG 통계', esg_cate)

    s_e = [(0,1),(0,3),(0,5),(-1,1),(-1,3),(-1,5),(-5,5)]
    CARs = []
    for s,e in s_e :
        CARs.append('CAR_{}_{}'.format(s,e))
    index = ['mean','t_stat','p_value']
    esg_lst2 = ['tot']
    esg_lst2.extend(esg_lst)
    esg_lst2.extend(['노동자','공급','소비자','부패','S','G'])
    column = pd.MultiIndex.from_product([esg_lst2, CARs], names=['ESG세부', 'CAR'])

    # 전체 t-test
    lst = []
    for car in CARs :
        m = df[car].mean()
        t_stat, p_value = stats.ttest_1samp(df[car], 0)
        lst_temp = [m, t_stat, p_value]
        lst.append(lst_temp)
        # print(car,'\n', 'averg: {:.4f}'.format(m),'t-stat: {:.4f}'.format(t_stat) , 'p-value: {:.4f}'.format(p_value))
    


    # esg 소분류별 t-test
    for esg in esg_lst :
        df_temp = df[df['ESG']==esg]    
        for car in CARs :
            m = df_temp[car].mean()
            t_stat, p_value = stats.ttest_1samp(df_temp[car], 0)
            lst_temp = [m, t_stat, p_value]
            lst.append(lst_temp)            
            # print(car,'\n', 'averg: {:.4f}'.format(m),'t-stat: {:.4f}'.format(t_stat) , 'p-value: {:.4f}'.format(p_value))

    # esg 중분류별 t-test
    labor =['파업','산재','고용','임금','노동권'] 
    supply = ['독과점','공급망','상생']
    consumer = ['품질','개인정보','유해물질','광고']
    corrupt =['비리','도덕성'] 
    esg_mid = [labor, supply, consumer, corrupt]

    for mid in esg_mid :
        for mi in mid:
            if mi == mid[0]:
                df_temp= df[df['ESG']==mi]
            else :
                df_temp = pd.concat([df_temp, df[df['ESG']==mi]],ignore_index=True)
        
        for car in CARs :
            m = df_temp[car].mean()
            t_stat, p_value = stats.ttest_1samp(df_temp[car], 0)
            lst_temp = [m, t_stat, p_value]
            lst.append(lst_temp)    

    # esg 대분류별 test
    Ss= ['파업','산재','고용','임금','노동권', '독과점','공급망','상생','품질','개인정보','유해물질','광고','성범죄'] 
    Gs = ['비리','도덕성','경영권','불공정거래','분식회계']
    esg_lg = [Ss, Gs]
    for lg in esg_lg :
        for l in lg:
            if l == lg[0]:
                df_temp= df[df['ESG']==l]
            else :
                df_temp = pd.concat([df_temp, df[df['ESG']==l]],ignore_index=True)
        
        for car in CARs :
            m = df_temp[car].mean()
            t_stat, p_value = stats.ttest_1samp(df_temp[car], 0)
            lst_temp = [m, t_stat, p_value]
            lst.append(lst_temp)    


    lst = np.array(lst)
    lst = np.transpose(lst)
    df_result = pd.DataFrame(lst, columns=column, index=index)

    df_result.to_excel('C:/ESG/'+file_name+'_t_test'+r)


    # ###############
    # # 기사 수 분석
    # ###############
    # a= df['기업'].value_counts()
    # b= df['ESG'].value_counts()
    # print('기사 수', df.shape[0])
    # print('기업 수', len(a.index.to_list()))
    # print('ESG 종류', len(b.index.to_list()))
    # print(b)

    print('\n')









