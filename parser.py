#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import os

DATA_DIR = './data'

def football_data_co_uk_parser(_file='E0.csv'):
    """
        Key to results data:

        Div = League Division
        Date = Match Date (dd/mm/yy)
        HomeTeam = Home Team
        AwayTeam = Away Team
        FTHG and HG = Full Time Home Team Goals
        FTAG and AG = Full Time Away Team Goals
        FTR and Res = Full Time Result (H=Home Win, D=Draw, A=Away Win)
        HTHG = Half Time Home Team Goals
        HTAG = Half Time Away Team Goals
        HTR = Half Time Result (H=Home Win, D=Draw, A=Away Win)

        Match Statistics (where available)
        Attendance = Crowd Attendance
        Referee = Match Referee
        HS = Home Team Shots
        AS = Away Team Shots
        HST = Home Team Shots on Target
        AST = Away Team Shots on Target
        HHW = Home Team Hit Woodwork
        AHW = Away Team Hit Woodwork
        HC = Home Team Corners
        AC = Away Team Corners
        HF = Home Team Fouls Committed
        AF = Away Team Fouls Committed
        HFKC = Home Team Free Kicks Conceded
        AFKC = Away Team Free Kicks Conceded
        HO = Home Team Offsides
        AO = Away Team Offsides
        HY = Home Team Yellow Cards
        AY = Away Team Yellow Cards
        HR = Home Team Red Cards
        AR = Away Team Red Cards
        HBP = Home Team Bookings Points (10 = yellow, 25 = red)
        ABP = Away Team Bookings Points (10 = yellow, 25 = red)
    """

    data = np.genfromtxt(os.path.join(DATA_DIR, _file), delimiter=',', dtype=str)
    # some datasets don't have Referee column
    # so we need to remove it
    if 'Referee' in data[0]:
        data = np.delete(data, 10, 1)
    return data[1:]

def get_team_matches(team, data, filter_by='all'):
    """
        @filter_by:
            - all : get all team matches
            - home : get only home matches
            - away : get only away matches
    """
    if filter_by == 'all':
        condition = (team==data[:,2]) | (team==data[:,3])
    elif filter_by == 'home':
        condition = (team==data[:,2])
    elif filter_by == 'away':
        condition = (team==data[:,3])

    return data[condition]

def get_columns():
    return [1,[2,3],[4,5],6,[10,11],[12,13],[15,16]]

def get_teams(data):
    return np.array(["{0} - {1}".format(game[2], game[3]) for game in data])

def get_goals(data):
    return np.array(["{0} - {1}".format(game[4], game[5]) for game in data])

def get_result(data):
    return data[:,6]

def get_total_shots(data):
    return np.array(["{0} - {1}".format(game[10], game[11]) for game in data])

def get_shots_on_target(data):
    return np.array(["{0} - {1}".format(game[14], game[13]) for game in data])

def get_corners(data):
    return np.array(["{0} - {1}".format(game[15], game[16]) for game in data])

def get_date(data):
    return data[:,1]

def get_home_team_stats(game):
    stats = game[[2,4,5,6,10,12]]

    points = 0
    if stats[3] == 'H':
        stats[3] = 'W'
        points = 3
    elif stats[3] == 'A':
        stats[3] = 'L'
    else:
        points = 1

    return np.append(stats, [points])

def get_away_team_stats(game):
    stats = game[[3,5,4,6,11,13]]

    points = 0
    if stats[3] == 'H':
        stats[3] = 'L'
    elif stats[3] == 'A':
        stats[3] = 'W'
        points = 3
    else:
        points = 1

    return np.append(stats, [points])

def get_all_teams(data):
    return list(np.unique(np.append(data[:, 2], data[:,3])))
