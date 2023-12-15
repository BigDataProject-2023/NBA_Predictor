import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split
from tqdm import tqdm
from sklearn.preprocessing import StandardScaler

data = pd.read_csv('merged_data/merged_data_2223.csv')

# 'home_score - away_score'가 0보다 크면 1, 아니면 0으로 하는 'Home-Team-Win' 생성
data['Home-Team-Win'] = (data['home_score'] - data['away_score'] > 0).astype(int)

#Feature 다른 조합으로 생각해야함 => 지금은 확률로 확률을 예측하는 느낌
#원본 데이터의 FT, 3GT, Home_team, AVG_WIN 이런걸로 구성해야
#현재 사용하는 피처는 나중에 drop하고 prediction을 해야할 거 같음

# 선택된 특성 (예시로 일부 특성만 선택)
selected_features = ['Home_Prob', 'Away_Prob', 'Home_Odds', 'Away_Odds']

# 선택된 특성 및 목표 변수 설정
X = data[selected_features].values
y = data['Home-Team-Win'].values

# 데이터 정규화
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

acc_results = []

for x in tqdm(range(50)):
    # 학습 데이터와 테스트 데이터로 분리
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.1, random_state=1)

    # XGBoost 데이터 형식으로 변환
    train = xgb.DMatrix(X_train, label=y_train)
    test = xgb.DMatrix(X_test, label=y_test)

    # XGBoost 모델 초기화
    param = {
        'max_depth': 3,
        'eta': 0.01,
        'objective': 'binary:logistic'
    }
    epochs = 750
    y_pred = []
    model = xgb.train(param, train, epochs)

    # 테스트 데이터에 대한 예측
    predictions = model.predict(test)
    for z in predictions:
        y_pred.append(np.argmax(z))

    # 모델 성능 평가
    accuracy = round(accuracy_score(y_test, y_pred)*100,1)
    print(f"{accuracy}%")
    acc_results.append(accuracy)

    if accuracy == max(acc_results):
        model.save_model('XGBoost_{}%_ML.json'.format(accuracy))


report = classification_report(y_test, y_pred)
# 결과 출력
print(f"Accuracy: {accuracy}")
print("Classification Report:")
print(report)
