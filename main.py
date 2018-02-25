#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from parser import football_data_co_uk_parser, get_team_matches

data = football_data_co_uk_parser()

team = 'Arsenal'
arsenal_games = get_team_matches(team, data)

arsenal_score = np.array([g[4] if g[2]==team else g[5] for g in arsenal_games]).astype(int)
arsenal_miss = np.array([g[5] if g[2]==team else g[4] for g in arsenal_games]).astype(int)

print(arsenal_score)
print(arsenal_miss)

print(arsenal_score.mean())
print(arsenal_miss.mean())

print(arsenal_score.std())
print(arsenal_miss.std())
