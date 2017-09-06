#!/usr/bin/env python3

from datetime import date
from pathlib import Path
import json

import qsbk
import lily
import sendmail

receivers = [
    'anchori@163.com',
    #'nettee.liu@gmail.com',
    #'tfn0510@gmail.com',
]

active_packages = [
    qsbk,
    lily,
]

if __name__ == '__main__':

    today = date.today().strftime('%Y%m%d')

    for package in active_packages:
        print('Fetching {}...'.format(package.abbr))
        fp = Path('data/{}-{}.json'.format(package.abbr, today))
        if fp.is_file():
            print('Reading from file {}...'.format(str(fp)))
            with fp.open('r') as f:
                json_string = f.read()
                data = json.loads(json_string)
        else:
            print('Crawler working...')
            data = package.collect()
            json_string = json.dumps(data)
            with fp.open('w') as f:
                print(json_string, file=f)
            print('Saved to file {}'.format(str(fp)))

        mail = package.generate_mail(data, today)
        for receiver in receivers:
            try:
                sendmail.sendmail(mail, receiver)
                print('Sent {} to {}'.format(package.abbr, receiver))
            except Exception:
                print('Error in sending {} to {}'.format(package.abbr, receiver))
