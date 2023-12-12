#해외 사이트 배당률 있는 경기만 가져옴
'''
import os
import pandas as pd
import requests
import argparse

api_key = os.getenv("2df36f9a31375b56518afeeb68db23bc")

import requests
 
url = "https://api.apilayer.com/odds/sports/basketball_nba/odds?regions=us&oddsFormat=decimal&markets=h2h&dateFormat=iso"
 
payload = {}
headers= {
  "apikey": "pgSU7ZuWkurGFaht6eAwF4Zg9VGWSZoy"
}
 
response = requests.request("GET", url, headers=headers, data = payload)
 
status_code = response.status_code
result = response.text

print(result)
'''
#print(result)

import argparse
import pandas as pd
import requests
import json

# Obtain the api key that was passed in from the command line
parser = argparse.ArgumentParser(description='Sample V4')
parser.add_argument('--api-key', type=str, default='')
args = parser.parse_args()


# An api key is emailed to you when you sign up to a plan
# Get a free API key at https://api.the-odds-api.com/
API_KEY = '2df36f9a31375b56518afeeb68db23bc'

SPORT = 'basketball_nba' # use the sport_key from the /sports endpoint below, or use 'upcoming' to see the next 8 games across all sports

REGIONS = 'us' # uk | us | eu | au. Multiple can be specified if comma delimited

MARKETS = 'h2h,spreads' # h2h | spreads | totals. Multiple can be specified if comma delimited

ODDS_FORMAT = 'decimal' # decimal | american

DATE_FORMAT = 'iso' # iso | unix

DATE = '2023-12-09T12:00:00Z'

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
# First get a list of in-season sports
#   The sport 'key' from the response can be used to get odds in the next request
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

sports_response = requests.get('https://api.the-odds-api.com/v4/sports', params={
    'api_key': API_KEY
})


if sports_response.status_code != 200:
    print(f'Failed to get sports: status_code {sports_response.status_code}, response body {sports_response.text}')

else:
    print('available')



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
# Now get a list of live & upcoming games for the sport you want, along with odds for different bookmakers
# This will deduct from the usage quota
# The usage quota cost = [number of markets specified] x [number of regions specified]
# For examples of usage quota costs, see https://the-odds-api.com/liveapi/guides/v4/#usage-quota-costs
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

odds_response = requests.get(f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds', params={
    'api_key': API_KEY,
    'regions': REGIONS,
    'markets': MARKETS,
    'oddsFormat': ODDS_FORMAT,
    'dateFormat': DATE_FORMAT,
    'date':DATE,
})

if odds_response.status_code != 200:
    print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')

else:
    odds_json = odds_response.json()

    # JSON 데이터를 DataFrame으로 변환
    odds_df = pd.json_normalize(odds_json)
    
    # CSV 파일로 저장
    odds_df.to_csv('odds_data_test.csv', index=False)

    json_file_path = 'odds.json'

    # Open the file in write mode and use json.dump to write the data
    with open(json_file_path, 'w') as json_file:
        json.dump(odds_json, json_file, indent=2)
    # Check the usage quota
    #print('Remaining requests', odds_response.headers['x-requests-remaining'])
    #print('Used requests', odds_response.headers['x-requests-used'])
    #print('Number of events:', len(odds_json))
    #print(odds_json)

import csv

# 파일 경로
json_file_path = '/Users/bagjaeyun/Desktop/basketball_reference_webcrawler-master/odds.json'
csv_file_path = '/Users/bagjaeyun/Desktop/basketball_reference_webcrawler-master/todayodds.csv'

# JSON 파일 읽기
with open(json_file_path) as file:
    datas = json.load(file)

# CSV 파일 쓰기
with open(csv_file_path, mode='w', newline='') as csv_file:
    fieldnames = ['name', 'price', 'point','win_prob']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # CSV 파일의 헤더 작성
    writer.writeheader()

    # JSON 데이터에서 필요한 정보 추출하여 CSV 파일에 쓰기
    for k in datas:
        for i in range(len(k['bookmakers'])):
            if k['bookmakers'][i]['key'] == 'fanduel':
                outcomes = k['bookmakers'][i]['markets'][1]['outcomes']
                for outcome in outcomes:
                    writer.writerow({
                        'name': outcome['name'],
                        'price': outcome['price'],
                        'point': outcome.get('point', None),  # 'point' 키가 없으면 None으로 기본값 설정
                        'win_prob': 1/outcome['price']
                    })

    
# 오늘 경기 배당률
