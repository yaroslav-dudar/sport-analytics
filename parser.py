#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import os
import time

from operator import itemgetter
from collections import OrderedDict

from utils import colorize

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

def get_teams(data):
    return np.array(["{0} - {1}".format(game[2], game[3]) for game in data])

def get_goals(data):
    return np.array(["{0} - {1}".format(game[4], game[5]) for game in data])

def get_result(data):
    return data[:,6]

def get_total_shots(data):
    return np.array(["{0} - {1}".format(game[10], game[11]) for game in data])

def get_shots_on_target(data):
    return np.array(["{0} - {1}".format(game[12], game[13]) for game in data])

def get_corners(data):
    return np.array(["{0} - {1}".format(game[16], game[17]) for game in data])

def get_date(data):
    return data[:,1]

def get_form(data, games, count_games=5):
    """
        Calculate teams form for the last <count_games>
        win = 1 lose = 0 draw = 0.5
        result = sum(game_form) / count_games
    """
    home = games[:,[1,2]]
    away = games[:,[1,3]]

    dates = np.array([
        time.mktime(time.strptime(d, '%d/%m/%y'))  for d in data[:,1]
    ])

    home_scores = []
    for t in home:
        home_scores.append(get_team_score(t, data, dates, count_games))

    away_scores = []
    for t in away:
        away_scores.append(get_team_score(t, data, dates, count_games))

    result = []
    for i,_ in enumerate(home_scores):
        result.append("{0} - {1}".format(home_scores[i], away_scores[i]))
    return result

def get_team_score(game, data, dates, count_games):
    game_date = time.mktime(time.strptime(game[0], '%d/%m/%y'))
    game_team = game[1]

    indexes = dates < game_date
    prev_data = data[indexes]

    # precondition: games already sorted by date
    team_games = prev_data[(game_team==prev_data[:,2]) |
        (game_team==prev_data[:,3])][-count_games:]

    score = 0
    for g in team_games:
        if g[2] == game_team:
            if g[6] == 'H':
                score += 1
        elif g[3] == game_team:
            if g[6] == 'A':
                score += 1

        if g[6] == 'D':
            score += 0.5

    return score/count_games

def get_postition(data, games):
    home = games[:,[1,2]]
    away = games[:,[1,3]]

    dates = np.array([
        time.mktime(time.strptime(d, '%d/%m/%y'))  for d in data[:,1]
    ])

    home_pos = []
    for t in home:
        home_pos.append(get_team_postition(t, data, dates))

    away_pos = []
    for t in away:
        away_pos.append(get_team_postition(t, data, dates))

    result = []
    for i,_ in enumerate(home_pos):
        result.append("{0} - {1}".format(home_pos[i], away_pos[i]))
    return result


def get_team_postition(game, data, dates):
    game_date = time.mktime(time.strptime(game[0], '%d/%m/%y'))
    game_team = game[1]

    indexes = dates < game_date
    # all gemes before <game_date>
    prev_games = data[indexes]

    teams = get_all_teams(data)
    # report: [points, goal diff]
    report = {t: [0,0] for t in teams}

    for g in prev_games:
        h_points, a_points = report[g[2]][0], report[g[3]][0]
        if g[6] == 'H':
            h_points += 3

        if g[6] == 'A':
            a_points += 3

        if g[6] == 'D':
            h_points += 1
            a_points += 1

        report[g[2]][0] = h_points
        report[g[2]][1] = report[g[2]][1] + int(g[4])-int(g[5])

        report[g[3]][0] = a_points
        report[g[3]][1] = report[g[3]][1] + int(g[5])-int(g[4])

    sorted_report = sorted(report.items(), key=itemgetter(1), reverse=True)

    team_pos = next((i for i,t in enumerate(sorted_report) if t[0] == game_team), None)
    return team_pos+1


def get_home_team_stats(game):
    stats = game[[2,4,5,6,10,12]]

    points = 0
    if stats[3] == 'H':
        stats[3] = colorize('W')
        points = 3
    elif stats[3] == 'A':
        stats[3] = colorize('L', 'red')
    else:
        points = 1

    return np.append(stats, [points])

def get_away_team_stats(game):
    stats = game[[3,5,4,6,11,13]]

    points = 0
    if stats[3] == 'H':
        stats[3] = colorize('L', 'red')
    elif stats[3] == 'A':
        stats[3] = colorize('W')
        points = 3
    else:
        points = 1

    return np.append(stats, [points])

def get_all_teams(data):
    return list(np.unique(np.append(data[:, 2], data[:,3])))
