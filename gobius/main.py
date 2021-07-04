# -*- coding: utf-8 -*-

"""
Copyright (c) 2021 symbiontDCOS

Authors:
    Robert Callicotte <rcallicotte@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sys
from .dialogs import (
        display_complete,
        display_final_answer,
        display_hostname,
        display_license,
        display_password,
        display_urlselector,
        display_title,
        display_write_image,
        select_disk,
        select_image,
        select_timezone,
        )

VERSION = '2107rc1'
DEFAULT_TITLE = f'Symbiont SlimOS installer v{VERSION}'
DEFAULT_URL = 'http://osi-hub.callicotte.org/osi-hub/SlimOS/generic-x86_64/stable'


def main():
    '''The main function'''

    display_title(DEFAULT_TITLE)

    if display_license() == 'cancel':
        sys.exit(1)

    myurl = display_urlselector(DEFAULT_URL)[1]
    image = select_image(myurl)[1]
    timezone = select_timezone()[1]
    hostname = display_hostname()[1]
    password = display_password()[1]
    disk = select_disk()[1]

    if display_final_answer(
            img=image,
            tz=timezone,
            host=hostname,
            hd=disk,
            passwd=password) == 'cancel':
        sys.exit(1)

    display_write_image(f'{myurl}/{image}', disk)
    display_complete()


if __name__ == '__main__':
    main()
