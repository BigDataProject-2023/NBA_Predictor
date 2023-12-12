import numpy as np
import pandas as pd
import xgboost as xgb
from colorama import Fore, Style, init, deinit
import Expected_Value
import Kelly_Criterion as kc
from sklearn.preprocessing import StandardScaler

init()
xgb_ml = xgb.Booster()
xgb_ml.load_model('/Users/bagjaeyun/Desktop/basketball_reference_webcrawler-master/models/XGBoost_43.8%_ML.json')
#y = data['Home-Team-Win'].values => winning confidence for home teams'
xgb_uo = xgb.Booster()
xgb_uo.load_model('/Users/bagjaeyun/Desktop/basketball_reference_webcrawler-master/models/XGBoost_47.7%_OU.json')
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
'''
    if kelly_criterion:
        print("------------Expected Value & Kelly Criterion-----------")
    else:
        print("---------------------Expected Value--------------------")
    count = 0
    for game in games:
        home_team = game[0]
        away_team = game[1]
        ev_home = ev_away = 0
        if home_team_odds[count] and away_team_odds[count]:
            ev_home = float(Expected_Value.expected_value(ml_predictions_array[count][0][1], int(home_team_odds[count])))
            ev_away = float(Expected_Value.expected_value(ml_predictions_array[count][0][0], int(away_team_odds[count])))
        expected_value_colors = {'home_color': Fore.GREEN if ev_home > 0 else Fore.RED,
                        'away_color': Fore.GREEN if ev_away > 0 else Fore.RED}
        bankroll_descriptor = ' Fraction of Bankroll: '
        bankroll_fraction_home = bankroll_descriptor + str(kc.calculate_kelly_criterion(home_team_odds[count], ml_predictions_array[count][0][1])) + '%'
        bankroll_fraction_away = bankroll_descriptor + str(kc.calculate_kelly_criterion(away_team_odds[count], ml_predictions_array[count][0][0])) + '%'

        print(home_team + ' EV: ' + expected_value_colors['home_color'] + str(ev_home) + Style.RESET_ALL + (bankroll_fraction_home if kelly_criterion else ''))
        print(away_team + ' EV: ' + expected_value_colors['away_color'] + str(ev_away) + Style.RESET_ALL + (bankroll_fraction_away if kelly_criterion else ''))
        count += 1
'''
    #deinit()

# 여기에 데이터와 오늘의 경기 정보를 제공하여 함수를 호출합니다.
# 예시: xgb_runner(data, todays_games_uo, frame_ml, games, home_team_odds, away_team_odds, kelly_criterion)
