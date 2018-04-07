#!/usr/bin/env python
# -*- coding: utf-8 -*-

from terminaltables import SingleTable

from utils import colorize

class LeagueReport:

    def __init__(self, dataset, amount_games=5, filter_by='all'):
        self.filter_by = filter_by
        self.amount_games = amount_games
        self.dataset = dataset
        self.FTR = -1

    def colorize_results(self, table):
        for team in table:
            results = team[self.FTR]

            colorized_res = []
            for res in results:
                if res == 'L':
                    col = 'red'
                elif res == 'W':
                    col = 'green'
                else:
                    col = 'white'

                colorized_res.append(colorize(res, color=col))

            team[self.FTR] = ' '.join(colorized_res)

        return table

    def print(self):
        report_column_names = [
            "Team", "Points", "Scored", "Cons", "Results",
        ]

        table = self.dataset.get_league_table(prev_games=self.amount_games)
        table = self.colorize_results(table)

        table.insert(0, report_column_names)
        league_table = SingleTable(table)
        print(league_table.table)
