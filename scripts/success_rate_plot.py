#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

from parser import (
    football_data_co_uk_parser, get_all_teams,
    get_team_matches, get_team_score, get_team_postition)

import numpy as np
import time
import os

def collect(data):
    form_amount = 5
    # get all teams from data
    dates = np.array([
        time.mktime(time.strptime(d, '%d/%m/%y'))  for d in data[:,1]
    ])
    teams = get_all_teams(data)
    opponents_form, success_rate = [], []
    # skip portion of first games, because we can't calculate opponent form for them
    skip_games = int(len(teams) / 2 * form_amount)
    filtered = data[skip_games:]

    for team in teams:
        np.random.shuffle(filtered)

        team_games = get_team_matches(team, filtered)
        _tmp_form, _tmp_SR = 0, 0
        for i,g in enumerate(team_games[:5]):
            if (g[2] == team):
                opponent_team, team_filt, opponent_filt = g[3], 'home', 'away'
                if g[6] == 'H':
                    _tmp_SR += 1
            elif (g[3] == team):
                opponent_team, team_filt, opponent_filt = g[2], 'away', 'home'
                if g[6] == 'A':
                    _tmp_SR += 1
            if g[6] == 'D':
                _tmp_SR += 0.5

            _tmp_form += get_team_score([g[1], team], data, dates, form_amount, team_filt) -\
                get_team_score([g[1], opponent_team], data, dates, form_amount, opponent_filt)
                

        success_rate.append(_tmp_SR/5)
        opponents_form.append(_tmp_form/5)

    return success_rate, opponents_form


if __name__ == '__main__':
    success_rate, opponents_form = [], []
    
    files = os.listdir("./data/EPL")

    for f in files:
        data = football_data_co_uk_parser(_file=f, _dir='./data/EPL')
        x, y = collect(data)
        success_rate.extend(x)
        opponents_form.extend(y)

    print(np.corrcoef(success_rate, opponents_form))

    plt.plot(success_rate, opponents_form, 'ro')
    plt.xlabel('Success rate')
    plt.ylabel('Recent form diff')
    plt.show()
