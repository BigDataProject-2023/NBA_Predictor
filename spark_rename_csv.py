import subprocess

# HDFS 경로 설정
hdfs_spark_directory = (
    "/user/maria_dev/NBA_Predictor/dataPreProcessing/season_join_data"
)

# 시즌별 디렉토리 경로 리스트
directories = [
    "season_2019",
    "season_2020",
    "season_2021",
    "season_2022",
    "season_2023",
    "season_2024",
]

for directory in directories:
    hdfs_files = subprocess.Popen(
        ["hadoop", "fs", "-ls", f"{hdfs_spark_directory}/{directory}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = hdfs_files.communicate()

    # 파일 경로 추출
    file_paths = [
        line.split()[-1] for line in out.splitlines()[1:] if line.startswith(b"-")
    ]

    for file_path in file_paths:
        if file_path.decode().startswith(f"{hdfs_spark_directory}/{directory}/part-"):
            file_name = file_path.decode().split("/")[-1]
            new_file_name = f"{directory}.csv"
            new_file_path = f"{hdfs_spark_directory}/{new_file_name}"

            rename_in_hdfs = subprocess.Popen(
                ["hadoop", "fs", "-mv", file_path.decode(), new_file_path]
            )
