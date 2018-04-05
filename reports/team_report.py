#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import time

from terminaltables import SingleTable

from utils import colorize

class TeamReport:

    def __init__(self, dataset, team, amount_games=5, filter_by='all'):
        self.color = 'green'
        self.team = team
        self.filter_by = filter_by
        self.amount_games = amount_games

        self.dataset = dataset
        self.games = dataset.get_games(team, filter_by)[-amount_games:]

        self.opponents_form = []
        self.opponents_pos = []

        self.calculate_team_index()

    def print(self):
        form = self.get_form()
        position = self.get_position()

        report = list(np.stack((
            self.get_date(), self.get_teams(), self.get_goals(), self.get_result(),
            self.get_total_shots(), self.get_shots_on_target(),
            self.get_corners(), form, position
        )).T)

        report_column_names = [
            "Date", "Home vs Away", "Full Time Score", "Result",
            "Total Shots", "Shots on Target", "Corners", "Recent Form",
            "League Position"
        ]

        report = self.colorize_report(report)
        report.insert(0, report_column_names)

        view_table = SingleTable(report)
        print(view_table.table)

        self.print_statistics()

    def print_statistics(self):
        from statistics import TeamStats

        stats = TeamStats(self.team, self.games)

        date = time.strftime('%d/%m/%y', time.gmtime())
        team_recent_form = self.dataset.get_success_rate(
            date, self.team, self.amount_games, self.filter_by
        )
        opponents_recent_form = sum(self.opponents_form) / self.amount_games
        opponents_pos = sum(self.opponents_pos) / self.amount_games

        stats_table = SingleTable([
            ['', 'Avg Goals Scored', 'SD goals scored', 'Avg total shots', 'Avg shots on target', 'Recent success rate', 'Recent position'],
            [
                'Team', colorize(stats.avg_goals_score()), colorize(stats.std_goals_score()),
                colorize(stats.avg_total_shots()), colorize(stats.avg_shots_on_target()),
                colorize(team_recent_form)
            ],
            [
                'Opponents', colorize(stats.avg_goals_concede(), 'red'), colorize(stats.std_goals_concede(), 'red'),
                colorize(stats.avg_op_total_shots(), 'red'),  colorize(stats.avg_op_shots_on_target(), 'red'),
                colorize(opponents_recent_form, 'red'), colorize(opponents_pos, 'red'),
            ],
        ])
        print(stats_table.table)

        total_table = SingleTable([
            ['Over 2.5', 'Under 2.5', 'Over 3.5', 'Under 3.5', 'Clean sheet', 'BTTS'],
            [
                colorize(stats.total_over_2_5()), colorize(stats.total_under_2_5()),
                colorize(stats.total_over_3_5()), colorize(stats.total_under_3_5()),
                colorize(stats.clean_sheet()), colorize(stats.btts())
            ]
        ])
        print(total_table.table)

    def colorize_report(self, report):
        result = []

        for i, data in enumerate(report):
            result.append([data[0]])

            if self.team_index[i] == 0:
                _team, _opponent = 0, 1
            elif self.team_index[i] == 1:
                _team, _opponent = 1, 0

            for i in range(len(data)-1):
                stats = data[i+1].split('-')

                if len(stats) < 2:
                    result[-1].insert(i+1, data[i+1])
                    continue

                team_stat = colorize(stats[_team].strip(), color=self.color)
                opponent_stat = stats[_opponent].strip()
                if _team == 0:
                    result[-1].insert(i+1, "{0} - {1}".format(team_stat, opponent_stat))
                elif _team == 1:
                    result[-1].insert(i+1, "{0} - {1}".format(opponent_stat, team_stat))

        return result

    def calculate_team_index(self):
        """
            if self.team == Home index=0
            if self.team == Away index=0
        """

        _, team_index = np.where(self.games == self.team)
        team_index[team_index==self.dataset.HOME] = 0
        team_index[team_index==self.dataset.AWAY] = 1

        self.team_index = team_index

    def get_form(self):
        recent_form = []

        for i, game in enumerate(self.games):
            date, home, away = game[[
                self.dataset.DATE, self.dataset.HOME, self.dataset.AWAY
            ]]
            
            home_form = self.dataset.get_success_rate(date, home)
            away_form = self.dataset.get_success_rate(date, away)
            recent_form.append("{0} - {1}".format(home_form, away_form))

            if self.team_index[i] == 0:
                self.opponents_form.append(away_form)
            else:
                self.opponents_form.append(home_form)

        return recent_form

    def get_position(self):
        league_positions = []

        for i, game in enumerate(self.games):
            date, home, away = game[[
                self.dataset.DATE, self.dataset.HOME, self.dataset.AWAY
            ]]
            
            home_pos = self.dataset.get_position(date, home)
            away_pos = self.dataset.get_position(date, away)
            league_positions.append("{0} - {1}".format(home_pos, away_pos))

            if self.team_index[i] == 0:
                self.opponents_pos.append(away_pos)
            else:
                self.opponents_pos.append(home_pos)

        return league_positions

    def get_date(self):
        return self.games[:,self.dataset.DATE]

    def get_teams(self):
        return np.array(["{0} - {1}".format(
            game[self.dataset.HOME], game[self.dataset.AWAY]) for game in self.games]
        )

    def get_result(self):
        return self.games[:,self.dataset.FTR]

    def get_goals(self):
        return np.array(["{0} - {1}".format(
            game[self.dataset.FTHG], game[self.dataset.FTAG]) for game in self.games]
        )

    def get_total_shots(self):
        return np.array(["{0} - {1}".format(
            game[self.dataset.HS], game[self.dataset.AS]) for game in self.games]
        )

    def get_shots_on_target(self):
        return np.array(["{0} - {1}".format(
            game[self.dataset.HST], game[self.dataset.AST]) for game in self.games]
        )

    def get_corners(self):
        return np.array(["{0} - {1}".format(
            game[self.dataset.HC], game[self.dataset.AC]) for game in self.games]
        )
