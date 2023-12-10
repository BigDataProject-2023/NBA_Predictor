import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import matplotlib.pyplot as plt

# 데이터 불러오기
data = pd.read_csv('/Users/bagjaeyun/Desktop/basketball_reference_webcrawler-master/merged_data/merged_data_2223.csv')

# 종속 변수 설정
target = 'OU'  # 예측할 값 선택 (Spread, OU 등)

# 범주형 데이터에 대한 One-Hot Encoding
categorical_columns = ['Home', 'Away', 'weekday', 'overtime','remarks']
data_encoded = pd.get_dummies(data, columns=categorical_columns)

# 팀 이름에 대한 Label Encoding
#label_encoder = LabelEncoder()
#data_encoded['Home'] = label_encoder.fit_transform(data_encoded['Home'])
#data_encoded['Away'] = label_encoder.transform(data_encoded['Away'])

# 종속 변수 및 특성 설정
X = data_encoded.drop(['Date', target], axis=1)
y = data_encoded[target]

# 학습 데이터와 테스트 데이터로 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 선형 회귀 모델 초기화
model = LinearRegression()

# 모델 학습
model.fit(X_train, y_train)

# 테스트 데이터에 대한 예측
y_pred = model.predict(X_test)

# 모델 성능 평가
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse}')
print(f'R-squared: {r2}')

# 선택된 특성으로 모델 시각화 (실제값 vs 예측값)
plt.scatter(y_test, y_pred)
plt.xlabel('Actual Spread')
plt.ylabel('Predicted Spread')
plt.title('Actual vs Predicted Spread')
plt.show()
