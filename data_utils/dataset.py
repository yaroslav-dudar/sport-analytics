#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import time

from operator import itemgetter

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
