from datetime import datetime
import csv
import os
import pandas as pd
from matplotlib import pyplot as plt


def get_dict(name_dict, key_dict):
    if name_dict.get(key_dict) is None:
        name_dict[key_dict] = [f'"cid","dt","dvalue"\n"{cid}","{dt}","{dvalue}"\n']
    else:
        temp = name_dict.get(key_dict)
        temp.append(f'"{cid}","{dt}","{dvalue}"\n')
        name_dict[key_dict] = temp


def create_csv(name_folder, name_dict):
    for key, value in name_dict.items():
        with open(f'task\\data\\{name_folder}\\{key}.csv', 'w') as new_file:
            new_file.writelines(value)


def create_png(way_folder):
    for dirs, folder, files in os.walk(f'task\\data\\{way_folder}'):
        for name in files:
            df = pd.read_csv(f'task\\data\\{way_folder}\\{name}')
            df.plot(y='dvalue', use_index=True)
            plt.savefig(f'task\\img\\{way_folder}\\{name[:-4]}.png')
            plt.close()


if __name__ == '__main__':
    dayAll, dayCid, weekAll, weekCid, cidAll = dict(), dict(), dict(), dict(), dict()
    with open('data1.csv', 'r') as file:
        reader = csv.reader(file)
        for cid, dt, dvalue in [*reader][1:]:
            date_and_time = dt.split(' ')
            date = date_and_time[0]
            day, month, year = date.split('.')
            cid_and_date = f'{cid} {date}'
            week_and_year = f'{datetime.strptime(f"{date}", "%d.%m.%Y").isocalendar()[1]} {year}'
            cid_and_week = f'{cid} {datetime.strptime(f"{date}", "%d.%m.%Y").isocalendar()[1]} {year}'
            get_dict(dayAll, date)
            get_dict(dayCid, cid_and_date)
            get_dict(weekAll, week_and_year)
            get_dict(weekCid, cid_and_week)
            get_dict(cidAll, cid)
    for way, name_dict in zip(['Every day all sensors', 'Every sensor every day', 'Every week all sensors',
                               'Every sensor is weekly', 'Each sensor for the entire time period'],
                              [dayAll, dayCid, weekAll, weekCid, cidAll]):
        create_csv(way, name_dict)
        create_png(way)
