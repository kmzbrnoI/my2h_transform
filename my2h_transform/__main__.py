"""My2h JOP Transform Utility
Usage:
  my2h_transform.py blocks <myjop_blk_file>
  my2h_transform.py (-h | --help)
  my2h_transform.py --version

Options:
  -h --help          Show this screen.
  --version          Show version.
"""

import json
from docopt import docopt

from storage import Storage


def main():
    '''Entry point'''
    args = docopt(__doc__, version='0.0.1')  # pylint: disable=unused-variable

    storage = Storage()

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

        # print('--- TR L blocks ---')
        # block_types L = railway
        # spojovaci tabulka mezi zkratkou trati a kolejemi?
        # neobsahuje zadne ID, nutno nacit pozdeji
        # for dataset in datasets[block_types.index('L')]['data'][1:]:
        #    data = dataset.split(';')
        #    print(data)
        #    railway = {
        #        'name': data[3],
        #    }
            # print(json.dumps(railway, sort_keys=True, indent=4))

        print('--- BL T blocks ---')
        # trate?
        blts = []
        for dataset in datasets[block_types.index('T')]['data'][1:]:
            data = dataset.split(';')
            item = {
                'id': data[3],
                'groupt': data[4],
                'label': data[5],
                'label_text_part': data[6],
                'gate_type': data[7],
                'velocity': data[12],
                'det1': data[15],
                'det2': data[16],
                'det3': data[17],
                'det4': data[18],
                'boost': data[19],
                'zdroj': data[20],
                'one_L': data[21],
                'two_L': data[22],
                'one_S': data[23],
                'two_S': data[24],
                'nvLtyp': data[25],
                'hw_L': data[26],
                'out1_L': data[27],
                'out2_L': data[28],
                'out3_L': data[29],
                'out4_L': data[30],
                'out5_L': data[31],
                'nvStyp': data[32],
                'hw_S': data[33],
                'out1_S': data[34],
                'out2_S': data[35],
                'out3_S': data[36],
                'out4_S': data[37],
                'out5_S': data[38],
            }
            blts.append(item)
            print(json.dumps(item, sort_keys=True, indent=4))

        storage.save_blts(blts)


if __name__ == '__main__':
    main()
