import pandas as pd

# CSV 파일 경로
csv_file_path = '/Users/bagjaeyun/Desktop/basketball_reference_webcrawler-master/todayodds.csv'

# CSV 파일 읽어오기
df = pd.read_csv(csv_file_path)

# 'home'와 'away' 컬럼 추가
#df['home'] = df[df.index % 2 == 0]['name'].reset_index(drop=True)
#df['away'] = df[df.index % 2 != 0]['name'].reset_index(drop=True)

# 필요 없는 컬럼 제거
#df.drop(columns=['name'], inplace=True)

# 'home' 팀과 'away' 팀의 데이터를 같은 행에 합치기
merged_df = pd.concat([df[df.index % 2 == 0].reset_index(drop=True), df[df.index % 2 != 0].reset_index(drop=True)], axis=1)

# CSV 파일로 저장
output_csv_file_path = '/Users/bagjaeyun/Desktop/basketball_reference_webcrawler-master/todayodds_combined.csv'
merged_df.to_csv(output_csv_file_path, index=False)

# 열 이름 변경
merged_df.columns = ['home_team', 'home_price', 'home_point', 'home_win_prob',
              'away_team', 'away_price', 'away_point', 'away_win_prob']

# CSV 파일로 저장
output_csv_file_path = '/Users/bagjaeyun/Desktop/basketball_reference_webcrawler-master/todayodds_combined.csv'
merged_df.to_csv(output_csv_file_path, index=False)
