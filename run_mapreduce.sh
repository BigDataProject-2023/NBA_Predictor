declare -a years=("2019" "2020" "2021" "2022" "2023" "2024")

for year in "${years[@]}"
do
    python3.6 mapreduce_season_detailed.py \
        -r hadoop \
        --hadoop-streaming-jar /usr/hdp/3.0.1.0-187/hadoop-mapreduce/hadoop-streaming.jar \
        --python-bin /usr/bin/python3.6 \
        --output-dir hdfs:///user/maria_dev/NBA_Predictor/mapreduce/${year}_detailed_mapreduce \
        hdfs:///user/maria_dev/NBA_Predictor/season_data/season_${year}_detailed.csv
done
