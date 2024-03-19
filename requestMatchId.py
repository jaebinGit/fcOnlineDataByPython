import pandas as pd
import requests

#동적 배열 초기화
matchData = []

#고유 식별자 번호 excel 파일 열고 정보 불러오기
df = pd.read_excel('accessId_data.xlsx')
access_ids_list = df['Access_id'].tolist()

#API 호출하여 각 AccessId에 대해 매치 고유 식별자 번호 불러오기
for accessid in access_ids_list:
    accessid = accessid
    matchtype = 50
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJYLUFwcC1SYXRlLUxpbWl0IjoiNTAwOjEwIiwiYWNjb3VudF9pZCI6IjE2Mjc3MDI5ODUiLCJhdXRoX2lkIjoiMiIsImV4cCI6MTcxNTc3NDY0MCwiaWF0IjoxNzAwMjIyNjQwLCJuYmYiOjE3MDAyMjI2NDAsInNlcnZpY2VfaWQiOiI0MzAwMTE0ODEiLCJ0b2tlbl90eXBlIjoiQWNjZXNzVG9rZW4ifQ.DBLzRXmygkn3Um5lEDrv1SWf8y9uSCpeK78p4Nab3k4"
    a = requests.get(f"https://public.api.nexon.com/openapi/fconline/v1.0/users/{accessid}/matches?matchtype={matchtype}", headers = {"Authorization" : key})
    print(a.json())
    matchData.append(a.json())

#불러온 매치 식별자 번호 저장
df = pd.DataFrame(matchData)
excel_file_path = 'output.xlsx'
df.to_excel(excel_file_path, index=False)
print(f'Data saved to {excel_file_path}')

