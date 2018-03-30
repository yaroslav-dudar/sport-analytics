#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from io import StringIO

class DataSet:
    
    def __init__(self, data):
        self.data = data

        # specify field indexes
        self.DATE = 0
        self.HOME = 1
        self.AWAY = 2

        self.HS = 3
        self.AS = 4

        self.HST = 5
        self.AST = 6

        self.HC = 7
        self.AC = 8 

    def get_games(self, team, filter_by='all'):
        """
        @filter_by:
            - all : get all team matches
            - home : get only home matches
            - away : get only away matches
        """
        if filter_by == 'all':
            condition = (team==self.data[:,self.HOME]) | (team==self.data[:,self.AWAY])
        elif filter_by == 'home':
            condition = (team==self.data[:,self.HOME])
        elif filter_by == 'away':
            condition = (team==self.data[:,self.AWAY])

        return self.data[condition]


class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path

        self._load_data()
        self._identify_fields()

    def to_dataset(self):
        """
            Convert data to numpy array in a given format
            [Date, Home Team, Away Team, Home Team Goals, Away Team Goals, Home Team Shots]
        """
        data = self.data[:,[
            self.DATE, self.HOME, self.AWAY, self.HS,
            self.AS, self.HST, self.AST, self.HC, self.AC]
        ]

        return DataSet(data)


class FootballDataLoader(DataLoader):
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

        self.HS = self.columns.index('HS')
        self.AS = self.columns.index('AS')

        self.HST = self.columns.index('HST')
        self.AST = self.columns.index('AST')

        self.HC = self.columns.index('HC')
        self.AC = self.columns.index('AC')
