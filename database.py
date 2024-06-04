import sqlite3 as sql
import traceback
import shutil
import requests
from time import sleep

from config import group_name

post_table = group_name


def initiate(db):
    with sql.connect(db, timeout=100, check_same_thread=False) as conn:
        cur = conn.cursor()
        cur.execute(f'CREATE TABLE IF NOT EXISTS {post_table} ('
                    'post_id TEXT PRIMARY KEY,'
                    'text TEXT,'
                    'photo_list TEXT,'
                    'is_sent TEXT);')
        conn.commit()
        print(db, 'local DB initiated')


def write_to_db(db, val):
    try:
        with sql.connect(db, timeout=100, check_same_thread=False) as conn:
            cur = conn.cursor()
            cur.execute(f'INSERT INTO {post_table} (post_id, text, photo_list, is_sent) values (?,?,?,?)', val)
            conn.commit()
            print(val[0], 'Inserted')
    except:
        pass


def get_not_sent(db):
    try:
        with sql.connect(db, timeout=100, check_same_thread=False) as conn:
            cur = conn.cursor()
            result = cur.execute(f'SELECT post_id, text, photo_list, is_sent FROM {post_table} WHERE is_sent=?', (0,)).fetchall()
    except:
        print(traceback.format_exc())
    return result


def update_sent(db, val):
    try:
        with sql.connect(db, timeout=100, check_same_thread=False) as conn:
            cur = conn.cursor()
            update = cur.execute(f'UPDATE {post_table} SET is_sent=? WHERE post_id=?', (1, val))
            conn.commit()
            print(f'[POST_ID] [{val}] [UPDATED] [UPDATE_STATUS:{update}]')
    except:
        print(traceback.format_exc())


def save_media(photo_url):
    try:
        response = requests.get(photo_url, stream=True)
        photo_local = 'media/' + str(photo_url).split('tag')[1] + '.jpg'
        with open(photo_local, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        sleep(0.5)
        del response
        print(photo_local)
    except:
        print(traceback.format_exc())

