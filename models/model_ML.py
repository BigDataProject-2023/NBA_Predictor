import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split

data = pd.read_csv('/Users/bagjaeyun/Desktop/basketball_reference_webcrawler-master/merged_data/merged_data_2223.csv')

# 'home_score - away_score'가 0보다 크면 1, 아니면 0으로 하는 'Home-Team-Win' 생성
data['Home-Team-Win'] = (data['home_score'] - data['away_score'] > 0).astype(int)

print(data.head())
# 선택된 특성 (예시로 일부 특성만 선택)
selected_features = ['Points', 'Win_Margin', 'Days_Rest_Home', 'Days_Rest_Away', 'Home_Prob', 'Away_Prob', 'Home_Odds', 'Away_Odds']

print(data[selected_features])

# 선택된 특성 및 목표 변수 설정
X = data[selected_features].values
y = data['Home-Team-Win'].values

# 데이터 정규화
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 학습 데이터와 테스트 데이터로 분리
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.1, random_state=1)

# 로지스틱 회귀 모델 초기화
model = LogisticRegression()

# 모델 학습
model.fit(X_train, y_train)

# 테스트 데이터에 대한 예측
y_pred = model.predict(X_test)

# 모델 성능 평가
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f"Acc: {accuracy}")
print(f"Classification report")
print(report)