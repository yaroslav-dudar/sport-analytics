#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import time

from terminaltables import SingleTable

from statistics import TeamStats
from utils import colorize

class StatsReport:

    def __init__(self, dataset, amount_games=5, filter_by='all', sort_by='avg_score'):
        self.dataset = dataset
        self.amount_games = amount_games
        self.filter_by = filter_by
        self.sort_by = sort_by

    def get_report_fields(self, team_stat):
        """
            Dynamically create report fields.
            Alsways start with Team name and sort_by field
        """
        report_column_names = ["Team", self.sort_by]
        for stat in team_stat[1]:
            if stat != self.sort_by:
                report_column_names.append(stat)

        return report_column_names

    def print(self):
        stats = self.collect_stats()
        try:
            stats = sorted(stats.items(), key=lambda t: t[1][self.sort_by], reverse=True)
        except KeyError:
            raise ValueError('Invalid sort_by value')

        self.colorize(stats)
        report_column_names = self.get_report_fields(stats[0])

        stats_list = []
        for t in stats:
            team_stats = [t[0]] + [t[1][key] for key in report_column_names[1:]]
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
            stats[t]['goal_diff'] = round(team_stats.goal_diff(), 2)
            stats[t]['total>2.5'] = team_stats.total_over_2_5()
            stats[t]['total>3.5'] = team_stats.total_over_3_5()

        return stats

    def colorize(self, stats):
        colors_list = ['red', 'yellow', 'green']

        color_ranges = {}
        for stat in stats[0][1]:
            vals = [s[1][stat] for s in stats]
            min_val, max_val = min(vals), max(vals)
            step = (max_val - min_val) / len(colors_list)
            intervals = np.arange(min_val, max_val+0.000001, step)
            
            color_ranges[stat] = [
                (round(intervals[i[0]],2), round(intervals[i[0]+1],2))
                for i,_ in np.ndenumerate(intervals[:len(colors_list)])
            ]

        for s in stats:
            for stat in s[1]:
                for i, interval in enumerate(color_ranges[stat]):
                    if interval[0] <= s[1][stat] <= interval[1]:
                        color_i = i

                s[1][stat] = colorize(s[1][stat], colors_list[color_i])
