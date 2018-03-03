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
    print(data[0])
    return data

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
    return [[
        "Date", "HomeTeam", "AwayTeam", "Home Goals",
        "Away Goals", "Result", "Home Shots",
        "Away Shots", "Home on Target", "Away on Target",
        "Home Corners", "Away Corners"
    ], [1,2,3,4,5,6,11,12,13,14,16,17]]