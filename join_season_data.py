import pandas as pd
import os


def merge_season_data(year):
    # CSV 파일에서 데이터 읽기
    basic_data = pd.read_csv(f"season_data/season_{year}_basic.csv")
    basic_column = [
        "date",
        "weekday",
        "home_team",
        "home_score",
        "away_team",
        "away_score",
        "attendance",
        "overtime",
        "remarks",
    ]
    starter_data = pd.read_csv(
        f"mapreduce/season_detailed_mapreduce/{year}_detailed_mapreduce_Starter.csv"
    )
    reserve_data = pd.read_csv(
        f"mapreduce/season_detailed_mapreduce/{year}_detailed_mapreduce_Reserve.csv"
    )

    # 날짜와 팀을 기준으로 조인
    merged_data = starter_data.merge(
        reserve_data, on=["date", "team"], suffixes=("_reserve", "_starter")
    )

    # 조인을 위한 home_team, away_team을 기준으로 데이터 조인
    home_data = pd.merge(
        basic_data,
        merged_data,
        left_on=["date", "home_team"],
        right_on=["date", "team"],
    ).drop(columns=["team"])
    away_data = pd.merge(
        basic_data,
        merged_data,
        left_on=["date", "away_team"],
        right_on=["date", "team"],
    ).drop(columns=["team"])

    home_renamed = home_data.rename(
        columns={
            col: f"Home_{col}" for col in home_data.columns if col not in basic_column
        }
    )
    away_renamed = away_data.rename(
        columns={
            col: f"Away_{col}"
            for col in away_data.columns
            if col
            not in [
                "date",
                "weekday",
                "home_team",
                "home_score",
                "away_team",
                "away_score",
                "attendance",
                "overtime",
                "remarks",
            ]
        }
    )

    # 날짜와 team을 기준으로 조인하여 최종 결과 데이터 생성
    result_data = home_renamed.merge(away_renamed, on=basic_column)

    # 조인된 데이터를 CSV 파일로 저장
    os.makedirs("mapreduce/season_join_data", exist_ok=True)
    result_data.to_csv(f"mapreduce/season_join_data/season_{year}.csv", index=False)


for year in range(2019, 2025):
    merge_season_data(year)
