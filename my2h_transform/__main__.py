"""My2h JOP Transform Utility
Usage:
  my2h_transform.py load_blocks <myjop_blk_file> <output_db_file>
  my2h_transform.py show_blocks <source_db_file>
  my2h_transform.py (-h | --help)
  my2h_transform.py --version

Options:
  -h --help          Show this screen.
  --version          Show version.
"""

import os
import json
import configparser
from docopt import docopt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils import DATASET_TYPES, remove_file, load_datasets
from dataset import save_datasets
from storage import BASE, Control_Area, Railway, Track_Section, Signal


def main():
    '''Entry point'''

    args = docopt(__doc__, version='0.0.1')

    if args['load_blocks']:

        output_file = os.path.abspath(args['<output_db_file>'])
        remove_file(output_file)

        SQLEngine = create_engine('sqlite:///{}'.format(output_file), echo=False)
        BASE.metadata.create_all(SQLEngine)
        SQLSession = sessionmaker(bind=SQLEngine)
        session = SQLSession()

        datasets = load_datasets(args['<myjop_blk_file>'])
        save_datasets(session, datasets)

    if args['show_blocks']:

        source_file = os.path.abspath(args['<source_db_file>'])

        SQLEngine = create_engine('sqlite:///{}'.format(source_file), echo=False)
        BASE.metadata.create_all(SQLEngine)
        SQLSession = sessionmaker(bind=SQLEngine)
        session = SQLSession()

        config = configparser.ConfigParser()
        config.optionxform = str
        # Track Sections
        for section, railway in session.query(
            Track_Section, Railway).filter(
            Track_Section.railway == Railway.id).order_by(
                Track_Section.id):

            data = {
                'nazev': '{} {}'.format(railway.shortname.split(' ', 1)[0], section.name),
                'typ': 1,
            }

            rcs_count = 0
            for det in (section.det1, section.det2, section.det3, section.det4):
                if det != '0:0':
                    rcs_count = rcs_count + 1

            RCSb0 = int(section.det1.split(':', 1)[0])
            RCSp0 = int(section.det1.split(':', 1)[1])
            RCSb1 = int(section.det2.split(':', 1)[0])
            RCSp1 = int(section.det2.split(':', 1)[1])
            RCSb2 = int(section.det3.split(':', 1)[0])
            RCSp2 = int(section.det3.split(':', 1)[1])
            RCSb3 = int(section.det4.split(':', 1)[0])
            RCSp3 = int(section.det4.split(':', 1)[1])

            if rcs_count != 0:
                data['RCScnt'] = rcs_count

            if RCSb0 != 0:
                data['RCSb0'] = RCSb0
                data['RCSp0'] = RCSp0

            if RCSb1 != 0:
                data['RCSb1'] = RCSb1
                data['RCSp1'] = RCSp1

            if RCSb2 != 0:
                data['RCSb2'] = RCSb2
                data['RCSp2'] = RCSp2

            if RCSb3 != 0:
                data['RCSb3'] = RCSb3
                data['RCSp3'] = RCSp3

            config[section.id] = data

        with open('./output.ini', 'w') as configfile:
            config.write(configfile, space_around_delimiters=False)


if __name__ == '__main__':
    main()
