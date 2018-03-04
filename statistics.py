#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

class TeamStats:

    def __init__(self, team, team_games):
        self.team = team
        self.team_games = team_games

    def avg_goals_score(self):
        x, y = np.where(self.team_games == self.team)
        return self.team_games[x,y+2].astype(int).mean()

    def avg_goals_concede(self):
        x, y = np.where(self.team_games == self.team)
        y[y==2] += 3
        y[y==3] += 1
        return self.team_games[x,y].astype(int).mean()

    def std_goals_score(self):
        x, y = np.where(self.team_games == self.team)
        return self.team_games[x,y+2].astype(int).std()

    def std_goals_concede(self):
        x, y = np.where(self.team_games == self.team)
        y[y==2] += 3
        y[y==3] += 1
        return self.team_games[x,y].astype(int).std()

    def avg_total_shots(self):
        x, y = np.where(self.team_games == self.team)
        return self.team_games[x,y+9].astype(int).std()

    def avg_shots_on_target(self):
        x, y = np.where(self.team_games == self.team)
        return self.team_games[x,y+11].astype(int).std()

    def avg_op_total_shots(self):
        x, y = np.where(self.team_games == self.team)
        y[y==2] += 10
        y[y==3] += 8
        return self.team_games[x,y].astype(int).std()

    def avg_op_shots_on_target(self):
        x, y = np.where(self.team_games == self.team)
        y[y==2] += 12
        y[y==3] += 10
        return self.team_games[x,y].astype(int).std()
