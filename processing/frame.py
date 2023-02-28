from nba_api.stats.endpoints import teamgamelog, boxscoretraditionalv2 as box_score, boxscoresummaryv2 as team_scoring
import numpy as np


def clean_df(df):
    '''
    Returns a cleaned DataFrame
    '''
    df = df.dropna()
    return df


def drop_columns(dropped_columns, df):
    '''
    Returns a DataFrame with the columns (in an array) dropped
    '''
    for column in dropped_columns:
        df = df.drop([column], axis='columns')
    return df


def convert_column_to_int(cleaned_columns, df):
    '''
    Returns a DataFrame with the columns (in an array) converted to int
    '''
    for column in cleaned_columns:
        df[[column]] = df[[column]].apply(np.int64)
    return df

# Returns the Team Summary Score (quarter summary) for a given gameID, cleans and formats the columns
def process_team_summary_score(gameID):

    # Get Team Scoring DataFrame
    df = team_scoring.BoxScoreSummaryV2(game_id=gameID).get_data_frames()[5]

    # Clean unwanted columns
    dropped_columns = ['GAME_DATE_EST', 'GAME_SEQUENCE', 'GAME_ID', 'TEAM_ID', 'TEAM_CITY_NAME', 'TEAM_NICKNAME', 'TEAM_WINS_LOSSES']
    df = drop_columns(dropped_columns, df)

    # Formatting, renaming
    df = df.loc[:, (df != 0).any(axis=0)]
    df.rename(columns={'PTS_QTR1': 'QTR1', 'PTS_QTR2': 'QTR2', 'PTS_QTR3': 'QTR3', 'PTS_QTR4': 'QTR4'}, inplace=True)
    df.rename(columns={'TEAM_ABBREVIATION': 'TEAM'}, inplace=True)

    return df

# Returns Team Box Score for a given gameID
def process_team_box_score(gameID):

    df = team_scoring.BoxScoreSummaryV2(game_id=gameID).get_data_frames()[1]

    dropped_columns = ['GAME_ID', 'TEAM_ID', 'TEAM_CITY', 'MIN', 'PF', 'PLUS_MINUS', 'TEAM_ABBREVIATION', 'FG_PCT', 'FG3_PCT', 'FT_PCT']
    df = drop_columns(dropped_columns, df)
    df.rename(columns={'TEAM_NAME': 'TEAM'}, inplace=True)

    return df

# Returns Player Detail Box Score: pass in gameID, abbreviation and showAll
def process_player_detail_box_score(gameID, abbreviation, showAll):
    df = box_score.BoxScoreTraditionalV2(game_id=gameID).get_data_frames()[0]

    dropped_columns = ['COMMENT', 'NICKNAME', 'TEAM_CITY', 'START_POSITION', 'GAME_ID', 'PLAYER_ID',
                    'TEAM_ID', 'PLUS_MINUS', 'OREB', 'DREB', 'FT_PCT', 'FG3_PCT', 'FG_PCT', 'PF']
    df = drop_columns(dropped_columns, df)
    df = clean_df(df)
    cleaned_columns = ['PTS', 'TO', 'BLK', 'STL', 'AST', 'REB', 'FTA', 'FTM', 'FG3A', 'FG3M', 'FGA', 'FGM']
    df = convert_column_to_int(cleaned_columns, df)

    if(showAll == False):
        df = df.loc[df['TEAM_ABBREVIATION'] == abbreviation]

    return df

