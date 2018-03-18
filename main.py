#!/usr/bin/env python
# -*- coding: utf-8 -*-

from parser import football_data_co_uk_parser
from reports import print_team_report, print_tournament_report

if __name__ == '__main__':  

    data = football_data_co_uk_parser(_file='I1.csv')
    print_team_report('Inter', data, 10, filter_by='all')
    #print_tournament_report(data, 7, filter_by='home')
