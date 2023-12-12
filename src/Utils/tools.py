from datetime import datetime
import re
import requests
import pandas as pd
from .Dictionaries import team_index_current

games_header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/57.0.2987.133 Safari/537.36',
    'Dnt': '1',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en',
    'origin': 'http://stats.nba.com',
    'Referer': 'https://github.com'
}

data_headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Host': 'stats.nba.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.nba.com/',
    'Connection': 'keep-alive'
}

def to_data_frame(data):
    try:
        data_list = data[0]
    except Exception as e:
        print(e)
        return pd.DataFrame(data={})
    return pd.DataFrame(data=data_list.get('rowSet'), columns=data_list.get('headers'))


def create_todays_games(input_list):
    games = []
    for game in input_list:
        home = game.get('h')
        away = game.get('v')
        home_team = home.get('tc') + ' ' + home.get('tn')
        away_team = away.get('tc') + ' ' + away.get('tn')
        games.append([home_team, away_team])
    return games


def get_date(date_string):
    year1,month,day = re.search(r'(\d+)-\d+-(\d\d)(\d\d)', date_string).groups()
    year = year1 if int(month) > 8 else int(year1) + 1
    return datetime.strptime(f"{year}-{month}-{day}", '%Y-%m-%d')

def get_json_data(url, save_to_csv=False, csv_filename=None):
    raw_data = requests.get(url, headers=data_headers)
    try:
        json_data = raw_data.json()
    except Exception as e:
        print(e)
        return {}

    if save_to_csv and csv_filename:
        save_json_to_csv(json_data, csv_filename)

    return json_data.get('resultSets')

def get_todays_games_json(url, save_to_csv=False, csv_filename=None):
    raw_data = requests.get(url, headers=games_header)
    json_data = raw_data.json()

    if save_to_csv and csv_filename:
        save_json_to_csv(json_data, csv_filename)

    return json_data.get('gs').get('g')

def create_todays_games_from_odds(input_dict, save_to_csv=False, csv_filename=None):
    games = []
    for game in input_dict.keys():
        home_team, away_team = game.split(":")
        if home_team not in team_index_current or away_team not in team_index_current:
            continue
        games.append([home_team, away_team])

    if save_to_csv and csv_filename:
        save_games_to_csv(games, csv_filename)

    return games

def save_json_to_csv(json_data, csv_filename):
    try:
        data_list = json_data[0]
    except Exception as e:
        print(e)
        return

    df = pd.DataFrame(data=data_list.get('rowSet'), columns=data_list.get('headers'))

    try:
        df.to_csv(csv_filename, index=False)
        print(f"Data saved to {csv_filename}")
    except Exception as e:
        print(e)

def save_games_to_csv(games, csv_filename):
    df = pd.DataFrame(games, columns=['Home Team', 'Away Team'])

    try:
        df.to_csv(csv_filename, index=False)
        print(f"Games saved to {csv_filename}")
    except Exception as e:
        print(e)