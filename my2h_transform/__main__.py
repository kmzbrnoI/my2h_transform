"""My2h JOP Transform Utility
Usage:
  my2h_transform.py blocks <myjop_blk_file>
  my2h_transform.py (-h | --help)
  my2h_transform.py --version

Options:
  -h --help          Show this screen.
  --version          Show version.
"""


from docopt import docopt
import json

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

        print('--- TR L blocks ---')
        # block_types L = railway
        # spojovaci tabulka mezi zkratkou trati a kolejemi?
        # neobsahuje zadne ID, nutno nacit pozdeji
        for dataset in datasets[block_types.index('L')]['data'][1:]:
            data = dataset.split(';')
            print(data)
            railway = {
                'name': data[3],
            }
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
                'L': data[21],
                'LL': data[22],
                'S': data[23],
                'SS': data[24],
                'nvLtyp': data[25],
                'hw1': data[26],
                'lout1': data[27],
                'lout2': data[28],
                'lout3': data[29],
                'lout4': data[30],
                'lout5': data[31],
                'nvStyp': data[32],
                'hw2': data[33],
                'sout1': data[34],
                'sout2': data[35],
                'sout3': data[36],
                'sout4': data[37],
                'sout5': data[38],
            }
            blts.append(item)
            print(json.dumps(item, sort_keys=True, indent=4))

        storage.save_blts(blts)


if __name__ == '__main__':
    main()
