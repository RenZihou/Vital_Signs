# -*- encoding: utf-8 -*-
# @Author: RZH

import json
from re import search
from datetime import timedelta, datetime

import pandas as pd


def data_process(df):
    # delete unwanted columns
    data_types = json.load(open('./config/types.json', 'r'))
    df = df.drop(labels=data_types['Discard'], axis=1)

    df.rename(
        columns={'Timestamp of Report (Local Time)': 'Time'}, inplace=True
    )

    # map strings into integers
    map_table = json.load(open('./config/mapping_table.json', 'r'))
    for name, table in map_table.items():
        for text, value in table.items():
            df.loc[df[name] == text, name] = value

    # split tokens
    tokens_ = json.load(open('./config/tokens.json', 'r'))
    for name, tokens in tokens_.items():
        for token in tokens:
            df[token] = df[name].apply(lambda x: 1 if token in str(x) else 0)
        del df[name]

    # reformat report time
    # represent the time in minutes (for later use: wake-up & sleep time)
    def time_to_minute(
            t: str,
            threshold=json.load(open('./config/sleep.json', 'r'))
    ):
        """
        :param t: str, `%B %d, %Y %H:%M:%S` format
        :param threshold: dict
        :return: pd.Series([int, str])
        """
        report_time = datetime.strptime(t, '%B %d, %Y %H:%M:%S')
        minute = int(report_time.strftime('%H')) * 60 \
            + int(report_time.strftime('%M'))
        if minute <= threshold['sleep'][1]:
            minute += 1440  # minutes
            report_time += timedelta(days=-1)  # regard as the previous day
        return pd.Series([minute, report_time.strftime('%B %d, %Y')])

    df[['Minute', 'Date']] = df['Time'].apply(time_to_minute)

    # merge the two reports (in a single day) into one line
    grouped_df = df.groupby(['Date'])
    new_df = pd.DataFrame()
    columns = list(df.columns)
    columns.remove('Date')
    columns.remove('Time')
    for name in columns:
        new_df[name] = grouped_df[name].apply(sum)
    new_df['Minute'] = grouped_df['Minute'].apply(
        lambda x: '|'.join(map(str, x))
    )  # merge wake-up time & sleep time
    new_df['Date'] = new_df.index

    # wake-up time & sleep time
    def duration(
            t: tuple,
            hours: list = json.load(open('./config/sleep.json'))['hours']
    ) -> int:
        """
        calculate sleep duration and represent it in hours
        :param t: (wake_minute: int, sleep_minute: int)
        :param hours: supported hours, sorted in ascending order
        :return: int
        """
        h = (t[1] - t[0]) / 60  # sleep duration in hours
        return list(filter(lambda x: x <= h, hours))[-1]
    # the former one
    new_df['Wake'] = new_df['Minute']\
        .apply(lambda x: -int(search(r'(.*)\|.*', x).groups()[0]))
    # the latter one
    new_df['Sleep'] = new_df['Minute']\
        .apply(lambda x: 1440 - int(search(r'.*\|(.*)', x).groups()[0]))
    new_df['Sleep_duration'] = new_df[['Wake', 'Sleep']].apply(duration, axis=1)
    del new_df['Minute']

    # represent date by days from the start date
    start_date = min(new_df['Date'].apply(
        lambda x: datetime.strptime(x, '%B %d, %Y'))
    )
    new_df['Day_num'] = new_df['Date'].apply(
        lambda x: (datetime.strptime(x, '%B %d, %Y') - start_date).days
    )
    new_df = new_df.sort_values(['Day_num'])
    new_df['DATE'] = new_df['Date'].apply(
        lambda x: datetime.strptime(x, '%B %d, %Y').strftime('%Y-%m-%d')
    )
    del new_df['Date']

    return new_df


if __name__ == '__main__':
    data = pd.read_csv('../data/reporter-export.csv')
    data = data_process(data)
    # print(data.head(5))
    # print(data.describe(include='all'))
    data.to_csv('../data/out.csv')
    pass
