from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert

import pandas as pd
import os

######
# kospi 100 종목 읽어오기
######

df = pd.read_csv('C:/ESG/data/KOSPI100.csv')
stocks = df['종목명'].to_list() 
# print(stocks[:5])

######
# 자동 검색 및 다운로드
######

# # 현재 열려있는 크롬창 제어
# from selenium.webdriver.chrome.options import Options
# chrome_options = Options()
# chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# chrome_driver = "C:/ESG/chromedriver.exe" 
# browser = webdriver.Chrome(chrome_driver, options=chrome_options)
# browser.get("https://www.bigkinds.or.kr/v2/news/index.do")

# browser = webdriver.Chrome() 

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
browser = webdriver.Chrome(options=options)
browser.get("https://www.bigkinds.or.kr/")

# 로그인
browser.find_element_by_xpath('//*[@id="header"]/div[1]/div/div/button[1]').click()
# browser.find_element_by_xpath('//*[@id="login-user-id"]').send_keys("") #id
time.sleep(1) 
# browser.find_element_by_xpath('//*[@id="login-user-password"]').send_keys("") #pw
time.sleep(1)
browser.find_element_by_xpath('//*[@id="login-btn"]').click()

# 뉴스검색분석 클릭
browser.find_element_by_xpath('//*[@id="header"]/div[2]/div[2]/div[1]/div/div[1]/div/ul/li[1]').click()
browser.find_element_by_xpath('//*[@id="header"]/div[2]/div[2]/div[1]/div/div[2]/div/div[1]/ul/li[1]').click()

for i in stocks :

    # 기간클릭
    browser.find_element_by_xpath('//*[@id="collapse-step-1-body"]/div[3]/div/div[1]/div[1]').click()
    time.sleep(0.5)

    # 시작날짜 끝날짜 입력
    elem = browser.find_element_by_xpath('//*[@id="search-begin-date"]')
    elem.click()
    elem.send_keys(Keys.CONTROL, 'a')
    elem.send_keys("2012-01-01") 	

    elem = browser.find_element_by_xpath('//*[@id="search-end-date"]')
    elem.click()
    elem.send_keys(Keys.CONTROL, 'a')
    elem.send_keys("2021-12-31") 	
    time.sleep(0.5)

    # 상세검색 클릭
    browser.find_element_by_xpath('//*[@id="collapse-step-1-body"]/div[3]/div/div[3]/div[1]').click() # 상세검색 클릭
    time.sleep(0.5)

    # 검색어범위 클릭 후 "제목"으로 설정
    search_range = browser.find_element_by_xpath('//*[@id="search-scope-type"]')
    search_range.click() # 검색어 범위 클릭 (제목+본문, 제목, 본문)
    search_range.send_keys(Keys.DOWN) # 아래(=제목)

    # 찾고자하는 단어 입력
    search_1 = browser.find_element_by_xpath('//*[@id="orKeyword1"]')  #단어중한개이상포함 
    search_1.send_keys('''
    논란, 갈등, 비판, 우려, 문제, 비난, 사태, 파장,
    고소, 위반, 기소, 위법, 불법, 고발, 소송, 조사, 책임, 훼손,
    공정위, 
    원점, 분쟁, 실형, 혐의, 폭력, 징역, 과징금,
    가시밭길, 하세월, 험로, 암초, 시대착오, 불발, 반성,
    저지, 구조조정, 강대강, 호소, 불투명,
    합병무산,
    사퇴, 해임, 징계,
    파업, 노사분쟁
    ''')
    time.sleep(5)
    # search_2 = browser.find_element_by_xpath('') //*[@id="andKeyword1"] #다음단어모두포함 
    search_3 = browser.find_element_by_xpath('//*[@id="exactKeyword1"]') #정확히일치하는단어 
    search_3.click()
    search_3.send_keys(i)

    # 검색 클릭
    browser.find_element_by_xpath('//*[@id="detailSrch1"]/div[7]/div/button[2]').click()

    # 로딩 대기
    element = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located( \
    (By.XPATH, '//*[@id="dataResult-news"]/a') ))

    # 분석 결과 클릭
    browser.find_element_by_xpath('//*[@id="collapse-step-3"]').click()
    time.sleep(5)
  
    # 엑셀 다운로드 클릭
    # element = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located( \
    # (By.XPATH, '//*[@id="analytics-data-download"]/div[3]/button') ))
    browser.find_element_by_xpath('//*[@id="analytics-data-download"]/div[3]/button').click()

    try :
        WebDriverWait(browser,3).until(EC.alert_is_present())
        da = Alert(browser)
        da.accept()
        time.sleep(20)
    except :
        pass  
    
    time.sleep(20) # 다운로드대기


    #새로고침
    browser.refresh()


######
# 파일명 변경
######
for k in range(1,len(stocks)) :
    file_oldname = os.path.join("C://Users//bes55//Downloads", "NewsResult_20120101-20211231 ({}).xlsx".format(k))  
    file_newname_newfile = os.path.join("C://Users//bes55//Downloads", "{}.xlsx".format(stocks[k]))
    os.rename(file_oldname, file_newname_newfile)
