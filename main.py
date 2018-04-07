#!/usr/bin/env python
# -*- coding: utf-8 -*-

from data_utils.footballcouk import FootballDataCoUK
from reports.team_report import TeamReport
from reports.league_report import LeagueReport

import os

if __name__ == '__main__':
    file_path = os.path.join('./data', 'E1.csv')
    data = FootballDataCoUK(file_path)
    dataset = data.to_dataset()
    
    league_report = LeagueReport(dataset, amount_games=7)
    league_report.print()
    
    report1 = TeamReport(dataset, 'Sheffield Weds', filter_by='all', amount_games=7)
    report1.print()

    report2 = TeamReport(dataset, 'Fulham', filter_by='all', amount_games=7)
    report2.print()
