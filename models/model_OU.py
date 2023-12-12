import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 데이터 불러오기
data = pd.read_csv('/Users/bagjaeyun/Desktop/basketball_reference_webcrawler-master/merged_data/merged_data_2223.csv')

# 'OU' 대신 'OU-Cover' 종속 변수 생성
data['OU-Cover'] = data.apply(lambda row: 2 if row['home_score'] + row['away_score'] == row['OU']
                               else (1 if row['home_score'] + row['away_score'] > row['OU'] else 0), axis=1)

# 종속 변수 설정
target = 'OU-Cover'

# 특성 선택
selected_features = ['Points', 'Win_Margin', 'Days_Rest_Home', 'Days_Rest_Away', 'Home_Prob', 'Away_Prob', 'Home_Odds', 'Away_Odds']

# 선택된 특성 및 목표 변수 설정
X = data[selected_features].values
y = data[target].values

# 데이터 정규화
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 학습 데이터와 테스트 데이터로 분리
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.1, random_state=42)

# 로지스틱 회귀 모델 초기화
model = LogisticRegression()

# 모델 학습
model.fit(X_train, y_train)

# 테스트 데이터에 대한 예측
y_pred = model.predict(X_test)

# 모델 성능 평가
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

# 결과 출력
print(f"Accuracy: {accuracy}")
print("Classification Report:")
print(report)