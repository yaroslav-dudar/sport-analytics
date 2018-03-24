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
        return self.team_games[x,y+8].astype(int).mean()

    def avg_shots_on_target(self):
        x, y = np.where(self.team_games == self.team)
        return self.team_games[x,y+10].astype(int).mean()

    def avg_op_total_shots(self):
        x, y = np.where(self.team_games == self.team)
        y[y==2] += 9
        y[y==3] += 7
        return self.team_games[x,y].astype(int).mean()

    def avg_op_shots_on_target(self):
        x, y = np.where(self.team_games == self.team)
        y[y==2] += 11
        y[y==3] += 9
        return self.team_games[x,y].astype(int).mean()

    def op_form(self, recent_form):
        x, y = np.where(self.team_games == self.team)
        y[y==2] = 1
        y[y==3] = 0

        success_rate = 0
        for i in x:
            form = recent_form[i].replace(' ', '').split('-')
            success_rate += float(form[y[i]])

        return success_rate/len(x)

    def op_position(self, positions):
        x, y = np.where(self.team_games == self.team)
        y[y==2] = 1
        y[y==3] = 0

        mean_position = 0
        for i in x:
            form = positions[i].replace(' ', '').split('-')
            mean_position += int(form[y[i]])

        return mean_position/len(x)

    def get_team_recent_form(self):
        x, y = np.where(self.team_games == self.team)
        scored = self.team_games[x,y+2].astype(int)

        x, y = np.where(self.team_games == self.team)
        y[y==2] += 3
        y[y==3] += 1
        conceded = self.team_games[x,y].astype(int)
        goal_diff = scored - conceded

        draws = goal_diff[goal_diff == 0]
        wins = goal_diff[goal_diff > 0]

        return (len(draws)*0.5 + len(wins))/len(goal_diff)
