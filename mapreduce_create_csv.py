# 실행방법 :
# python3.6 mapreduce_create_csv.py  -r hadoop  --hadoop-streaming-jar /usr/hdp/3.0.1.0-187/hadoop-mapreduce/hadoop-streaming.jar  --python-bin /usr/bin/python3.6

import subprocess
import pandas as pd
import csv
from io import StringIO

# HDFS 경로 설정
hdfs_mapreduce_directory = "/user/maria_dev/NBA_Predictor/mapreduce"

# 시즌별 디렉토리 경로 리스트
directories = [
    "2019_detailed_mapreduce",
    "2020_detailed_mapreduce",
    "2021_detailed_mapreduce",
    "2022_detailed_mapreduce",
    "2023_detailed_mapreduce",
    "2024_detailed_mapreduce",
]

for directory in directories:
    # 모든 데이터를 저장할 리스트
    all_data = []

    hdfs_files = subprocess.Popen(
        ["hadoop", "fs", "-ls", f"{hdfs_mapreduce_directory}/{directory}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = hdfs_files.communicate()

    # 파일 경로 추출
    file_paths = [
        line.split()[-1] for line in out.splitlines()[1:] if line.startswith(b"-")
    ]

    for file_path in file_paths:
        if file_path.decode().startswith(
            f"{hdfs_mapreduce_directory}/{directory}/part-"
        ):
            # HDFS에서 파일 읽기
            hdfs_content = subprocess.Popen(
                ["hadoop", "fs", "-cat", file_path.decode()],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            content_out, content_err = hdfs_content.communicate()

            # 데이터 가공 (바이트 스트림을 디코딩하여 문자열로 변환)
            lines = content_out.decode().splitlines()
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
        role_filename = f"{directory}_{role}.csv"
        role_df = role_df.drop(columns="role")  # Role 열 제거

        # CSV 파일로 저장하여 HDFS에 올리기
        csv_buffer = StringIO()
        role_df.to_csv(csv_buffer, index=False, quoting=csv.QUOTE_NONE)
        csv_buffer.seek(0)

        hdfs_file_path = f"{hdfs_mapreduce_directory}/{role_filename}"
        # HDFS에 데이터 저장
        put_to_hdfs = subprocess.Popen(
            ["hadoop", "fs", "-put", "-", hdfs_file_path],
            stdin=subprocess.PIPE,
        )
        put_to_hdfs.communicate(input=csv_buffer.getvalue().encode())
