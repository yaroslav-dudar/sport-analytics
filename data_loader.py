#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from io import StringIO

from operator import itemgetter
from collections import OrderedDict

import time

class DataSet:
    
    # specify field indexes
    DATE = 0
    HOME = 1
    AWAY = 2

    FTHG = 3
    FTAG = 4

    HS = 5
    AS = 6

    HST = 7
    AST = 8

    HC = 9
    AC = 10

    FTR = 11

    def __init__(self, data):
        self.data = data

        self.TS_DATES = np.array([
            time.mktime(time.strptime(d, '%d/%m/%y')) for d in self.data[:,self.DATE]
        ])

    def get_games(self, team, filter_by='all'):
        condition = self.filter(team, filter_by)
        return self.data[condition]

    def get_all_teams(self):
        return list(np.unique(np.append(self.data[:, self.HOME], self.data[:, self.AWAY])))

    def filter(self, team, filter_by, data=np.array([])):
        """
        @filter_by:
            - all : get all team matches
            - home : get only home matches
            - away : get only away matches
        """

        if data.size == 0:
            data = self.data

        if filter_by == 'all':
            condition = (team==data[:,self.HOME]) | (team==data[:,self.AWAY])
        elif filter_by == 'home':
            condition = (team==data[:,self.HOME])
        elif filter_by == 'away':
            condition = (team==data[:,self.AWAY])

        return condition

    def get_success_rate(self, date, team, prev_games=5, filter_by='all'):
        """
            Calculate team form for the last <prev_games>
            where date > game_date

            win = 1 lose = 0 draw = 0.5
            result = sum(game_form) / prev_games
        """

        ts_date = time.mktime(time.strptime(date, '%d/%m/%y'))
        prev_data = self.data[self.TS_DATES < ts_date]
        condition = self.filter(team, filter_by, prev_data)

        # Precondition: games already sorted by date
        team_games = prev_data[condition][-prev_games:]

        score = 0
        for game in team_games:
            if game[self.HOME] == team:
                if game[self.FTR] == 'H':
                    score += 1
            elif game[self.AWAY] == team:
                if game[self.FTR] == 'A':
                    score += 1

            if game[self.FTR] == 'D':
                score += 0.5

        return score/prev_games

    def get_position(self, date, team):
        """ Get team league position before given date """

        ts_date = time.mktime(time.strptime(date, '%d/%m/%y'))
        # all gemes before <game_date>
        prev_games = self.data[self.TS_DATES < ts_date]

        teams = self.get_all_teams()
        # report: [points, goal diff]
        report = {t: [0,0] for t in teams}

        for game in prev_games:
            h_points, a_points = report[game[self.HOME]][0], report[game[self.AWAY]][0]
            if game[self.FTR] == 'H':
                h_points += 3

            if game[self.FTR] == 'A':
                a_points += 3

            if game[self.FTR] == 'D':
                h_points += 1
                a_points += 1

            report[game[self.HOME]][0] = h_points
            report[game[self.HOME]][1] = report[game[self.HOME]][1] +\
                int(game[self.FTHG])-int(game[self.FTAG])

            report[game[self.AWAY]][0] = a_points
            report[game[self.AWAY]][1] = report[game[self.AWAY]][1] +\
                int(game[self.FTAG])-int(game[self.FTHG])

        sorted_report = sorted(report.items(), key=itemgetter(1), reverse=True)

        team_pos = next((i for i,t in enumerate(sorted_report) if t[0] == team), None)
        return team_pos+1

    def get_league_table(self, prev_games=5):
        """
            Structure is: points, goals scored, goals cons, game results list
        """
        teams = self.get_all_teams()
        table = {t: [0,0,0,[]] for t in teams}

        for game in np.flip(self.data, axis=0):
            home = self._get_team_stats(game, 'home')
            away = self._get_team_stats(game, 'away')

            for team in [home, away]:
                team_stats = table[team['team']]
                if len(team_stats[3]) < prev_games:
                    team_stats[0] += team['points']
                    team_stats[1] += team['score']
                    team_stats[2] += team['cons']
                    team_stats[3].insert(0, team['result'])

                # remove team for which all stats are collected
                if len(team_stats[3]) == prev_games:
                    try:
                        teams.remove(team['team'])
                    except ValueError:
                        pass

            if not teams:
                break

        result_table = [[team]+stats for team, stats in table.items()]
        result_table.sort(key=lambda x: x[1], reverse=True)
        return result_table

    def _get_team_stats(self, game, side='home'):
        stats, game_result = {}, game[self.FTR]

        if side == 'home':
            team = game[self.HOME]
            score, cons, win = game[self.FTHG], game[self.FTAG], 'H'
        elif side == 'away':
            team = game[self.AWAY]
            score, cons, win = game[self.FTAG], game[self.FTHG], 'A'

        if game_result == win:
            stats['points'] = 3
            game_result = 'W'
        elif game_result == 'D':
            stats['points'] = 1
        else:
            stats['points'] = 0
            game_result = 'L'

        stats['team'] = team
        stats['score'] = int(score)
        stats['cons'] = int(cons)
        stats['result'] = game_result
        return stats

class DataSource:
    def __init__(self, file_path):
        self.file_path = file_path

        self._load_data()
        self._identify_fields()

    def to_dataset(self):
        """
            Convert data to numpy array in a given format
            [
                Date, Home Team, Away Team, Home Team Goals,
                Away Team Goals, Home Team Shots, Away Team Shots,
                Home Team Shots on Target, Away Team Shots on Target,
                Home Team Corners, Away Team Corners
            ]
        """
        indexes = []
        indexes.insert(DataSet.DATE, self.DATE)
        indexes.insert(DataSet.HOME, self.HOME)
        indexes.insert(DataSet.AWAY, self.AWAY)
        indexes.insert(DataSet.FTR, self.FTR)

        indexes.insert(DataSet.FTHG, self.FTHG)
        indexes.insert(DataSet.FTAG, self.FTAG)

        indexes.insert(DataSet.HS, self.HS)
        indexes.insert(DataSet.AS, self.AS)

        indexes.insert(DataSet.HST, self.HST)
        indexes.insert(DataSet.AST, self.AST)

        indexes.insert(DataSet.HC, self.HC)
        indexes.insert(DataSet.AC, self.AC)

        data = self.data[:,indexes]
        return DataSet(data)


class FootballDataCoUK(DataSource):
    def _load_data(self):
        rows, max_row_len = [], -1

        for line in open(self.file_path):
            row = np.loadtxt(StringIO(line), dtype=str, delimiter=',')
            rows.append(row)

            if len(row) > max_row_len:
                max_row_len = len(row)

        data = []
        # fill missing columns with empty string
        for row in rows:
            row_len_diff = max_row_len - len(row)
            row = np.append(row, ['']*row_len_diff)
            data.append(row)

        del rows
        data = np.array(data)

        self.data = data[1:]
        self.columns = list(data[0])

    def _identify_fields(self):
        self.DATE = self.columns.index('Date')
        self.HOME = self.columns.index('HomeTeam')
        self.AWAY = self.columns.index('AwayTeam')
        self.FTR = self.columns.index('FTR')

        self.HS = self.columns.index('HS')
        self.AS = self.columns.index('AS')

        self.HST = self.columns.index('HST')
        self.AST = self.columns.index('AST')

        self.HC = self.columns.index('HC')
        self.AC = self.columns.index('AC')

        self.FTHG = self.columns.index('FTHG')
        self.FTAG = self.columns.index('FTAG')
