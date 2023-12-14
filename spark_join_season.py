from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when

if __name__ == "__main__":
    spark = SparkSession.builder.appName("NBA_Season_Join").getOrCreate()
    spark.conf.set("spark.sql.crossJoin.enabled", "true")

    def merge_season_data(year):
        # CSV 파일에서 데이터 읽기
        basic_data = spark.read.load(
            f"hdfs:///user/maria_dev/NBA_Predictor/season_data/season_{year}_basic.csv",
            format="csv",
            sep=",",
            inferSchema=True,
            header=True,
        )
        basic_data = basic_data.drop("weekday", "attendance", "overtime", "remarks")
        basic_column = ["date", "home_team", "home_score", "away_team", "away_score"]

        starter_data = spark.read.load(
            f"hdfs:///user/maria_dev/NBA_Predictor/mapreduce/{year}_detailed_mapreduce_Starter.csv",
            format="csv",
            sep=",",
            inferSchema=True,
            header=True,
        )
        starter_data = starter_data.withColumnRenamed("date", "st_date")
        starter_data = starter_data.withColumnRenamed("team", "st_team")

        reserve_data = spark.read.load(
            f"hdfs:///user/maria_dev/NBA_Predictor/mapreduce/{year}_detailed_mapreduce_Reserve.csv",
            format="csv",
            sep=",",
            inferSchema=True,
            header=True,
        )
        reserve_data = reserve_data.withColumnRenamed("date", "rs_date")
        reserve_data = reserve_data.withColumnRenamed("team", "rs_team")

        # 날짜와 팀을 기준으로 조인
        merged_data = starter_data.join(
            reserve_data,
            (starter_data["st_date"] == reserve_data["rs_date"])
            & (starter_data["st_team"] == reserve_data["rs_team"]),
        ).drop("rs_date", "rs_team")

        # 조인을 위한 home_team, away_team을 기준으로 데이터 조인
        home_data = basic_data.join(
            merged_data,
            (basic_data["date"] == merged_data["st_date"])
            & (basic_data["home_team"] == merged_data["st_team"]),
        ).drop("st_team", "st_date")

        away_data = basic_data.join(
            merged_data,
            (basic_data["date"] == merged_data["st_date"])
            & (basic_data["away_team"] == merged_data["st_team"]),
        ).drop("st_team", "st_date")

        home_renamed = home_data.toDF(
            *(
                f"{col}_Home" if col not in basic_column else col
                for col in home_data.columns
            )
        )
        away_renamed = away_data.toDF(
            *(
                f"{col}_Away" if col not in basic_column else col
                for col in away_data.columns
            )
        ).drop("home_score", "away_team", "away_score")
        away_renamed = away_renamed.withColumnRenamed("date", "aw_date")
        away_renamed = away_renamed.withColumnRenamed("home_team", "aw_home_team")

        # 날짜와 team을 기준으로 조인하여 최종 결과 데이터 생성
        result_data = home_renamed.join(
            away_renamed,
            (home_renamed["date"] == away_renamed["aw_date"])
            & (home_renamed["home_team"] == away_renamed["aw_home_team"]),
        ).drop("aw_date", "aw_home_team")

        # 경기 결과를 새로운 컬럼에 저장
        result_data = result_data.withColumn(
            "game_result",
            when(col("home_score") - col("away_score") < 0, 0).otherwise(1),
        )

        result_data.coalesce(1).write.csv(
            f"hdfs:///user/maria_dev/NBA_Predictor/dataPreProcessing/season_join_data/season_{year}",
            header=True,
            mode="overwrite",
        )

    for year in range(2019, 2025):
        merge_season_data(year)
