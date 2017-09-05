#!/usr/bin/env python3

from datetime import date
from pathlib import Path
import json

import qsbk
import lily
import sendmail

active_packages = [
    #qsbk,
    lily,
]

if __name__ == '__main__':

    today = date.today().strftime('%Y%m%d')

    for package in active_packages:
        fp = Path('data/{}-{}.json'.format(package.abbr, today))
        if fp.is_file():
            with fp.open('r') as f:
                json_string = f.read()
                data = json.loads(json_string)
        else:
            data = package.collect()
            json_string = json.dumps(data)
            with fp.open('w') as f:
                print(json_string, file=f)

        mail = package.generate_mail(data, today)
        sendmail.sendmail(mail)
