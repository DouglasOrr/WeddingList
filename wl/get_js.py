import urllib.request
import os
from os import path
import subprocess
import shutil


def download(src, dest):
    parent = path.dirname(dest)
    if not path.isdir(parent):
        os.makedirs(parent)
    with urllib.request.urlopen(src) as fs:
        with open(dest, 'wb') as fd:
            fd.write(fs.read())


js_root = 'wl/static/lib/js'
css_root = 'wl/static/lib/css'

download('https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/css/bootstrap.min.css',  # NOQA
         path.join(css_root, 'bootstrap.css'))

download('https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/js/bootstrap.min.js',  # NOQA
         path.join(js_root, 'bootstrap.js'))

download('https://code.jquery.com/jquery-3.2.1.min.js',  # NOQA
         path.join(js_root, 'jquery.js'))

download('https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.11.0/umd/popper.min.js',  # NOQA
         path.join(js_root, 'popper.js'))

# Flipclock - have to unzip
subprocess.check_call(
    ['wget',
     'https://github.com/objectivehtml/FlipClock/archive/0.7.7.zip',
     '-qO', '/tmp/flipclock.zip'])
subprocess.check_call(
    ['unzip', '-q', '/tmp/flipclock.zip', '-d', '/tmp/flipclock'])
shutil.move('/tmp/flipclock/FlipClock-0.7.7/compiled/flipclock.min.js',
            path.join(js_root, 'flipclock.js'))
shutil.move('/tmp/flipclock/FlipClock-0.7.7/compiled/flipclock.css',
            path.join(css_root, 'flipclock.css'))
