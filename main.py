#!/usr/bin/env python
# -*- coding: utf-8 -*-

from parser import football_data_co_uk_parser
from reports_lib import print_team_report, print_tournament_report

from data_loader import FootballDataLoader
from reports.team_report import TeamReport

import os

if __name__ == '__main__':
    data = football_data_co_uk_parser(_file='SP1.csv')
    print_tournament_report(data, 5, filter_by='all')

    file_path = os.path.join('./data', 'SP1.csv')
    data = FootballDataLoader(file_path)
    dataset = data.to_dataset()

    report1 = TeamReport(dataset, 'Betis', filter_by='all')
    report1.print()

    report2 = TeamReport(dataset, 'Getafe', filter_by='all')
    report2.print()
