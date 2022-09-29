from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
import requests, bs4
from html_table_parser import parser_functions as parser
import pandas as pd
import numpy as np
import datetime 

df_kospi = pd.read_csv('C:/ESG/data/KOSPI.csv',  encoding='cp949')
df_kospi['종목코드'] = df_kospi['종목코드'].astype(str).str.zfill(6) 
ticker_dict = dict(zip(df_kospi['종목명'].to_list(),df_kospi['종목코드'].to_list())) # 종목명이 key
ticker_dict2 = dict(zip(df_kospi['종목코드'].to_list(),df_kospi['종목명'].to_list())) 

file_name = 'DF_최종_5_AR_10일중복'

df_target = pd.read_excel('C:/ESG/'+file_name+'.xlsx', engine='openpyxl')
stocks_name = df_target['기업'].value_counts().index.to_list()
stocks = [str(ticker_dict.get(i)) for i in stocks_name]

# # # 현재 열려있는 크롬창 제어
# # chrome_driver = "C:/ESG/chromedriver.exe"
# options = webdriver.ChromeOptions()
# options.add_experimental_option("excludeSwitches", ["enable-logging"])
# browser = webdriver.Chrome(options=options)
# browser.get("https://dart.fss.or.kr/dsab007/main.do?option=corp")

# # 공시일 저장용 list
# ancs = []

# df = pd.DataFrame(columns=['종목명','접수일자'])

# for i in stocks :
#     time.sleep(1)
#     # 종목명 입력
#     elem =  browser.find_element_by_xpath('//*[@id="textCrpNm"]')
    
#     elem.click()
#     elem.send_keys(i)
#     elem.send_keys(Keys.TAB)
#     time.sleep(0.1)

#     # 기간클릭    
#     # 시작날짜 끝날짜 입력
#     elem = browser.find_element_by_xpath('//*[@id="startDate"]')
#     elem.click()
#     elem.send_keys(Keys.CONTROL, 'a')
#     elem.send_keys("20120101") 	

#     elem = browser.find_element_by_xpath('//*[@id="endDate"]')
#     elem.click()
#     elem.send_keys(Keys.CONTROL, 'a')
#     elem.send_keys("20211231") 	
#     time.sleep(0.1)

#     # 정기공시 체크
#     browser.find_element_by_xpath('//*[@id="li_01"]/label[1]/img').click() # 통합분류
#     time.sleep(0.5) 

#     # 조회건수 100 설정
#     items = browser.find_element_by_xpath('//*[@id="maxResultsCb"]')
#     items.click()
#     items.send_keys(Keys.DOWN) # 15->30
#     items.send_keys(Keys.DOWN) # 30->50
#     items.send_keys(Keys.DOWN) # 50->100
#     items.send_keys(Keys.ENTER)

#     # 검색 클릭
#     browser.find_element_by_xpath('//*[@id="searchForm"]/div[2]/div[2]/a[1]').click()
#     time.sleep(1)


#     ####
#     # beautiful soup으로 긁기!!
#     html = browser.page_source
#     response = bs4.BeautifulSoup(html, 'html.parser')
#     # td 추출
#     head = response.find('thead')
#     head = head.find_all('th')
#     head = [head[i].text for i in range(len(head))]
    
#     target = response.find('tbody')
#     p = parser.make2d(target)
#     df_temp = pd.DataFrame(p, columns=head)

#     df_temp['종목명']=  ticker_dict2.get(i) 
#     df_temp = df_temp[['종목명','접수일자']]
#     df = pd.concat([df, df_temp], axis=0, ignore_index=True)
#     print(df, df.shape)

#     # anc_days = df_temp['접수일자'].to_list()
#     # ancs.append(anc_days)
#     # print(anc_days)
    
#     browser.refresh()

# df.to_excel('C:/ESG/anounce.xlsx', engine='openpyxl')

# anc_dict = dict(zip(df_kospi['종목명'].to_list(),ancs)) 
# print(anc_dict[:5])
# print(len(anc_dict))




###공시날짜와 news날짜 매칭 후 제거 (+-5)

df_anc = pd.read_excel('C:/ESG/anounce.xlsx', engine='openpyxl') 
# df_anc['접수일자'].apply(lambda _ : datetime.datetime.strptime(_,'%Y.%m.%d'))
df_anc['접수일자'] = pd.to_datetime(df_anc['접수일자'])
print(df_anc.info())

df_target['일자'] = pd.to_datetime(df_target['일자'])
column = list(df_target.columns)
df_tot = pd.DataFrame(columns=column)

for stock in stocks_name:
    df_anc_temp = df_anc[df_anc['종목명']==stock]
    df_target_temp = df_target[df_target['기업']==stock]
    elim = []
    for i in range(df_target_temp.shape[0]):
        elim_temp = []
        for j in range(df_anc_temp.shape[0]):
            if (df_target_temp.iloc[i]['일자'] - datetime.timedelta(days=6) < df_anc_temp.iloc[j]['접수일자'] < df_target_temp.iloc[i]['일자'] + datetime.timedelta(days=6)) :
                elim_temp.append(True)
            else:
                elim_temp.append(False)
        if True in elim_temp : # 하나라도 T가 있으면 중복되는 기사가 있으므로 T로  저장
            elim.append(True)
        else : # 전부 F
            elim.append(False)
    print(stock)
    df_target_temp['제거']=elim
    df_target_temp = df_target_temp[df_target_temp['제거']==False]
    df_tot = pd.concat([df_tot, df_target_temp], ignore_index=True)
print(df_tot.shape)    

df_tot.to_excel('C:/ESG/'+ file_name +'_anounce.xlsx', engine='openpyxl')
