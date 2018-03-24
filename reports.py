
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from colorclass import Color
from terminaltables import SingleTable

from statistics import TeamStats
from parser import (get_team_matches, get_teams, get_date, get_corners,
    get_goals, get_total_shots, get_shots_on_target, get_result, get_form,
    get_all_teams, get_home_team_stats, get_away_team_stats, get_postition)

from utils import colorize_team_report, colorize

def print_team_report(team, data, games_amount, filter_by='all'):
    games = get_team_matches(team, data, filter_by=filter_by)[-games_amount:]
    stats = TeamStats(team, games)

    recent_form = get_form(data, games)
    team_positions = get_postition(data, games)

    report = list(np.stack((
        get_date(games),get_teams(games), get_goals(games), get_result(games),
        get_total_shots(games), get_shots_on_target(games),
        get_corners(games), recent_form, team_positions
    )).T)

    report_column_names = [
        "Date", "Home vs Away", "Full Time Score", "Result",
        "Total Shots", "Shots on Target", "Corners", "Recent Form",
        "League Position"
    ]

    report = colorize_team_report(report, team)
    report.insert(0, report_column_names)

    view_table = SingleTable(report)
    print(view_table.table)

    stats_table = SingleTable([
        ['', 'Avg Goals Scored', 'SD goals scored', 'Avg total shots', 'Avg shots on target', 'Recent success rate', 'Recent position'],
        [
            'Team', colorize(stats.avg_goals_score()), colorize(stats.std_goals_score()),
            colorize(stats.avg_total_shots()), colorize(stats.avg_shots_on_target()),
            colorize(stats.get_team_recent_form())
        ],
        [
            'Opponents', colorize(stats.avg_goals_concede(), 'red'), colorize(stats.std_goals_concede(), 'red'),
            colorize(stats.avg_op_total_shots(), 'red'),  colorize(stats.avg_op_shots_on_target(), 'red'),
            colorize(stats.op_form(recent_form), 'red'), colorize(stats.op_position(team_positions), 'red'),
        ],
    ])
    print(stats_table.table)


def print_tournament_report(data, games_amount,
        sort_by='points', filter_by='all'):
    
    teams = get_all_teams(data)
    sort_index = {'points': 1}
    # report structure
    # points, goals scored, goals cons, game results list
    report_column_names = [
       "Team", "Points", "Scored", "Cons", "Results",
    ]
    report = {t: [0,0,0,[]] for t in teams}

    for g in np.flip(data, axis=0):
        if filter_by == 'all':
            # take both teams from a game
            home = get_home_team_stats(g)
            away = get_away_team_stats(g)

            if home[0] in teams:
                add_team(report, home)

                if len(report[home[0]][3]) == games_amount:
                    teams.remove(home[0])

            if away[0] in teams:
                add_team(report, away)

                if len(report[away[0]][3]) == games_amount:
                    teams.remove(away[0])

        elif filter_by == 'home':
            home = get_home_team_stats(g)
            if home[0] in teams:
                add_team(report, home)

                if len(report[home[0]][3]) == games_amount:
                    teams.remove(home[0])

        elif filter_by == 'away':
            # take only away team
            away = get_away_team_stats(g)
            if away[0] in teams:
                add_team(report, away)

                if len(report[away[0]][3]) == games_amount:
                    teams.remove(away[0])
        else:
            raise Exception("filter_by is invalid: %s" % filter_by)

        if not teams:
            break

    # build final report
    result_report = [[team]+stats for team,stats in report.items()]
    for t in result_report:
        # result should print from old to new
        t[4].reverse()
        t[4] = ' '.join(t[4])

    result_report.sort(key=lambda x: x[1], reverse=True)

    result_report.insert(0, report_column_names)
    view_table = SingleTable(result_report)
    print(view_table.table)


def add_team(report, game):
    d = report[game[0]]
    d[0] += int(game[-1])
    d[1] += int(game[1])
    d[2] += int(game[2])
    d[3].append(game[3])
