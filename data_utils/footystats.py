#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from io import StringIO
import csv

from data_utils.datasource import DataSource

class FootyStatsOrg(DataSource):
    def _load_data(self):
        rows, max_row_len = [], -1

        for line in open(self.file_path):
            row = next(csv.reader(StringIO(line), delimiter=','))
            rows.append(row)

            if len(row) > max_row_len:
                max_row_len = len(row)


        data = np.array(rows)
        self.data = data[1:]
        self.columns = list(data[0])

    def _identify_fields(self):
        self.DATE = self.columns.index('date_GMT')
        self.HOME = self.columns.index('home_team_name')
        self.AWAY = self.columns.index('away_team_name')
        self.FTR = self.columns.index('result')

        self.HS = self.columns.index('home_team_shots')
        self.AS = self.columns.index('away_team_shots')

        self.HST = self.columns.index('home_team_shots_on_target')
        self.AST = self.columns.index('away_team_shots_on_target')

        self.HC = self.columns.index('home_team_corner_count')
        self.AC = self.columns.index('away_team_corner_count')

        self.FTHG = self.columns.index('home_team_goal_count')
        self.FTAG = self.columns.index('away_team_goal_count')