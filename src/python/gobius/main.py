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

from gobius.dialogs import (
    display_complete,
    display_final_answer,
    display_hostname,
    display_license,
    display_password,
    display_urlselector,
    display_title,
    display_write_image,
    display_disk,
    display_image,
    display_timezone,
)
from gobius.utils import die


VERSION = "2107rc1"
DEFAULT_TITLE = f"Symbiont SlimOS installer v{VERSION}"
DEFAULT_URL = "http://osi-hub.callicotte.org/osi-hub/SlimOS/generic-x86_64/stable"


def select_config(selector):
    """Calls simple selectors"""
    if selector[0] == "cancel":
        die("Installer terminated per user request")

    return selector[1]


def install():
    """Set up the main selector components"""
    display_title(DEFAULT_TITLE)

    if display_license() == "cancel":
        die("Installer terminated per user request")

    myurl = display_urlselector(DEFAULT_URL)

    if myurl[0] == "cancel":
        die("Installer terminated per user request")

    image = select_config(display_image(myurl[1]))
    timezone = select_config(display_timezone())
    hostname = select_config(display_hostname())
    password = select_config(display_password())
    disk = select_config(display_disk())

    if (
        display_final_answer(
            img=image, tz=timezone, host=hostname, hd=disk, passwd=password
        )
        == "cancel"
    ):
        die("Installer terminated per user request")

    display_write_image(f"{myurl[1]}/{image}", disk)

    return {
        "timezone": timezone,
        "hostname": hostname,
        "password": password,
    }


def post_install(args):
    """Post install steps"""
    pass


def main():
    """The main function"""
    install()


if __name__ == "__main__":
    main()
