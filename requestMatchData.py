import time

import pandas as pd
import requests
from pandas._libs import json

#excel에 저장될 각 항목 초기화
longPassTryData_list = []
throughPassTryData_list = []
shortPassTryData_list = []
passTryData_list = []
dirrbleData_list = []

possessionData_list = []
controllerData_list = []
shootTotalData_list = []
goalTotalData_list = []
shootHeadingData_list = []
shootInPenaltyData_list = []
shootOutPenaltyData_list = []
tackleTryData_list = []
effectiveShootTotalData_list = []


#match 고유 식별자 번호 읽어 API 호출하여 각 match 고유 식별자 번호에 대한 matchData 불러오기
df = pd.read_excel('output.xlsx')
for i in range(0,100):
    for j in range(0,100):
        matchid = df[i][j]
        matchtype = 50
        if(pd.isna(matchid) == True) :  #빈 cell에 대한 처리 (최근 100경기를 채우지 못한 경우)
            print("error detective")
            continue
        key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJYLUFwcC1SYXRlLUxpbWl0IjoiNTAwOjEwIiwiYWNjb3VudF9pZCI6IjE2Mjc3MDI5ODUiLCJhdXRoX2lkIjoiMiIsImV4cCI6MTcxNTc3NDY0MCwiaWF0IjoxNzAwMjIyNjQwLCJuYmYiOjE3MDAyMjI2NDAsInNlcnZpY2VfaWQiOiI0MzAwMTE0ODEiLCJ0b2tlbl90eXBlIjoiQWNjZXNzVG9rZW4ifQ.DBLzRXmygkn3Um5lEDrv1SWf8y9uSCpeK78p4Nab3k4"
        matchdata = requests.get(f"https://public.api.nexon.com/openapi/fconline/v1.0/matches/{matchid}",
                     headers = {"Authorization" : key})
        # JSON 데이터 파싱
        data = matchdata.json()

        # 원하는 항목 추출
        matchIdTest = data['matchId']
        print(matchIdTest)
        matchResult = data['matchInfo'][0]['matchDetail']['matchResult']
        matchEndType = data['matchInfo'][0]['matchDetail']['matchEndType']
        try:    #API server에 데이터가 존재하지 않는 경우 예외 처리 (탈퇴, 정지 등의 사유)
            if((matchResult == '승' and matchEndType == 0)) : #승리한 user의 데이터만 불러오기
                longPassTry = data['matchInfo'][0]['pass']['longPassTry']
                throughPassTry = data['matchInfo'][0]['pass']['throughPassTry']
                shortPassTry = data['matchInfo'][0]['pass']['shortPassTry']
                passTry = data['matchInfo'][0]['pass']['passTry']
                dirrble = data['matchInfo'][0]['matchDetail']['dribble']

                possession = data['matchInfo'][0]['matchDetail']['possession']
                controller = data['matchInfo'][0]['matchDetail']['controller']
                shootTotal = data['matchInfo'][0]['shoot']['shootTotal'] + data['matchInfo'][1]['shoot']['shootTotal']
                goalTotal = data['matchInfo'][0]['shoot']['goalTotal'] + data['matchInfo'][1]['shoot']['goalTotal']
                shootHeading = data['matchInfo'][0]['shoot']['shootHeading']
                shootInPenalty = data['matchInfo'][0]['shoot']['shootInPenalty']
                shootOutPenalty = data['matchInfo'][0]['shoot']['shootOutPenalty']
                tackleTry = data['matchInfo'][0]['defence']['tackleTry']
                effectiveShootTotal = data['matchInfo'][0]['shoot']['effectiveShootTotal']

            elif((matchResult == '패' and matchEndType == 0)) : #승리한 user의 데이터만 불러오기
                longPassTry = data['matchInfo'][1]['pass']['longPassTry']
                throughPassTry = data['matchInfo'][1]['pass']['throughPassTry']
                shortPassTry = data['matchInfo'][1]['pass']['shortPassTry']
                passTry = data['matchInfo'][1]['pass']['passTry']
                dirrble = data['matchInfo'][1]['matchDetail']['dribble']

                possession = data['matchInfo'][1]['matchDetail']['possession']
                controller = data['matchInfo'][1]['matchDetail']['controller']
                shootTotal = data['matchInfo'][0]['shoot']['shootTotal'] + data['matchInfo'][1]['shoot']['shootTotal']
                goalTotal = data['matchInfo'][0]['shoot']['goalTotal'] + data['matchInfo'][1]['shoot']['goalTotal']
                shootHeading = data['matchInfo'][1]['shoot']['shootHeading']
                shootInPenalty = data['matchInfo'][1]['shoot']['shootInPenalty']
                shootOutPenalty = data['matchInfo'][1]['shoot']['shootOutPenalty']
                tackleTry = data['matchInfo'][1]['defence']['tackleTry']
                effectiveShootTotal = data['matchInfo'][0]['shoot']['effectiveShootTotal']

        except IndexError as e:
            continue
        # 정상적으로 data 불러온 경우 각 data에 맞는 List에 추가
        longPassTryData_list.append(longPassTry)
        throughPassTryData_list.append(throughPassTry)
        shortPassTryData_list.append(shortPassTry)
        dirrbleData_list.append(dirrble)
        shootOutPenaltyData_list.append(shootOutPenalty)
        passTryData_list.append(passTry)

        possessionData_list.append(possession)
        shootTotalData_list.append(shootTotal)
        goalTotalData_list.append(goalTotal)
        shootHeadingData_list.append(shootHeading)
        shootInPenaltyData_list.append(shootInPenalty)
        tackleTryData_list.append(tackleTry)
        controllerData_list.append(controller)
        effectiveShootTotalData_list.append(effectiveShootTotal)
    #서버 과부화 방지 time.sleep
    time.sleep(5)
    print("timeSleep")
#만들어진 data에 대한 row name 만들기
df_result = pd.DataFrame({'longPassTry': longPassTryData_list, 'throughPassTry': throughPassTryData_list,
                          'shortPassTry': shortPassTryData_list,'dirrble': dirrbleData_list,
                          'shootOutPenalty': shootOutPenaltyData_list,'passTry': passTryData_list,
                          'possession': possessionData_list,'shootTotal': shootTotalData_list,
                          'goalTotal': goalTotalData_list,'shootHeading': shootHeadingData_list,
                          'shootInPenalty': shootInPenaltyData_list,'tackleTry': tackleTryData_list,
                          'controller': controllerData_list,})

# 결과 Excel 파일로 저장
df_result.to_excel('matchData.xlsx', index=False)




