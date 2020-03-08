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
from docopt import docopt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils import DATASET_TYPES, remove_file, load_datasets
from dataset import save_datasets
from storage import BASE, Control_Area


def main():
    '''Entry point'''

    args = docopt(__doc__, version='0.0.1')  # pylint: disable=unused-variable

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

        print('Control Areas')
        for area in session.query(Control_Area).order_by(Control_Area.name):
            print('  {}\t{}'.format(area.id, area.name))


if __name__ == '__main__':
    main()
