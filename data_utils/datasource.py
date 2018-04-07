#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from data_utils.dataset import DataSet

class DataSource:
    def __init__(self, file_path):
        self.file_path = file_path

        self._load_data()
        self._identify_fields()

    def to_dataset(self):
        """
            Convert data to numpy array in a given format
            [
                Date, Home Team, Away Team, Home Team Goals,
                Away Team Goals, Home Team Shots, Away Team Shots,
                Home Team Shots on Target, Away Team Shots on Target,
                Home Team Corners, Away Team Corners
            ]
        """
        indexes = []
        indexes.insert(DataSet.DATE, self.DATE)
        indexes.insert(DataSet.HOME, self.HOME)
        indexes.insert(DataSet.AWAY, self.AWAY)
        indexes.insert(DataSet.FTR, self.FTR)

        indexes.insert(DataSet.FTHG, self.FTHG)
        indexes.insert(DataSet.FTAG, self.FTAG)

        indexes.insert(DataSet.HS, self.HS)
        indexes.insert(DataSet.AS, self.AS)

        indexes.insert(DataSet.HST, self.HST)
        indexes.insert(DataSet.AST, self.AST)

        indexes.insert(DataSet.HC, self.HC)
        indexes.insert(DataSet.AC, self.AC)

        data = self.data[:,indexes]
        return DataSet(data)
