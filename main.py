from nba_api.live.nba.endpoints import scoreboard
from datetime import date, timedelta, datetime
from hashlib import new
from matplotlib.pyplot import get
from nba_api.stats.endpoints import teamgamelog, boxscoretraditionalv2 as box_score, boxscoresummaryv2 as team_scoring

from nba_api.stats.static import teams, players
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
import plotly.graph_objects as go
import json

import smtplib
import imghdr
from email.message import EmailMessage

import frame
import player
import scoreboard
import teams

if __name__ == "__main__":

    # Get latest game's DataFrame, formatted
    abbreviation = 'CLE'


    # Team ID and latest game ID
    teamID = teams.get_team_id_abbrev(abbreviation)
    latest_game_ID = teams.get_latest_game_ID(teamID)

    # # Did the team play yesterday?
    # if teams.did_play_when(teamID, 1):
    #     boxScoreFrames = box_score.BoxScoreTraditionalV2(game_id=latest_game_ID)
    # else:
    #     print('No game yesterday')
    #     exit()

    boxScoreFrames = box_score.BoxScoreTraditionalV2(game_id=latest_game_ID)

    teamSummaryScore = frame.process_team_summary_score(latest_game_ID)
    # print(teamSummaryScore)

    playerDetailScore = frame.process_player_detail_box_score(latest_game_ID, abbreviation, True)
    print(playerDetailScore)






