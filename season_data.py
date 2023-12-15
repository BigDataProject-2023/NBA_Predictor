import os
import random
import sys
import time
from datetime import datetime, timedelta
import re
import pandas as pd
from sbrscrape import Scoreboard
from tqdm import tqdm

sys.path.insert(1, os.path.join(sys.path[0], '../..'))
#from src.Utils.tools import get_date

def get_date(date_string):
    year1,month,day = re.search(r'(\d+)-\d+-(\d\d)(\d\d)', date_string).groups()
    year = year1 if int(month) > 8 else int(year1) + 1
    return datetime.strptime(f"{year}-{month}-{day}", '%Y-%m-%d')

year = ["2023", "2024"]
season = ["2023-24"]

month = [10, 11, 12, 1, 2, 3, 4, 5, 6]
days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]

begin_year_pointer = year[0]
end_year_pointer = year[0]
count = 0

sportsbook = 'fanduel'
df_data = []

# CSV 파일로 저장할 경로
csv_filepath = " "

for season1 in tqdm(season):
    teams_last_played = {}
    for month1 in tqdm(month):
        if month1 == 1:
            count += 1
            end_year_pointer = year[count]
        for day1 in tqdm(days):
            if month1 == 10 and day1 < 24:
                continue
            if month1 in [4, 6, 9, 11] and day1 > 30:
                continue
            if month1 == 2 and day1 > 28:
                continue
            # skip future games
            if datetime.now() < datetime(year=int(end_year_pointer), month=month1, day=day1):
                continue
            print(f"{end_year_pointer}-{month1:02}-{day1:02}")
            sb = Scoreboard(date=f"{end_year_pointer}-{month1:02}-{day1:02}")
            if not hasattr(sb, "games"):
                continue
            for game in sb.games:
                if game['home_team'] not in teams_last_played:
                    teams_last_played[game['home_team']] = get_date(f"{season1}-{month1:02}{day1:02}")
                    home_games_rested = timedelta(days=7)  # start of season, big number
                else:
                    current_date = get_date(f"{season1}-{month1:02}{day1:02}")
                    home_games_rested = current_date - teams_last_played[game['home_team']]
                    teams_last_played[game['home_team']] = current_date
                    # todo update row

                if game['away_team'] not in teams_last_played:
                    teams_last_played[game['away_team']] = get_date(f"{season1}-{month1:02}{day1:02}")
                    away_games_rested = timedelta(days=7)  # start of season, big number
                else:
                    current_date = get_date(f"{season1}-{month1:02}{day1:02}")
                    away_games_rested = current_date - teams_last_played[game['away_team']]
                    teams_last_played[game['away_team']] = current_date

                try:
                    df_data.append({
                        'Unnamed: 0': 0,
                        'Date': f"{season1}-{month1:02}{day1:02}",
                        'Home': game['home_team'],
                        'Away': game['away_team'],
                        'OU': game['total'][sportsbook],
                        'Spread': game['away_spread'][sportsbook],
                        'ML_Home': game['home_ml'][sportsbook],
                        'ML_Away': game['away_ml'][sportsbook],
                        'Points': game['away_score'] + game['home_score'],
                        'Win_Margin': game['home_score'] - game['away_score'],
                        'Days_Rest_Home': home_games_rested.days,
                        'Days_Rest_Away': away_games_rested.days
                    })
                except KeyError:
                    print(f"No {sportsbook} odds data found for game: {game}")
            time.sleep(random.randint(1, 3))
    begin_year_pointer = year[count]

    df = pd.DataFrame(df_data)

    # 홈 팀과 원정 팀의 배당률 계산 및 추가
    df['Home_Prob'] = 1 / (abs(df['ML_Home']) / 100)
    df['Away_Prob'] = 1 / (abs(df['ML_Away']) / 100)

    # 배당률 계산
    df['Home_Odds'] = 1 / df['Home_Prob']
    df['Away_Odds'] = 1 / df['Away_Prob']
    # CSV 파일로 저장
    df.to_csv(csv_filepath, index=False)
