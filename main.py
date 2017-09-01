#!/usr/bin/env python3

from datetime import date
from pathlib import Path

import qsbk
import sendmail

if __name__ == '__main__':

    today = date.today().strftime('%Y%m%d')

    fp = Path('data/qsbk-{}.json'.format(today))
    if fp.is_file():
        with fp.open('r') as f:
            json = f.read()
    else:
        qs_list = qsbk.collect()
        json = qs_list.toJson()
        with fp.open('w') as f:
            print(json, file=f)

    print(json)

    #sendmail.send_text('糗事百科每日精选', text)




