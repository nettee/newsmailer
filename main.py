#!/usr/bin/env python3

from datetime import date
from pathlib import Path
import json

import qsbk
import sendmail

if __name__ == '__main__':

    today = date.today().strftime('%Y%m%d')

    fp = Path('data/qsbk-{}.json'.format(today))
    if fp.is_file():
        with fp.open('r') as f:
            json_string = f.read()
            qs_list = json.loads(json_string)
    else:
        qs_list = qsbk.collect()
        json_string = json.dumps(qs_list)
        with fp.open('w') as f:
            print(json_string, file=f)

    mail = qsbk.generate_mail(qs_list)
    sendmail.sendmail(mail)

