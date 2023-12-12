# 실행방법 :
# python3.6 data_preProcessing.py -r hadoop  --hadoop-streaming-jar /usr/hdp/3.0.1.0-187/hadoop-mapreduce/hadoop-streaming.jar  --python-bin /usr/bin/python3.6# hadoop fs -copyFromLocal mapreduce/season_join_data /user/maria_dev/NBA_Predictor/mapreduce/
# hadoop fs -copyFromLocal merge_all_data /user/maria_dev/NBA_Predictor/

import pandas as pd
import os


def preProcessing(year):
    odds_data = pd.read_csv(f"odds_data\odds_data_{year-2001}{year-2000}.csv")
    season_data = pd.read_csv(f"mapreduce\season_join_data\season_{year}.csv")

    # 날짜 형식 변환 함수 정의
    def format_date_odds(date_str):
        month = date_str[8:10]
        day = date_str[10:]
        return f"{month}-{day}"

    # 'Date' 열 형식 변환
    odds_data["Date"] = odds_data["Date"].apply(format_date_odds)

    # 데이터 형식 변경 함수
    def format_date_season(date_str):
        month = date_str[5:7]
        day = date_str[8:10]
        return f"{month}-{day}"

    # 'date' 열 형식 변환
    season_data["date"] = pd.to_datetime(season_data["date"]).dt.strftime("%m-%d")

    # 데이터 조인 및 필요없는 열 삭제
    result_data = pd.merge(
        odds_data,
        season_data,
        left_on=["Date", "Home", "Away"],
        right_on=["date", "home_team", "away_team"],
    ).drop(["date", "home_team", "away_team"], axis=1)

    # 조인된 데이터를 CSV 파일로 저장
    result_data.to_csv(f"merge_all_data/nba_{year-2001}{year-2000}.csv", index=False)


for year in range(2019, 2025):
    preProcessing(year)
