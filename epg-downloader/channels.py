#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from collections import namedtuple

import datetime
from bs4 import BeautifulSoup

from utils import request_tv_channels, request_program_for_date, get_datetime_object

Show = namedtuple('Show', 'url name start_time description episode season')


class ChannelsManager:
    EPG_HOST = 'telemagazyn.pl'
    EPG_URL = 'https://{host}'.format(host=EPG_HOST)

    TV_CHANNELS = '/stacje'
    TV_CHANNELS_URL = '{url}{tv_channels}'.format(url=EPG_URL, tv_channels=TV_CHANNELS)

    def __init__(self, channels):
        self.channels = channels
        self.number_of_channels = len(channels)

    def __getitem__(self, item):
        return self.channels[ChannelsManager.encode_channel_name(item)]

    @staticmethod
    def encode_channel_name(name):
        return name.lower().replace(" ", "_")

    @classmethod
    def from_website(cls):
        response = request_tv_channels(ChannelsManager.TV_CHANNELS_URL)

        soup = BeautifulSoup(response.text, "html.parser")

        channels = {}
        for channel in soup.find("div", {"class": "listaStacji"}).findAll("li", {"class": "polska"}):
            name = channel.next.text
            url = channel.next.attrs['href']
            channels[ChannelsManager.encode_channel_name(name)] = Channel(name, url)

        return cls(channels)


class Channel:
    def __init__(self, name, url):
        self.name = name
        self.channel_url = '{epg_url}/{url}'.format(epg_url=ChannelsManager.EPG_URL, url=url.strip('/'))
        self.program = {}

    def __repr__(self):
        return '<Channel: {name}, URL: {url}>'.format(name=self.name, url=self.channel_url)

    def get_program_for_date(self, date):
        today = get_datetime_object(date)

        response = request_program_for_date(self.channel_url, today)

        soup = BeautifulSoup(response.text, "html.parser")
        for program in soup.find("div", {"id": "programDzien"}).find("ul").findAll("a", {"class": None}):
            if program.attrs['href'].startswith('/'):
                url = program.attrs['href'].strip('/')
            else:
                continue

            # url name start_time description episode season
            start_time = program.find("em").text.strip()
            if int(start_time.split(':')[0]) >= 6:

                show_url = '{epg_url}/{url}'.format(epg_url=ChannelsManager.EPG_URL, url=url)
                name = program.find("span").text.strip()

                descriptions = program.findAll("p")
                if len(descriptions) == 1:
                    description = descriptions[0].text.strip()
                    season, episode = None, None
                elif len(descriptions) == 2:
                    description = descriptions[0].text.strip()
                    season_re = re.search(r'Sezon\:\s+(\d+)', descriptions[1].text)
                    episode_re = re.search(r'Odcinek\:\s+(\d+)', descriptions[1].text)
                    season = season_re.group(1) if season_re else None
                    episode = episode_re.group(1) if episode_re else None
                else:
                    description, season, episode = None, None, None

                show = Show(url=show_url, name=name, start_time=start_time, description=description, season=season,
                            episode=episode)

                print(show)
                print('----------')
