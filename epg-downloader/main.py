#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from channels import ChannelsManager


def main():
    channels_manager = ChannelsManager.from_website()
    channel = channels_manager['hbo2']

    channel.get_program_for_date(datetime.datetime.now())


if __name__ == '__main__':
    main()
