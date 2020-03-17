"""My2h JOP Transform Utility
Usage:
  loco.py convert <input.lok> <output.2lok>
  loco.py (-h | --help)
  loco.py --version

Options:
  -h --help          Show this screen.
  --version          Show version.
"""

import os
import logging
import configparser
from docopt import docopt

#Tady je soubor specifikace hnacího vozidla MyJOP (.lok) a hJOP (.2lok), položky v MyJOP souboru jsou:
#* adresa
#* nazev
#* majitel
#* poznamka
#* trida
#* zbytek dat ignorovat


def remove_file_if_exists(fname):
    '''Remove file if exists.'''

    if os.path.exists(fname):
        os.remove(fname)
        logging.info(f'Old output file [{fname}] was removed.')


class Loco:

    def __init__(self, input_fname):

        with open(input_fname, encoding='cp1250') as loco_file:
            line = loco_file.readline()
            loco_data = line.split(';')
            self.address = loco_data[0]
            self.name = loco_data[1]
            self.owner = loco_data[2]
            self.note = loco_data[3]
            self.kind = loco_data[4]

    def write_2lok(self, output_fname):

        global_data = {'version': '2.0'}
        data = {}
        if self.name:
            data['nazev'] = self.name
        if self.owner:
            data['majitel'] = self.owner
        if '.' in self.name:
            data['oznaceni'] = self.name
        if self.note:
            data['poznamka'] = self.note
        if self.kind:
            data['trida'] = self.kind

        config = configparser.ConfigParser()
        config.optionxform = str
        config['global'] = global_data
        config[self.address] = data

        with open(output_fname, 'w', encoding='utf8') as configfile:
            config.write(configfile, space_around_delimiters=False)

        logging.info(f'Loco succesfully saved in [{output_fname}].')



    def __str__(self):
        data = [self.address, self.name, self.owner, self.kind, self.note]
        return ';'.join(data)

    __repr__ = __str__


def main():
    '''Entry point'''

    args = docopt(__doc__, version='0.0.1')

    if args['convert']:

        input_file = os.path.abspath(args['<input.lok>'])
        output_file = os.path.abspath(args['<output.2lok>'])

        remove_file_if_exists(output_file)

        loco = Loco(input_file)
        loco.write_2lok(output_file)



if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
    main()
