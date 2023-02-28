from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamgamelog
from datetime import date, timedelta
import pandas as pd
import json


def get_team_id_abbrev(team_name):
    '''
    Returns the ID of the team designated by the abbreviation provided
    '''
    nba_teams = teams.get_teams()
    temp_team = [team for team in nba_teams if team['abbreviation'] == team_name][0]
    return temp_team['id']

def get_latest_game(teamID):
    '''
    Returns DataFrame of latest game
    '''
    teamGameLog = teamgamelog.TeamGameLog(team_id=teamID)
    return teamGameLog.get_data_frames()[0].iloc[0]


def did_play_when(teamID, days_ago):
    '''
    Returns True if the team played yesterday, False if not.
    Date/Time is formatted to be compatible with pandas, and then
    compared.
    '''
    teamGameLog = teamgamelog.TeamGameLog(team_id=teamID)
    latest_game_date = get_latest_game(teamID)['GAME_DATE']
    formatted_date = pd.to_datetime(latest_game_date)

    # Sourcery being a GOAT (!!!)
    return (formatted_date == pd.Timestamp(date.today()) - timedelta(days=days_ago))


def player_attribute_leader(column, df):
    '''
    Returns the player that was the attribute leader in a certain category
    '''
    returnString = ''
    columnMax = df[column].max()
    columnMaxIndex = df[column].idxmax()
    playerName = df.loc[columnMaxIndex, 'PLAYER_NAME']
    returnString += f'({column}) {playerName}: {str(columnMax)}'
    return returnString


def get_latest_game_ID(teamID):
    '''
    Returns the ID of the latest game
    '''
    teamGameLog = teamgamelog.TeamGameLog(team_id=teamID)
    latest_game = get_latest_game(teamID)
    return latest_game['Game_ID']


def get_team_color(abbreviation):
    '''
    Returns the color of the team
    '''
    with open('team_colors.json') as f:
        return json.load(f)[abbreviation]
