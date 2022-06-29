import argparse
import configparser
import datetime
import time
import requests as req
import os
from threading import Thread
from collections import defaultdict
import random

stats = defaultdict(int)


def main():
    parser = argparse.ArgumentParser(description="Request repeater")
    parser.add_argument('-s', '--start_date', type=str, help='The start date of request repetition, default is now, '
                                                             'format: Y-m-d H:M:S')
    parser.add_argument('-e', '--end_date', type=str, help='The end date of request repetition, default is start_date '
                                                           '+ 1min, required if config file not provided, format: '
                                                           'Y-m-d H:M:S')
    parser.add_argument('-l', '--link', type=str, help='The link for request, required if config file not provided')
    parser.add_argument('-r', '--ratio', type=int, default=0, help='Ratio of request sending per minute, 0 is max, '
                                                                   '-r 1 means 1 request per minute')
    parser.add_argument('-f', '--file', type=str, help='Path to the file to send')
    parser.add_argument('-rd', '--random', type=str, default=0, help='Sleep is 60/ratio, random defines the percent of this number to add/delete to this equation')
    parser.add_argument('-t', '--threads', type=int, default=1, help='Number of threads used to execute request '
                                                                     'repetition. default = 1, system max = 0')
    parser.add_argument('-c', '--config', type=str, help='Path to the config file in format:\n'
                                                         '[DEFAULT]\n'
                                                         'StartDate = x\n'
                                                         'EndDate = x\n'
                                                         'Link = x\n'
                                                         'Ratio = x\n'
                                                         'File = x\n'
                                                         'Threads = x\n')

    args = parser.parse_args()
    start_date: datetime
    end_date: datetime
    link: str
    ratio: int
    random_c: int
    file: str
    threads: int
    if args.config is not None:
        config = configparser.ConfigParser()
        config.read(args.config)
        config = config['DEFAULT']
        start_date = datetime.datetime.strptime(config["StartDate"], "%Y-%m-%d %H:%M:%S")
        end_date = datetime.datetime.strptime(config["EndDate"], "%Y-%m-%d %H:%M:%S")
        link = config["Link"]
        ratio = int(config["Ratio"])
        file = config["File"]
        threads = int(config["Threads"])
        random_c = int(config["Random"])
    elif args.link is None:
        raise AssertionError('Link must be provided')
    elif args.file is None:
        raise AssertionError('File path must be provided')
    else:
        if args.start_date is None:
            start_date = datetime.datetime.now()
        else:
            start_date = datetime.datetime.strptime(args.start_date, "%Y-%m-%d %H:%M:%S")

        if args.end_date is None:
            end_date = start_date + datetime.timedelta(minutes=1)
        else:
            end_date = datetime.datetime.strptime(args.end_date, "%Y-%m-%d %H:%M:%S")
        link = args.link
        ratio = args.ratio
        file = args.file
        random_c = args.random

        if args.threads == 0:
            threads = os.cpu_count()
        else:
            threads = args.threads

    # noinspection PyUnboundLocalVariable
    for x in range(1, threads):
        t = Thread(target=request_sender, args=(x, start_date, end_date, ratio, link, file, random_c))
        t.start()
    t = Thread(target=request_sender, args=(0, start_date, end_date, ratio, link, file, random_c, True))
    t.start()


def request_sender(name, start, stop, ratio, link, file, random_c, stat=False):
    real_start = datetime.datetime.now()
    while datetime.datetime.now() < stop:
        if start < datetime.datetime.now():
            stats[name] += 1
            req.post(link, files={'pdf': open(file, 'rb')})
            if stat:
                t = (datetime.datetime.now() - real_start).total_seconds()
                s = sum(stats.values())
                print(f'Requests sent: {s}, time elapsed: {str(t)}, | {s/t} r/s\r', end="")
            if ratio != 0:
                t = 60 / ratio
                t += random.randint(-random_c, random_c)/100 * t
                time.sleep(t)
        else:
            time.sleep(60)
            real_start = datetime.datetime.now()


if __name__ == '__main__':
    main()
