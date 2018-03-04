#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from terminaltables import SingleTable

from statistics import TeamStats
from parser import (football_data_co_uk_parser,
    get_team_matches, get_teams, get_date, get_corners,
    get_goals, get_total_shots, get_shots_on_target, get_result)


def print_team_report(team, data, filter_by='all'):
    games_amount = 20
    games = get_team_matches(team, data, filter_by=filter_by)[-games_amount:]
    stats = TeamStats(team, games)

    report = list(np.stack((
        get_date(games),get_teams(games),
        get_goals(games), get_result(games),
        get_total_shots(games), get_shots_on_target(games),
        get_corners(games)
    )).T)
    report_column_names = [
        "Date", "Home vs Away", "Full Time Score",
        "Result", "Total Shots", "Shots on Target", "Corners"
    ]
    report.insert(0, report_column_names)

    view_table = SingleTable(report)

    print(view_table.table)
    print("Average goals scored: %s" % stats.avg_goals_score())
    print("Average goals conceded: %s" %stats.avg_goals_concede())
    print('='*30)
    print("Standard deviation goals scored: %s" % stats.std_goals_score())
    print("Standard deviation goals conceded: %s" %stats.std_goals_concede())
    print('='*30)
    print("Avg total shots: %s" % stats.avg_total_shots())
    print("Avg shots on target: %s" %stats.avg_shots_on_target())
    print('='*30)
    print("Avg opponent total shots: %s" % stats.avg_op_total_shots())
    print("Avg opponent shots on target: %s" %stats.avg_op_shots_on_target())


if __name__ == '__main__':  
    team_1 = 'Brighton'
    team_2 = 'Arsenal'

    data = football_data_co_uk_parser()
    print_team_report(team_2, data, filter_by='away')
