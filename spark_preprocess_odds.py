from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when


def update_date_format(year):
    # Spark 세션 생성
    spark = SparkSession.builder.appName("Date_Format_Update").getOrCreate()

    # HDFS에서 데이터 읽기
    file_path = (
        f"hdfs:///user/maria_dev/NBA_Predictor/odds_data/odds_data_{year}{year+1}.csv"
    )
    odds_data = spark.read.csv(file_path, header=True)

    # Date 컬럼을 string 타입으로 변환하여 'mmdd' 부분 추출
    odds_data = odds_data.withColumn("Date", col("Date").substr(-4, 4))

    # 날짜 업데이트하기
    odds_data = odds_data.withColumn(
        "Date",
        when(
            col("Date") == "0101",
            f"20{year+1}-" + col("Date").substr(1, 2) + "-" + col("Date").substr(3, 2),
        ).otherwise(
            f"20{year}-" + col("Date").substr(1, 2) + "-" + col("Date").substr(3, 2)
        ),
    )
    if year == 18:
        odds_data = odds_data.withColumn(
            "Date",
            f"20{year+1}-" + col("Date").substr(1, 2) + "-" + col("Date").substr(3, 2),
        )

    # 새로운 날짜 형식으로 변환하여 HDFS에 저장
    odds_data.coalesce(1).write.csv(
        f"hdfs:///user/maria_dev/NBA_Predictor/odds_date_data/odds_{year}{year+1}.csv",
        header=True,
        mode="overwrite",
    )


for year in range(18, 24):
    update_date_format(year)
