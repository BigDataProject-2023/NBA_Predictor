from pyspark.sql import SparkSession
from pyspark.sql.functions import col


def merge_season_data():
    # SparkSession 생성
    spark = SparkSession.builder.appName("MergeData").getOrCreate()

    # HDFS 경로 설정
    hdfs_directory = "/user/maria_dev/NBA_Predictor/dataPreProcessing/joined_data/"
    hdfs_output_file = "/user/maria_dev/NBA_Predictor/dataPreProcessing/nba_19to24.csv"

    # HDFS의 CSV 파일을 읽어서 DataFrame으로 변환
    df = spark.read.option("header", "true").csv(hdfs_directory + "*.csv")

    # 통합된 데이터를 CSV 파일로 HDFS에 저장
    df.write.mode("overwrite").csv(hdfs_output_file)

    # SparkSession 종료
    spark.stop()


merge_season_data()
