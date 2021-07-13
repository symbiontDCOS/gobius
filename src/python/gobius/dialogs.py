# -*- coding:utf-8 -*-

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
import time
import random
import pytz
from dialog import Dialog
from gobius.utils import list_disks, list_images, write_image


DISPLAY = Dialog(dialog="dialog", DIALOGRC="/etc/dialogrc")


def display_write_image(url, dest):
    """
    Write the selected image to disk using bmaptools. This requires a
    specialized webserver (osi-hub).  The webserver must display the
    artifacts in json format.
    """
    pretty_image = url.split("/")[-1]
    DISPLAY.gauge_start(f"Installing {pretty_image}", width=80, height=15, percent=0)

    mycopy = write_image(url, dest)

    percent = 0
    while mycopy.poll() is None:
        DISPLAY.gauge_update(percent)
        time.sleep(1)
        percent += 2

        if percent == 100:
            percent -= random.randint(0, 100)

    DISPLAY.gauge_update(100)
    DISPLAY.gauge_stop()


def display_title(title):
    """Set the default title for the installer"""
    return DISPLAY.set_background_title(title)


def display_license():
    """Display license info"""
    return DISPLAY.yesno(
        """
        License

        The Symbiont Slim operating system is a compilation of software
        packages, each under its own license. The compilation itself is
        released under the MIT license. However, this compilation license
        does not supersede the licenses of code and content contained in the
        Symbiont Slim operating system, which conform to the legal guidelines
        described at <URL>.

        MIT license text

        Copyright 2021 Symbiont DCOS Project Authors.

        Permission is hereby granted, free of charge, to any person obtaining
        a copy of this software and associated documentation files (the
        "Software"), to deal in the Software without restriction, including
        without limitation the rights to use, copy, modify, merge, publish,
        distribute, sublicense, and/or sell copies of the Software, and to
        permit persons to whom the Software is furnished to do so, subject to
        the following conditions:

        The above copyright notice and this permission notice shall be included
        in all copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
        EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
        MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
        IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
        CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
        TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
        SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

        Source Availability

        You may also access a copy of this source code at:
        <URL>

        Export Regulations

        By downloading or installing Symbiont software, you acknowledge that
        you understand all of the following: Symbiont software and technical
        information may be subject to the U.S. Export Administration
        Regulations (the “EAR”) and other U.S. and foreign laws and may not
        be exported, re-exported or transferred (a) to any country listed in
        Country Group E:1 in Supplement No. 1 to part 740 of the EAR
        (currently, Cuba, Iran, North Korea, Sudan & Syria); (b) to any
        prohibited destination or to any end user who has been prohibited
        from participating in U.S. export transactions by any federal agency
        of the U.S.  government; or (c) for use in connection with the design,
        development or production of nuclear, chemical or biological weapons,
        or rocket systems, space launch vehicles, or sounding rockets, or
        unmanned air vehicle systems. You may not download Fedora software or
        technical information if you are located in one of these countries or
        otherwise subject to these restrictions. You may not provide Fedora
        software or technical information to individuals or entities located
        in one of these countries or otherwise subject to these restrictions.
        You are also responsible for compliance with foreign law requirements
        applicable to the import, export and use of Symbiont software and
        technical information.

        Do you accept the license terms?

        """,
        width=80,
        height=20,
        title="License Agreement",
        yes_label="Accept",
        no_label="Decline",
    )


def display_urlselector(default_text):
    """display URL downloader selection"""
    return DISPLAY.inputbox(
        """
        Please enter the download URL for "BASE IMAGE"

        """,
        width=100,
        height=10,
        init=default_text,
    )


def display_hostname():
    """Displays the dialog box for setting the hostname"""
    return DISPLAY.inputbox(
        "Please set the hostname", width=80, height=20, init="localhost.localdomain"
    )


def display_password():
    """Displays the dialog box for setting the root password"""
    return DISPLAY.passwordbox(
        "Please set the root password",
        width=80,
        height=10,
        init="changeme",
        insecure=True,
    )


def display_clock():
    """Displays the dialog for setting local time"""


def display_timezone():
    """Displays the dialog for all"""
    tzlist = pytz.common_timezones
    tzlist.sort()
    tag = tzlist
    desc = []

    for item in tag:
        desc.append(item.split("/")[-1])

    mytzlist = zip(tag, desc)
    return DISPLAY.menu(
        "Please select the system timezone.", width=80, height=40, choices=mytzlist
    )


def display_disk():
    """Select disk from list"""
    mydisks = list_disks()
    mydisks.sort()
    tag = []
    desc = []

    for item in mydisks:
        tag.append(f"/dev/{item}")
        desc.append(item)

    mydisklist = zip(tag, desc)

    return DISPLAY.menu(
        "Please select the disk to install to.", width=60, height=20, choices=mydisklist
    )


def display_image(url):
    """Select disk from list"""

    myimages = list_images(url)
    myimages.sort(reverse=True)
    tag = []
    desc = []

    for item in myimages:
        tag.append(item)
        desc.append("OS Image")

    myimglist = zip(tag, desc)

    return DISPLAY.menu(
        f"Please select the image from {url}.", width=80, height=20, choices=myimglist
    )


def display_alert(text):
    """Show alerts and error conditions"""
    DISPLAY.msgbox(text, width=60, height=10, colors=True)
    sys.exit(1)


def display_final_answer(img=None, tz=None, host=None, hd=None, passwd=None):
    """Display final selection before staring install"""
    return DISPLAY.yesno(
        f"""You have selected the following:
        Installation Disk: {hd}
        Installation Image: {img}
        Timezone: {tz}
        Hostname: {host}
        Password: ********

        Do you want to proceed?""",
        width=60,
        height=15,
    )


def display_complete():
    """Installation finished"""
    DISPLAY.msgbox("Installation has successfully completed.  System will now reboot")
