#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

import numpy as np
import time
import os

from parser import (
    football_data_co_uk_parser, get_all_teams,
    get_team_matches, get_team_score, get_team_postition)

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def collect(data):
    form_amount = 5

    # get all teams from data
    teams = get_all_teams(data)

    dates = np.array([
        time.mktime(time.strptime(d, '%d/%m/%y'))  for d in data[:,1]
    ])

    less_25, more_25, less_35, more_35 = [0,0,0,0]
    for game in data:
        total = int(game[4]) + int(game[5])

        if total < 2.5:
            less_25 += 1
        if total < 3.5:
            less_35 += 1
        if total > 2.5:
            more_25 += 1
        if total > 3.5:
            more_35 += 1

    return time.strptime(data[0][1], '%d/%m/%y').tm_year, less_35/len(data)


if __name__ == '__main__':
    success_rate, years = np.array([]), np.array([])
    success_rate2, years2 = np.array([]), np.array([])

    files = os.listdir("./data/EPL")

    for f in files:
        data = football_data_co_uk_parser(_file=f, _dir='./data/EPL')
        x, y = collect(data)

        success_rate = np.append(success_rate, [x])
        years = np.append(years, [y])

    res = np.stack((success_rate, years)).T
    res = res[res[:,0].argsort()]

    files = os.listdir("./data/BL1")

    for f in files:
        data = football_data_co_uk_parser(_file=f, _dir='./data/BL1')
        x, y = collect(data)

        success_rate2 = np.append(success_rate2, [x])
        years2 = np.append(years2, [y])
    
    res2 = np.stack((success_rate2, years2)).T
    res2 = res2[res2[:,0].argsort()]
    print(res)
    print(res2)
    plt.plot(res[:,0], res[:,1])
    plt.plot(res2[:,0], res2[:,1])
    plt.xlabel('Year')
    plt.ylabel('Total < 3.5 %')

    plt.legend(['English PL', 'Bundesliga'], loc='upper left')
    plt.show()
