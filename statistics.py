#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from data_utils.dataset import DataSet

class TeamStats:

    def __init__(self, team, team_games):
        self.team = team
        self.team_games = team_games
        self.get_total()

    def get_total(self):
        x, _ = np.where(self.team_games == self.team)
        self.total = np.sum(
            self.team_games[x][:,[DataSet.FTHG, DataSet.FTAG]].astype(int),
            axis=1
        )

    def avg_goals_score(self):
        x, y = np.where(self.team_games == self.team)
        y[y==DataSet.HOME] = DataSet.FTHG
        y[y==DataSet.AWAY] = DataSet.FTAG
        return self.team_games[x,y].astype(int).mean()

    def avg_goals_concede(self):
        x, y = np.where(self.team_games == self.team)
        y[y==DataSet.HOME] = DataSet.FTAG
        y[y==DataSet.AWAY] = DataSet.FTHG
        return self.team_games[x,y].astype(int).mean()

    def std_goals_score(self):
        x, y = np.where(self.team_games == self.team)
        y[y==DataSet.HOME] = DataSet.FTHG
        y[y==DataSet.AWAY] = DataSet.FTAG
        return self.team_games[x,y].astype(int).std()

    def std_goals_concede(self):
        x, y = np.where(self.team_games == self.team)
        y[y==DataSet.HOME] = DataSet.FTAG
        y[y==DataSet.AWAY] = DataSet.FTHG
        return self.team_games[x,y].astype(int).std()

    def avg_total_shots(self):
        x, y = np.where(self.team_games == self.team)
        y[y==DataSet.HOME] = DataSet.HS
        y[y==DataSet.AWAY] = DataSet.AS
        return self.team_games[x,y].astype(int).mean()

    def avg_shots_on_target(self):
        x, y = np.where(self.team_games == self.team)
        y[y==DataSet.HOME] = DataSet.HST
        y[y==DataSet.AWAY] = DataSet.AST
        return self.team_games[x,y].astype(int).mean()

    def avg_op_total_shots(self):
        x, y = np.where(self.team_games == self.team)
        y[y==DataSet.HOME] = DataSet.AS
        y[y==DataSet.AWAY] = DataSet.HS
        return self.team_games[x,y].astype(int).mean()

    def avg_op_shots_on_target(self):
        x, y = np.where(self.team_games == self.team)
        y[y==DataSet.HOME] = DataSet.AST
        y[y==DataSet.AWAY] = DataSet.HST
        return self.team_games[x,y].astype(int).mean()

    def total_over_2_5(self):
        return (self.total > 2.5).sum() / len(self.total)

    def total_under_2_5(self):
        return (self.total < 2.5).sum() / len(self.total)

    def total_over_3_5(self):
        return (self.total > 3.5).sum() / len(self.total)

    def total_under_3_5(self):
        return (self.total < 3.5).sum() / len(self.total)

    def btts(self):
        """ Both teams to score """
        x, _ = np.where(self.team_games == self.team)
        goals = self.team_games[x][:,[DataSet.FTHG, DataSet.FTAG]].astype(int)
        return np.all(goals, axis=1).sum() / len(goals)

    def clean_sheet(self):
        x, y = np.where(self.team_games == self.team)
        y[y==DataSet.HOME] = DataSet.FTAG
        y[y==DataSet.AWAY] = DataSet.FTHG

        concede = self.team_games[x,y].astype(int)
        return (concede == 0).sum() / len(concede)
