"""
Database handler
"""

import os
import sqlite3


DB_FILE = './blk.sql'


def dict_factory(cursor, row):
    '''
    Helper for getting dictionaries from sqlite3 queries
    '''
    dictionary = {}
    for idx, col in enumerate(cursor.description):
        dictionary[col[0]] = row[idx]
    return dictionary


class Storage:
    '''
    Class handling database
    '''

    def __init__(self):

        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)

        self._conn = sqlite3.connect(DB_FILE)
        self._conn.row_factory = dict_factory
        self._cursor = self._conn.cursor()

        self._cursor.execute('''
            CREATE TABLE IF NOT EXISTS blt (
                id INTEGER PRIMARY KEY,
                groupt TEXT,
                label TEXT,
                label_text_part TEXT,
                gate_type TEXT,
                velocity INTEGER,
                det1 TEXT,
                det2 TEXT,
                det3 TEXT,
                det4 TEXT,
                boost INTEGER,
                zdroj TEXT,
                one_L TEXT,
                two_L TEXT,
                one_S TEXT,
                two_S TEXT,
                nvLtyp TEXT,
                hw_L TEXT,
                out1_L TEXT,
                out2_L TEXT,
                out3_L TEXT,
                out4_L TEXT,
                out5_L TEXT,
                nvStyp TEXT,
                hw_S TEXT,
                out1_S TEXT,
                out2_S TEXT,
                out3_S TEXT,
                out4_S TEXT,
                out5_S TEXT
            );
        ''')
        self._conn.commit()

    def __del__(self):
        self._conn.close()

    def save_blts(self, blts):
        '''
        Save records to blt table
        '''
        if len(blts) == 0:
            return

        columns = ', '.join(blts[0].keys())
        placeholders = ', '.join('?' * len(blts[0]))
        sql = 'REPLACE INTO blt ({}) VALUES ({});'.format(columns, placeholders)

        values = []
        for item in blts:
            values.append(list(item.values()))

        self._cursor.executemany(sql, values)
        self._conn.commit()
