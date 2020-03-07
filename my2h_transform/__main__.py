"""My2h JOP Transform Utility
Usage:
  my2h_transform.py blocks <myjop_blk_file>
  my2h_transform.py (-h | --help)
  my2h_transform.py --version

Options:
  -h --help          Show this screen.
  --version          Show version.
"""

import os
import json
from docopt import docopt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from storage import BASE, BLT, BLW


DB_FILE = './blk.db'


def main():
    '''Entry point'''
    args = docopt(__doc__, version='0.0.1')  # pylint: disable=unused-variable

    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print('File [{}] removed.'.format(DB_FILE))

    SQLEngine = create_engine('sqlite:///blk.db', echo=False)
    BASE.metadata.create_all(SQLEngine)
    SQLSession = sessionmaker(bind=SQLEngine)
    session = SQLSession()

    if args['blocks']:

        block_types = ['PNL', 'OR', 'OPM', 'OPD', 'L', 'W', 'T', 'H', 'B', 'C', 'A',
                       'D', 'E', 'V', 'M', 'S', 'K', 'UV', 'Q', 'PST', 'EZ', 'N', 'R', 'P']

        datasets = []
        with open(args['<myjop_blk_file>'], encoding='cp1250') as blk_file:
            lines = blk_file.readlines()
            dataset = []
            type_number = 0
            for line in lines:
                if line == '\n':
                    datasets.append({'type': block_types[type_number], 'data': dataset})
                    dataset = []
                    type_number = type_number + 1
                else:
                    dataset.append(line.strip('\n'))

        print('--- Datasets ---')
        for dataset in datasets:
            print(dataset['type'])

        print('--- BL T dataset ---')
        print('Zřejmě se jedná o koleje')
        blts = []
        for dataset in datasets[block_types.index('T')]['data'][1:]:
            data = dataset.split(';')
            blt = BLT(
                id=data[3],
                group=data[4],
                label=data[5],
                label_text_part=data[6],
                gate_type=data[7],
                velocity=data[12],
                det1=data[15],
                det2=data[16],
                det3=data[17],
                det4=data[18],
                boost=data[19],
                power_source=data[20],
                one_L=data[21],
                two_L=data[22],
                one_S=data[23],
                two_S=data[24],
                nvLtype=data[25],
                hw_L=data[26],
                out1_L=data[27],
                out2_L=data[28],
                out3_L=data[29],
                out4_L=data[30],
                out5_L=data[31],
                nvStype=data[32],
                hw_S=data[33],
                out1_S=data[34],
                out2_S=data[35],
                out3_S=data[36],
                out4_S=data[37],
                out5_S=data[38])
            blts.append(blt)

        session.add_all(blts)
        session.commit()

        print('--- BL W dataset ---')
        print('Koleje propojeny do tratí')
        blws = []
        for dataset in datasets[block_types.index('W')]['data'][1:]:
            data = dataset.split(';')
            blw = BLW(
                id=data[3],
                label=data[4],
                name=data[6],
                gate_type=data[7],
                conn_1=data[10],
                conn_2=data[11],
                conn_3=data[12],
                conn_4=data[13],
                conn_5=data[14],
                conn_6=data[15] if data[3] == str(341) else None)
            blws.append(blw)

        session.add_all(blws)
        session.commit()

        print('--- TR L dataset ---')
        print('Nepřináší žádnou novou informaci')


        #print(json.dumps(railway, sort_keys=True, indent=4))


if __name__ == '__main__':
    main()
