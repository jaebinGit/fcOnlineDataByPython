import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://fconline.nexon.com/datacenter/rank"

# Safari 브라우저 초기화
browser = webdriver.Safari()
browser.maximize_window()
browser.get(url)

# 동적 배열 (리스트) 초기화
names_list = []

#1페이지(1~20위) 부터 5페이지(81위~100위)까지 크롤링
for i in range(1, 6):
    xpath_to_click = f'//*[@id="inner"]/div[2]/div/ul/li[{i}]/a'

    element_to_click = WebDriverWait(browser, 20).until(
        EC.element_to_be_clickable((By.XPATH, xpath_to_click))
    )
    element_to_click.click()

    time.sleep(2)
    # 페이지 이동 후 요소 찾기 대기
    html_comments = WebDriverWait(browser, 20).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "profile_pointer"))
    )

    for comment in html_comments:
        name = comment.text
        names_list.append(name)

    # 페이지 이동 후 대기
    time.sleep(2)

# DataFrame 생성
df = pd.DataFrame({'Names': names_list})

# Excel 파일로 저장
df.to_excel('names_data.xlsx', index=False)

# 출력
print("Names List:")
print(df)

# 브라우저 종료
browser.quit()

