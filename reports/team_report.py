#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

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

    def print(self):
        report = list(np.stack((
            self.get_date(), self.get_teams(), self.get_goals(), self.get_result(),
            self.get_total_shots(), self.get_shots_on_target(),
            self.get_corners(), self.get_form(), self.get_position()
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

    def colorize_report(self, report):
        result = []

        for data in report:
            teams = data[1].split('-')
            result.append([data[0]])

            if teams[0].strip() == self.team:
                _team, _opponent = 0, 1
            elif teams[1].strip() == self.team:
                _team, _opponent = 1, 0
            else:
                raise Exception()

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

    def get_form(self):
        recent_form = []

        for game in self.games:
            date, home, away = game[[
                self.dataset.DATE, self.dataset.HOME, self.dataset.AWAY
            ]]
            
            home_form = self.dataset.get_success_rate(date, home)
            away_form = self.dataset.get_success_rate(date, away)
            recent_form.append("{0} - {1}".format(home_form, away_form))

        return recent_form

    def get_position(self):
        league_positions = []

        for game in self.games:
            date, home, away = game[[
                self.dataset.DATE, self.dataset.HOME, self.dataset.AWAY
            ]]
            
            home_pos = self.dataset.get_position(date, home)
            away_pos = self.dataset.get_position(date, away)
            league_positions.append("{0} - {1}".format(home_pos, away_pos))

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
