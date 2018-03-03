#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from parser import football_data_co_uk_parser, get_team_matches, get_columns

from terminaltables import SingleTable

data = football_data_co_uk_parser()
col_names, col_indx = get_columns()

if __name__ == '__main__':
    games_amount = 20
    team_1 = 'Brighton'
    team_2 = 'Arsenal'

    team_1_games = get_team_matches(team_1, data, filter_by='home')[-games_amount:]
    team_1_data = list(team_1_games[:,col_indx])
    team_1_data.insert(0, col_names)

    view_table = SingleTable(team_1_data)
    print(view_table.table)
