"""Perform a bulk insert into the database, and download images.
"""

import csv
import os
import subprocess
from os import path
import shutil
from . import util


conn = util.connect()
try:
    list_file = 'list.csv'
    img_dir = 'wl/static/lib/img'
    extensions = {'image/jpeg': '.jpg', 'image/png': '.png'}
    clean = True

    cursor = conn.cursor()
    if clean:
        if path.isdir(img_dir):
            shutil.rmtree(img_dir)
        cursor.execute('delete from item')
        cursor.execute('delete from image')

    if not path.isdir(img_dir):
        os.makedirs(img_dir)

    with open(list_file) as f:
        for row in csv.DictReader(f):
            # Insert item first
            cursor.execute("""
            INSERT INTO item (id, title, description, value)
            VALUES (%(id)s, %(title)s, %(description)s, %(value)s)
            """, row)

            os.makedirs(path.join(img_dir, row['id']))
            for image_n in range(3):
                # Download up to three images, and store links in database
                img_url = row['image_%d' % image_n].strip()
                img_link = row['image_%d_link' % image_n].strip()
                if img_url != '':
                    # Download image
                    tmp = path.join('/tmp', '%x' % abs(hash(img_url)))
                    subprocess.check_call(['wget', img_url, '-qO', tmp])

                    # Autodetect mime type for the extension
                    img_type = subprocess.check_output(
                        ['file', '--brief', '--mime-type', tmp]
                    ).decode('utf-8').strip()
                    name = path.join(
                        row['id'], str(image_n) + extensions[img_type]
                    )
                    shutil.move(tmp, path.join(img_dir, name))

                    # Insert image
                    cursor.execute("""
                    INSERT INTO image (item_id, path, link, thumb)
                    VALUES (%s, %s, %s, %s)
                    """, (row['id'], name, img_link, image_n == 0))
    conn.commit()
    cursor.close()
finally:
    conn.close()
