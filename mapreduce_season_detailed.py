from mrjob.job import MRJob
from mrjob.step import MRStep
import csv


class seasonDetailedMapReduce(MRJob):
    def steps(self):
        return [
            MRStep(
                mapper=self.mapper,
                reducer=self.reducer,
                # reducer_final=self.write_output,
            )
        ]

    def mapper(self, _, line):
        # CSV 파일에서 각 줄을 읽고 date, team, role을 키로, 나머지를 값으로 매핑
        row = next(csv.reader([line]))  # CSV 파싱
        # 첫 번째 줄인 경우 헤더이므로 건너뜀
        if row[0] != "date":
            key = (row[0], row[1], row[3])  # date, team, role을 튜플로 설정하여 키로 사용
            values = [
                float(x) if x else 0.0 for x in row[4:]
            ]  # 나머지 값들은 실수형으로 변환하여 값으로 사용
            yield key, values

    def reducer(self, key, values):
        # 키 별로 받은 값들을 평균을 계산하여 출력
        total = [0.0] * 21  # 평균을 계산할 값들의 총합을 저장할 리스트
        count = 0  # 값을 받은 횟수를 저장할 변수
        for val in values:
            total = [sum(x) for x in zip(total, val)]  # 값들을 합산
            count += 1  # 값을 받은 횟수 증가
        avg_values = [x / count for x in total]  # 평균 계산
        yield key, avg_values


if __name__ == "__main__":
    seasonDetailedMapReduce.run()

# python mapreduce_season_detailed.py  season_data/season_20xx_detailed.csv --output-dir mapreduce\20xx_detailed_mapreduce 으로 실행
