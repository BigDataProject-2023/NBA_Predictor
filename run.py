import argparse
from datetime import datetime, timedelta

import pandas as pd
import tensorflow as tf
from colorama import Fore, Style

from src.DataProviders.SbrOddsProvider import SbrOddsProvider
import xgb_runner
from src.Utils.Dictionaries import team_index_current
from src.Utils.tools import create_todays_games_from_odds, get_json_data, to_data_frame, get_todays_games_json, create_todays_games, save_games_to_csv, save_json_to_csv


todays_games_url = 'https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2023/scores/00_todays_scores.json'
data_url = 'https://stats.nba.com/stats/leaguedashteamstats?' \
           'Conference=&DateFrom=&DateTo=&Division=&GameScope=&' \
           'GameSegment=&LastNGames=0&LeagueID=00&Location=&' \
           'MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&' \
           'PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&' \
           'PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&' \
           'Season=2023-24&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&' \
           'StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision='


def createTodaysGames(games, odds):
    match_data = []
    todays_games_uo = []
    home_team_odds = []
    away_team_odds = []

    for game in games:
        home_team = game[0]
        away_team = game[1]
        if home_team not in team_index_current or away_team not in team_index_current:
            continue
        if odds is not None:
            game_odds = odds[home_team + ':' + away_team]
            todays_games_uo.append(game_odds['under_over_odds'])

            home_team_odds.append(game_odds[home_team]['money_line_odds'])
            away_team_odds.append(game_odds[away_team]['money_line_odds'])

        else:
            todays_games_uo.append(input(home_team + ' vs ' + away_team + ': '))

            home_team_odds.append(input(home_team + ' odds: '))
            away_team_odds.append(input(away_team + ' odds: '))

    return todays_games_uo,  home_team_odds, away_team_odds


def main():
    data = pd.read_csv('todayodds_combined.csv')

    odds = None
    if args.odds:
        odds = SbrOddsProvider(sportsbook=args.odds).get_odds()
        games = create_todays_games_from_odds(odds)

        #print(f"odds:{odds}")
        print(f"games:{games}")

        if len(games) == 0:
            print("No games found.")
            return
        if (games[0][0] + ':' + games[0][1]) not in list(odds.keys()):
            print(games[0][0] + ':' + games[0][1])
            print(Fore.RED,"--------------Games list not up to date for todays games!!! Scraping disabled until list is updated.--------------")
            print(Style.RESET_ALL)
            odds = None
        else:
            print(f"------------------{args.odds} odds data------------------")
            for g in odds.keys():
                home_team, away_team = g.split(":")
                print(f"{home_team} ({odds[g][home_team]['money_line_odds']}) @ {away_team} ({odds[g][away_team]['money_line_odds']})")
    

    todays_games_uo,  home_team_odds, away_team_odds = createTodaysGames(games,odds)
    
    if args.xgb:
        print("---------------XGBoost Model Predictions---------------")
        xgb_runner.xgb_runner(data, games, todays_games_uo,  home_team_odds, away_team_odds)
        print("-------------------------------------------------------")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Model to Run')
    parser.add_argument('-xgb', action='store_true', help='Run with XGBoost Model')
    parser.add_argument('-odds', help='Sportsbook to fetch from. (fanduel, draftkings, betmgm, pointsbet, caesars, wynn, bet_rivers_ny')
    args = parser.parse_args()
    main()
