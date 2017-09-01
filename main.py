#!/usr/bin/env python3

import qsbk
import sendmail

if __name__ == '__main__':

    text = qsbk.collect_text()
    sendmail.send_text('糗事百科每日精选', text)




