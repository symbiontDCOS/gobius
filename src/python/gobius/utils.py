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


import subprocess
import shlex
import json
import sys
import requests


def run(cmd, **kwargs):
    """Generic shell out wrapper"""
    return subprocess.run(cmd, **kwargs)


def spawn(cmd, **kwargs):
    """Non-blocking generic shell out wrapper"""
    return subprocess.Popen(cmd, **kwargs)


def die(msg):
    """Handles exiting the program.  Always returns status 1"""
    return sys.exit(msg)


def list_disks():
    """Gather disk names"""
    mydisks = run(shlex.split("/usr/bin/lsblk -SJ"), capture_output=True, check=True)
    mydisks = mydisks.stdout
    mydisks = json.loads(mydisks.decode("utf-8"))

    myblockdevices = []

    for drive in mydisks["blockdevices"]:
        myblockdevices.append(
            {
                "name": drive["name"],
                "model": drive["model"],
            }
        )

    # Remove listings for cdrom/dvdrom devices
    if "sr0" in myblockdevices:
        myblockdevices.remove("sr0")

    return myblockdevices


def list_images(url):
    """Pull the list of images from the server"""
    try:
        images = []
        resp = requests.get(url, timeout=30)

        for item in resp.json():
            if item["name"].endswith(".img") or item["name"].endswith(".img.xz"):
                images.append(f'{item["name"]}')

        return images

    except requests.Timeout:
        die("Request timed out. Please try again.  Aborting installation.")

    except json.JSONDecodeError:
        die("Invalid JSON detected. Can not detect images. Aborting Installation.")


def write_image(url, dest):
    """Write the image out to its final destination"""
    return spawn(
        shlex.split(f"/usr/bin/bmaptool --quiet copy --no-sig-verify {url} {dest}")
    )
