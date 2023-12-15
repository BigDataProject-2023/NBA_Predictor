import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm
# 데이터 불러오기
data = pd.read_csv('merged_data/merged_data_2223.csv')

ㅊ#Feature 다른 조합으로 생각해야함 => 지금은 확률로 확률을 예측하는 느낌
#원본 데이터의 FT, 3GT, Home_team, AVG_WIN 이런걸로 구성해야
#현재 사용하는 피처는 나중에 drop하고 prediction을 해야할 거 같음


# 'OU' 대신 'OU-Cover' 종속 변수 생성
data['OU-Cover'] = data.apply(lambda row: 2 if row['home_score'] + row['away_score'] == row['OU']
                               else (1 if row['home_score'] + row['away_score'] > row['OU'] else 0), axis=1)

# 종속 변수 설정
target = 'OU-Cover'

# 특성 선택
selected_features = ['Home_Prob', 'Away_Prob', 'Home_Odds', 'Away_Odds']

# 선택된 특성 및 목표 변수 설정
X = data[selected_features].values
y = data[target].values

# 데이터 정규화
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

acc_results = []
for x in tqdm(range(50)):
    
    # 학습 데이터와 테스트 데이터로 분리
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.1, random_state=42)

    # XGBoost 데이터 형식으로 변환
    train = xgb.DMatrix(X_train, label=y_train)
    test = xgb.DMatrix(X_test)

    # XGBoost 모델 초기화
    param = {
        'max_depth': 20,
        'eta': 0.05,
        'objective': 'multi:softprob',
        'num_class': 3
    }
    epochs = 750

    model = xgb.train(param, train, epochs)

    # 테스트 데이터에 대한 예측
    predictions = model.predict(test)
    y_pred = [np.argmax(z) for z in predictions]

    # 모델 성능 평가
    accuracy = round(accuracy_score(y_test, y_pred)*100, 1)
    print(f"{accuracy}%")
    acc_results.append(accuracy)
    
    if accuracy == max(acc_results):
        model.save_model('XGBoost_{}%_OU.json'.format(accuracy))

report = classification_report(y_test, y_pred)
# 결과 출력
print(f"Accuracy: {accuracy}")
print("Classification Report:")
print(report)
