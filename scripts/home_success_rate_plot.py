#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

import numpy as np
import time
import os

from parser import (
    football_data_co_uk_parser, get_all_teams,
    get_team_matches, get_team_score, get_team_postition)


def collect(data):
    form_amount = 5

    # get all teams from data
    teams = get_all_teams(data)

    dates = np.array([
        time.mktime(time.strptime(d, '%d/%m/%y'))  for d in data[:,1]
    ])

    score = 0
    for team in teams:
        home_games = get_team_matches(team, data, 'home')
        tmp_score = 0

        for g in home_games:
            if (g[2] == team):
                if g[6] == 'H':
                    tmp_score += 1
                if g[6] == 'D':
                    tmp_score += 0.5
        
        score += tmp_score/len(home_games)

    return  time.strptime(data[0][1], '%d/%m/%y').tm_year, score/len(teams)


if __name__ == '__main__':
    success_rate, years = np.array([]), np.array([])
    
    files = os.listdir("./data/EPL")

    for f in files:
        data = football_data_co_uk_parser(_file=f, _dir='./data/EPL')
        x, y = collect(data)

        success_rate = np.append(success_rate, [x])
        years = np.append(years, [y])

    res = np.stack((success_rate, years)).T
    res = res[res[:,0].argsort()]
    
    plt.plot(res[:,0], res[:,1])
    plt.xlabel('Year')
    plt.ylabel('Home success rate')
    plt.show()
