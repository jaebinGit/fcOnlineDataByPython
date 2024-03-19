import pandas as pd
import requests

#동적 배열 초기화
access_ids = []

#nickname정보 읽고 정보 불러오기
df = pd.read_excel('names_data.xlsx')
names_list = df['Names'].tolist()

#API 호출하여 각 nickname에 대한 고유 식별자 번호 불러오기
for name in names_list:
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJYLUFwcC1SYXRlLUxpbWl0IjoiNTAwOjEwIiwiYWNjb3VudF9pZCI6IjE2Mjc3MDI5ODUiLCJhdXRoX2lkIjoiMiIsImV4cCI6MTcxNTc3NDY0MCwiaWF0IjoxNzAwMjIyNjQwLCJuYmYiOjE3MDAyMjI2NDAsInNlcnZpY2VfaWQiOiI0MzAwMTE0ODEiLCJ0b2tlbl90eXBlIjoiQWNjZXNzVG9rZW4ifQ.DBLzRXmygkn3Um5lEDrv1SWf8y9uSCpeK78p4Nab3k4"
    accessId = requests.get(f"https://public.api.nexon.com/openapi/fconline/v1.0/users?nickname={name}",
                    headers = {"Authorization" : key})
            # print(a.json());
            # JSON 데이터 파싱
    data = accessId.json()
    accessid = data['accessId']
    print(accessid)
    access_ids.append(accessid)

#Names열, Access_id열 생성하여 각 원소 저장
df_result = pd.DataFrame({'Names': names_list, 'Access_id': access_ids})

# 결과 Excel 파일로 저장
df_result.to_excel('accessId_data.xlsx', index=False)