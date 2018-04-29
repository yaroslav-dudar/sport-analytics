#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request
import random

import lxml.html

class Bet365Parser:

    def __init__(self):
        self.host = 'https://mobile.bet365.com/V6/sport/coupon/coupon.aspx?key=%s'

        self.useragent = 'Mozilla/5.0 (X11; Linux x86_64)' +\
            ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'

        self.keys = {
            'E0': '1-1-13-33577327-2-1-0-0-1-0-0-4100-0-0-1-0-0-0-0-0-0-0-0',
            'E1': '1-1-13-26278644-2-1-0-0-1-0-0-4100-0-0-1-0-0-0-0-0-0-0-0',
            'D1': '1-1-13-33754901-2-7-0-0-1-0-0-4100-0-0-1-0-0-0-0-0-0-0-0',
        }

        self.events_list = "//div[contains(@class, 'liveAlertKey')]//" +\
            "div[contains(@class, 'podEventRow') or contains(@class, 'podHeaderRow')]"
        self.team_names = ".//span[@class='ippg-Market_Truncator']/text()"
        self.odds = ".//div[@class='ippg-Market_Topic priceColumn']/span/text()"
        self.time_start = ".//div[@class='ippg-Market_GameStartTime']/text()"
        self.event_date = ".//div[@class='wideLeftColumn']/text()"

        self.proxy_list = ['80.211.14.207:53']

    def get_proxy(self):
        return random.choice(self.proxy_list)

    def request(self, key):
        req = urllib.request.Request(self.host % self.keys[key])
        req.add_header('User-Agent', self.useragent)

        req.set_proxy(self.get_proxy(), 'https')
        req.set_proxy(self.get_proxy(), 'http')

        resp = urllib.request.urlopen(req)
        text = resp.read().decode('utf-8')
        self.parse_html(text)

    def parse_html(self, html):
        html_tree = lxml.html.fromstring(html)
        events = html_tree.xpath(self.events_list)
        last_date = ''

        for game in events:
            date = game.xpath(self.event_date)
            if date:
                last_date = date
                continue

            teams = game.xpath(self.team_names)
            odds = game.xpath(self.odds)
            game_start = game.xpath(self.time_start)
            print(teams, odds, last_date, game_start)

    def test_request(self, _):
        """ take pre-saved html file """
        text = open('./odds/bet365-test').read()
        self.parse_html(text)

    def to_csv(self, rows):
        pass
