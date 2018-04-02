#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from data_loader import DataSet

class TeamStats:

    def __init__(self, team, team_games):
        self.team = team
        self.team_games = team_games

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
