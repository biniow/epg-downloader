#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup


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
        return name.lower().replace(" ", "")

    @classmethod
    def create_manager(cls):
        try:
            response = requests.get(ChannelsManager.TV_CHANNELS_URL)
        except requests.RequestException as e:
            print('Error while downloading TV channels list {error}'.format(error=str(e)))
            raise

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

    def __repr__(self):
        return '<Channel: {name}, URL: {url}>'.format(name=self.name, url=self.channel_url)
