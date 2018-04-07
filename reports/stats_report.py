#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import time

from terminaltables import SingleTable

from statistics import TeamStats

class StatsReport:

    def __init__(self, dataset, amount_games=5, filter_by='all', sort_by='avg_score'):
        self.dataset = dataset
        self.amount_games = amount_games
        self.filter_by = filter_by
        self.sort_by = sort_by

    def print(self):
        stats = self.collect_stats()
        try:
            stats = sorted(stats.items(), key=lambda t: t[1][self.sort_by], reverse=True)
        except KeyError:
            raise ValueError('Invalid sort_by value')

        report_column_names = [
            "Team", "Clean Sheet", "BTTS", "Avg Score", "Avg Concede", "Total>2.5", "Total>3.5"
        ]

        stats_list = []
        for t in stats:
            team_stats = [
                t[0], t[1]['clean_sheet'], t[1]['btts'], t[1]['avg_score'],
                t[1]['avg_concede'], t[1]['total>2.5'], t[1]['total>3.5']
            ]
            stats_list.append(team_stats)

        stats_list.insert(0, report_column_names)
        stats_report = SingleTable(stats_list)
        print(stats_report.table)

    def collect_stats(self):
        teams = self.dataset.get_all_teams()

        stats = {t: {} for t in teams}
        for t in teams:
            games = self.dataset.get_games(t, self.filter_by)[-self.amount_games:]
            team_stats = TeamStats(t, games)
            
            stats[t]['clean_sheet'] = team_stats.clean_sheet()
            stats[t]['btts'] = team_stats.btts()
            stats[t]['avg_score'] = team_stats.avg_goals_score()
            stats[t]['avg_concede'] = team_stats.avg_goals_concede()
            stats[t]['total>2.5'] = team_stats.total_over_2_5()
            stats[t]['total>3.5'] = team_stats.total_over_3_5()

        return stats
