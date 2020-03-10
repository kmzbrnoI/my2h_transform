"""My2h JOP Transform Utility
Usage:
  my2h_transform.py load_blocks <myjop_blk_file> <output_db_file>
  my2h_transform.py show_blocks <source_db_file>
  my2h_transform.py reid <source_db_file>
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

from utils import DATASET_TYPES, remove_file, load_datasets, all_blocks
from dataset import save_datasets
from storage import BASE
from writer import write_track_section, write_section, write_signal, write_junction, write_disconnector
from reid import ids_old_to_new


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

        write_track_section(session, config)
        write_section(session, config)
        write_signal(session, config)
        write_junction(session, config)
        write_disconnector(session, config)

        with open('./output.ini', 'w') as configfile:
            config.write(configfile, space_around_delimiters=False)

    if args['reid']:

        source_file = os.path.abspath(args['<source_db_file>'])

        SQLEngine = create_engine('sqlite:///{}'.format(source_file), echo=False)
        BASE.metadata.create_all(SQLEngine)
        SQLSession = sessionmaker(bind=SQLEngine)
        session = SQLSession()

        map_ = ids_old_to_new(session)

        all_blocks_ = all_blocks(session)
        for old_id, new_id in sorted(map_.items(), key=lambda kv: kv[1]):
            if new_id >= 100000:
                print(new_id, all_blocks_[old_id].name)


if __name__ == '__main__':
    main()
