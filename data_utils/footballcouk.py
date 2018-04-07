#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from io import StringIO

from data_utils.datasource import DataSource

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
