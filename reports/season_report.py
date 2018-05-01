#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from terminaltables import SingleTable

from utils import colorize
from reports.team_report import TeamReport

class SeasonReport:

    def __init__(self, team, dataset):
        self.team = team
        self.dataset = dataset

        self.all_opponents = len(dataset.get_all_teams()) - 1
        self.all_games = self.all_opponents * 2

        self.table = self.dataset.get_league_table(prev_games=self.all_games)
        self.team_pos, self.team_data = next(
            ((pos, t) for pos,t in enumerate(self.table) if t[0] == self.team)
        )

        self.POINTS = 1

    def print(self):
        away_report = TeamReport(
            self.dataset, self.team,
            self.all_opponents, filter_by='away'
        )
        away_report.print()

        home_report = TeamReport(
            self.dataset, self.team,
            self.all_opponents, filter_by='home'
        )
        home_report.print()

        top_6, top_4,  = self.top6(), self.top4()
        top, relegation =  self.league_top(), self.relegation_zone()

        color = lambda p_diff: 'green' if p_diff <= 0 else 'red'
        top_6 = colorize(top_6, color(top_6))
        top_4 = colorize(top_4, color(top_4))
        top = colorize(top, color(top))
        relegation = colorize(relegation, color(relegation))

        meaningful_positions = SingleTable([
            ['League Position', 'To 1th', 'To 4th', 'To 6th', 'To Relegation zone'],
            [self.team_pos+1, top, top_4, top_6, relegation]
        ])
        print(meaningful_positions.table)

    def relegation_zone(self):
        """ distance to last 3 teams or to the safe zone """
        position = -4 if self.all_opponents - self.team_pos < 3 else -3
        points = self.table[position][self.POINTS]
        return points - self.team_data[self.POINTS]

    def top6(self):
        """ distance to first 6 teams or to the 7th """
        position = 6 if self.team_pos < 6 else 5
        points = self.table[position][self.POINTS]
        return points - self.team_data[self.POINTS]

    def top4(self):
        """ distance to first 4 teams or to the 5th """
        position = 4 if self.team_pos < 4 else 3
        points = self.table[position][self.POINTS]
        return points - self.team_data[self.POINTS]

    def league_top(self):
        """ distance to first place or to the 2th """
        position = 1 if self.team_pos == 0 else 0
        points = self.table[position][self.POINTS]
        return points - self.team_data[self.POINTS]
