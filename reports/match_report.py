#!/usr/bin/env python
# -*- coding: utf-8 -*-

from reports.team_report import TeamReport
from reports.league_report import LeagueReport
from reports.stats_report import StatsReport

from terminaltables import SingleTable

class MatchReport:

    def __init__(self, home_team, away_team, dataset):
        self.home_team = home_team
        self.away_team = away_team
        self.dataset = dataset

        self.amount_games = len(dataset.get_all_teams())*2 - 2
        self.recent_games = 7

    def print(self):
        self.print_headline('League Table')
        league_report = LeagueReport(self.dataset, amount_games=self.amount_games)
        league_report.print()

        self.print_headline('Home team report')
        home_report = TeamReport(self.dataset, self.home_team, self.recent_games, filter_by='home')
        home_report.print()
        home_report = TeamReport(self.dataset, self.home_team, self.recent_games, filter_by='all')
        home_report.print()

        self.print_headline('Away team report')
        away_report = TeamReport(self.dataset, self.away_team, self.recent_games, filter_by='away')
        away_report.print()
        away_report = TeamReport(self.dataset, self.away_team, self.recent_games, filter_by='all')
        away_report.print()

        self.print_headline('Overall Stats Report')
        stats_report = StatsReport(self.dataset, amount_games=self.amount_games)
        stats_report.print()

        self.print_headline('Recent Stats Report')
        stats_report = StatsReport(self.dataset, amount_games=self.recent_games)
        stats_report.print()
        
    def print_headline(self, text):
        text = SingleTable([[text]])
        text.padding_left, text.padding_right = [35, 35]
        print(text.table)
