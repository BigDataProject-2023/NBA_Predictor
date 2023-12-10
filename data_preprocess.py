import pandas as pd

# 첫 번째 데이터셋
data_odds = pd.read_csv('/Users/bagjaeyun/Desktop/basketball_reference_webcrawler-master/odds_data_2324.csv')  # 파일명은 실제 파일명으로 변경

# 데이터 형식 변경 함수
def format_date_odds(date_str):
    month = date_str[8:10]
    day = date_str[10:]
    return f"{month}-{day}"

# 'Date' 열을 새로운 형식으로 변환
data_odds['Date'] = data_odds['Date'].apply(format_date_odds)

# 결과 확인
print("Data Odds Info:")
print(data_odds.tail())

# 두 번째 데이터셋
data_season = pd.read_csv('/Users/bagjaeyun/Desktop/basketball_reference_webcrawler-master/season_2024_basic.csv')  # 파일명은 실제 파일명으로 변경

# 데이터 형식 변경 함수
def format_date_season(date_str):
    month = date_str[5:7]
    day = date_str[8:10]
    return f"{month}-{day}"

# 'date' 열을 새로운 형식으로 변환
data_season['date'] = pd.to_datetime(data_season['date']).dt.strftime('%m-%d')

# 결과 확인
print("\nData Season Info:")
print(data_season.tail())


# 두 데이터셋을 날짜를 기준으로 합병
# 두 데이터셋을 'Date', 'Home', 'Away' 열을 기준으로 합병
merged_data = pd.merge(data_odds, data_season, left_on=['Date', 'Home', 'Away'], right_on=['date', 'home_team', 'away_team'], how='inner')

# 날짜 열 중복 제거 (하나는 기존의 'Date', 다른 하나는 합병 후의 'date')
merged_data.drop(['date', 'home_team', 'away_team'], axis=1, inplace=True)

# CSV 파일로 저장
merged_data.to_csv('/Users/bagjaeyun/Desktop/basketball_reference_webcrawler-master/merged_data.csv', index=False)

# 결과 확인
print(merged_data)
