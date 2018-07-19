#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import requests


def request_tv_channels(url):
    return request(url)


def request_program_for_date(channel_url, date):
    if not is_valid_date_range(date):
        raise Exception('Invalid date range. Should be (2 years in the past <-> 14 days in the future)')

    url = "{channel}?dzien={day}".format(channel=channel_url, day=date.strftime('%Y-%m-%d'))
    return request(url)


def request(url):
    try:
        return requests.get(url)
    except requests.RequestException as e:
        print('Error while downloading TV channels list {error}'.format(error=str(e)))
        raise


def is_valid_date_range(date):
    now = datetime.datetime.now()
    past_milestone = now - datetime.timedelta(days=730)
    future_milestone = now + datetime.timedelta(days=14)
    return past_milestone < date < future_milestone


def get_datetime_object(date):
    if not isinstance(date, datetime.datetime):
        try:
            return datetime.datetime.strptime(str(date), '%Y-%m-%d')
        except ValueError:
            raise Exception('Invalid data provided. Should be datetime object or in format YYYY-MM-DD')
    return date