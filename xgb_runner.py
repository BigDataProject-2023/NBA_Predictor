import numpy as np
import pandas as pd
import xgboost as xgb
from colorama import Fore, Style, init, deinit
from sklearn.preprocessing import StandardScaler

init()
xgb_ml = xgb.Booster()
xgb_ml.load_model('models/XGBoost_43.8%_ML.json')
#y = data['Home-Team-Win'].values => winning confidence for home teams'
xgb_uo = xgb.Booster()
xgb_uo.load_model('models/XGBoost_47.7%_OU.json')
#y = data['OU-cover'].values => OU rates

# features : 'Home_Prob', 'Away_Prob', 'Home_Odds', 'Away_Odds'

def xgb_runner(data, games, todays_games_uo,  home_team_odds, away_team_odds):
    
    #data column
    #[home_team,
    # home_price,
    # home_point,
    # home_win_prob,
    # away_team,
    # away_price,
    # away_point,
    # away_win_prob]
    
    ml_predictions_array = []

    data = pd.DataFrame(data)

        # 필요한 열만 선택하여 새로운 데이터프레임 생성
    new_df = data[['home_win_prob', 'away_win_prob', 'home_price', 'away_price']].copy()

    # 열 이름 변경
    new_df.columns = ['Home_Prob', 'Away_Prob', 'Home_Odds', 'Away_Odds']

    # 데이터 정규화
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(new_df)

    for row in data_scaled:
        ml_predictions_array.append(xgb_ml.predict(xgb.DMatrix(np.array([row]))))


    #frame_uo = frame_ml.copy()
    #frame_uo['OU'] = np.asarray(todays_games_uo)
    #data_uo = frame_uo.values
    #data_uo_scaled = scaler.transform(data_uo)

    ou_predictions_array = []

    for row in data_scaled:
        ou_predictions_array.append(xgb_uo.predict(xgb.DMatrix(np.array([row]))))

    count = 0
    for game in games:
        print(f"game : {game}")
        home_team = game[0]
        away_team = game[1]
        winner = int(np.argmax(ml_predictions_array[count]))
        under_over = int(np.argmax(ou_predictions_array[count]))
        winner_confidence = ml_predictions_array[count]
        un_confidence = ou_predictions_array[count]

        if winner_confidence >=0.5:
            winner_confidence = round(winner_confidence[0] * 100, 1)
            if under_over == 0:
                un_confidence = round(ou_predictions_array[count][0][0] * 100, 1)
                print(
                    Fore.GREEN + home_team + Style.RESET_ALL + Fore.CYAN + f" ({winner_confidence}%)" + Style.RESET_ALL + ' vs ' + Fore.RED + away_team + Style.RESET_ALL + ': ' +
                    Fore.MAGENTA + 'UNDER ' + Style.RESET_ALL  + str(todays_games_uo[count]) + Style.RESET_ALL + Fore.CYAN + f" ({un_confidence}%)" + Style.RESET_ALL)
            else:
                un_confidence = round(ou_predictions_array[count][0][1] * 100, 1)
                print(
                    Fore.GREEN + home_team + Style.RESET_ALL + Fore.CYAN + f" ({winner_confidence}%)" + Style.RESET_ALL + ' vs ' + Fore.RED + away_team + Style.RESET_ALL + ': ' +
                    Fore.BLUE + 'OVER ' + Style.RESET_ALL +  str(todays_games_uo[count])+ Style.RESET_ALL + Fore.CYAN + f" ({un_confidence}%)" + Style.RESET_ALL)
        else:
            winner_confidence = round(winner_confidence[0] * 100, 1)
            if under_over == 0:
                un_confidence = round(ou_predictions_array[count][0][0] * 100, 1)
                print(
                    Fore.RED + home_team + Style.RESET_ALL + ' vs ' + Fore.GREEN + away_team + Style.RESET_ALL + Fore.CYAN + f" ({winner_confidence}%)" + Style.RESET_ALL + ': ' +
                    Fore.MAGENTA + 'UNDER ' + Style.RESET_ALL + str(todays_games_uo[count]) + Style.RESET_ALL + Fore.CYAN + f" ({un_confidence}%)" + Style.RESET_ALL)
            else:
                un_confidence = round(ou_predictions_array[count][0][1] * 100, 1)
                print(
                    Fore.RED + home_team + Style.RESET_ALL + ' vs ' + Fore.GREEN + away_team + Style.RESET_ALL + Fore.CYAN + f" ({winner_confidence}%)" + Style.RESET_ALL + ': ' +
                    Fore.BLUE + 'OVER ' + Style.RESET_ALL + str(todays_games_uo[count]) + Style.RESET_ALL + Fore.CYAN + f" ({un_confidence}%)" + Style.RESET_ALL)
        count += 1

    #deinit()

# 여기에 데이터와 오늘의 경기 정보를 제공하여 함수를 호출합니다.
# 예시: xgb_runner(data, todays_games_uo, frame_ml, games, home_team_odds, away_team_odds, kelly_criterion)
