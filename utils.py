#!/usr/bin/env python
# -*- coding: utf-8 -*-

from colorclass import Color
import numpy as np

def colorize(string, color='green'):
    return Color('{%s}%s{/%s}' % (color, string, color))

def colorize_team_report(report, team, color='green'):
    colorize_report = []

    for data in report:
        teams = data[1].split('-')
        colorize_report.append([data[0]])

        if teams[0].strip() == team:
            _team, _opponent = 0, 1
        elif teams[1].strip() == team:
            _team, _opponent = 1, 0
        else:
            raise Exception()

        for i in range(len(data)-1):
            stats = data[i+1].split('-')

            if len(stats) < 2:
                colorize_report[-1].insert(i+1, data[i+1])
                continue

            team_stat = colorize(stats[_team].strip(), color=color)
            opponent_stat = stats[_opponent].strip()
            if _team == 0:
                colorize_report[-1].insert(i+1, "{0} - {1}".format(team_stat, opponent_stat))
            elif _team == 1:
                colorize_report[-1].insert(i+1, "{0} - {1}".format(opponent_stat, team_stat))

    del report
    return colorize_report
