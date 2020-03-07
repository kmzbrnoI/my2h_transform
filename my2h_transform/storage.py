import os
import sqlite3


DB_FILE = './blk.sql'


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Storage:

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
                L TEXT,
                LL TEXT,
                S TEXT,
                SS TEXT,
                nvLtyp TEXT,
                hw1 TEXT,
                lout1 TEXT,
                lout2 TEXT,
                lout3 TEXT,
                lout4 TEXT,
                lout5 TEXT,
                nvStyp TEXT,
                hw2 TEXT,
                sout1 TEXT,
                sout2 TEXT,
                sout3 TEXT,
                sout4 TEXT,
                sout5 TEXT
            );
        ''')
        self._conn.commit()

    def __del__(self):
        self._conn.close()

    def save_blts(self, blts):

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
