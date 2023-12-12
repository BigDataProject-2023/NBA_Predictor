# 실행방법 :
# python3.6 mapreduce_create_csv.py  -r hadoop  --hadoop-streaming-jar /usr/hdp/3.0.1.0-187/hadoop-mapreduce/hadoop-streaming.jar  --python-bin /usr/bin/python3.6
# hadoop fs -copyFromLocal mapreduce/season_detailed_mapreduce /user/maria_dev/NBA_Predictor/mapreduce/

import pandas as pd
import csv
import os

# 현재 및 대상 디렉토리 경로 설정
current_directory = os.path.dirname(os.path.abspath(__file__))
mapreduce_directory = os.path.join(current_directory, "mapreduce")
new_directory = os.path.join(mapreduce_directory, "season_detailed_mapreduce")

# 시즌별 디렉토리 경로 리스트
directories = [
    os.path.join(mapreduce_directory, "2019_detailed_mapreduce"),
    os.path.join(mapreduce_directory, "2020_detailed_mapreduce"),
    os.path.join(mapreduce_directory, "2021_detailed_mapreduce"),
    os.path.join(mapreduce_directory, "2022_detailed_mapreduce"),
    os.path.join(mapreduce_directory, "2023_detailed_mapreduce"),
    os.path.join(mapreduce_directory, "2024_detailed_mapreduce"),
]

for directory in directories:
    # 모든 데이터를 저장할 리스트
    all_data = []

    # 디렉토리 내 파일들을 찾아서 순회
    for filename in os.listdir(directory):
        if filename.startswith("part-"):
            file_path = os.path.join(directory, filename)
            with open(file_path, "r") as file:
                lines = file.readlines()

            # 데이터 가공
            data = []
            for line in lines:
                parts = line.split("\t")
                date = parts[0].strip("[]").split(", ")[0].replace('"', "")
                team = parts[0].strip("[]").split(", ")[1].replace('"', "")
                role = parts[0].strip("[]").split(", ")[2].replace('"', "")
                team = team.split(" Basic")[0]
                stats = eval(parts[1])
                row = [date, team, role] + stats
                data.append(row)

            # 리스트에 데이터 추가
            all_data.extend(data)

    # 데이터를 pandas DataFrame으로 변환
    columns = [
        "date",
        "team",
        "role",
        "MP",
        "FG",
        "FGA",
        "FG_PCT",
        "FG3",
        "FG3A",
        "FG3_PCT",
        "FT",
        "FTA",
        "FT_PCT",
        "ORB",
        "DRB",
        "TRB",
        "AST",
        "STL",
        "BLK",
        "TOV",
        "PF",
        "PTS",
        "PLUS_MINUS",
    ]
    df = pd.DataFrame(all_data, columns=columns)

    # Role에 따라 파일 저장
    for role in df["role"].unique():
        role_df = df[df["role"] == role]
        role_prefix = f"{role}_"
        role_df.columns = [
            f"{role_prefix}{col}" if col not in ["date", "team", "role"] else col
            for col in role_df.columns
        ]
        role_filename = f"{os.path.basename(directory)}_{role}.csv"
        role_df = role_df.drop(columns="role")  # Role 열 제거
        role_file_path = os.path.join(new_directory, role_filename)
        role_df.to_csv(role_file_path, index=False, quoting=csv.QUOTE_NONE)
