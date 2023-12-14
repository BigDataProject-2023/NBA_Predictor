from pyspark.sql import SparkSession
from pyspark.sql.functions import col

if __name__ == "__main__":
    spark = SparkSession.builder.appName("NBA_Season_Join").getOrCreate()
    spark.conf.set("spark.sql.crossJoin.enabled", "true")

    def preProcessing(year):
        spark = SparkSession.builder.appName("NBA_Data_PreProcessing").getOrCreate()

        # 데이터 읽기
        odds_data = spark.read.load(
            f"hdfs:///user/maria_dev/NBA_Predictor/odds_data/odds_data_{year-2001}{year-2000}.csv",
            format="csv",
            sep=",",
            inferSchema=True,
            header=True,
        )
        season_data = spark.read.load(
            f"hdfs:///user/maria_dev/NBA_Predictor/dataPreProcessing/season_join_data/season_{year}.csv",
            format="csv",
            sep=",",
            inferSchema=True,
            header=True,
        )

        # 날짜 형식 변환
        season_data = season_data.withColumn("date", col("date").cast("date"))

        # 데이터 조인 및 필요없는 열 삭제
        result_data = odds_data.join(
            season_data,
            (odds_data["Date"] == season_data["date"])
            & (odds_data["Home"] == season_data["home_team"])
            & (odds_data["Away"] == season_data["away_team"]),
            "inner",
        ).drop("date", "home_team", "away_team")

        # 조인된 데이터를 저장
        result_data.write.mode("overwrite").csv(
            f"hdfs:///user/maria_dev/NBA_Predictor/dataPreProcessing/joined_data/nba_{year-2001}{year-2000}"
        )

        spark.stop()

    for year in range(2019, 2025):
        preProcessing(year)
