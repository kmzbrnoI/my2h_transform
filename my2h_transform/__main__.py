"""My2h JOP Transform Utility
Usage:
  my2h_transform.py load_blocks <myjop_blk_file> <output_db_file>
  my2h_transform.py reid <source_db_file> <output_reid_csv>
  my2h_transform.py remap_by_reid <source_db_file> <reid_csv> <output_db_file>
  my2h_transform.py create_ini <source_db_file> <output_ini_file>
  my2h_transform.py (-h | --help)
  my2h_transform.py --version

Options:
  -h --help          Show this screen.
  --version          Show version.
"""

import os
import csv
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
from remap import remap_control_area


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

    if args['reid']:

        source_file = os.path.abspath(args['<source_db_file>'])
        output_file = os.path.abspath(args['<output_reid_csv>'])

        SQLEngine = create_engine('sqlite:///{}'.format(source_file), echo=False)
        # BASE.metadata.create_all(SQLEngine)
        SQLSession = sessionmaker(bind=SQLEngine)
        session = SQLSession()

        map_ = ids_old_to_new(session)

        data = []
        all_blocks_ = all_blocks(session)
        for old_id, new_id in sorted(map_.items(), key=lambda kv: kv[1]):
            data.append({
                'old_id': old_id,
                'new_id': new_id,
                'block_name': all_blocks_[old_id].name,
            })

        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = ['old_id', 'new_id', 'block_name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    if args['remap_by_reid']:

        source_file = os.path.abspath(args['<source_db_file>'])
        reid_file = os.path.abspath(args['<reid_csv>'])
        output_file = os.path.abspath(args['<output_db_file>'])

        Source_SQLEngine = create_engine('sqlite:///{}'.format(source_file), echo=False)
        # BASE.metadata.create_all(Source_SQLEngine)
        Source_SQLSession = sessionmaker(bind=Source_SQLEngine)
        source_session = Source_SQLSession()

        Output_SQLEngine = create_engine('sqlite:///{}'.format(output_file), echo=False)
        BASE.metadata.create_all(Output_SQLEngine)
        Output_SQLSession = sessionmaker(bind=Output_SQLEngine)
        output_session = Output_SQLSession()

        reid = {}
        with open(reid_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                reid[row['old_id']] = row['new_id']

        remap_control_area(reid, source_session, output_session)

#        railways
#        track_sections
#        blms
#        blks
#        signals
#        junctions
#        disconnectors
#        blps
#        pnls
#        blezs
#        blqs
#        bluvs

    if args['create_ini']:

        source_file = os.path.abspath(args['<source_db_file>'])
        output_file = os.path.abspath(args['<output_ini_file>'])

        SQLEngine = create_engine('sqlite:///{}'.format(source_file), echo=False)
        # BASE.metadata.create_all(SQLEngine)
        SQLSession = sessionmaker(bind=SQLEngine)
        session = SQLSession()

        config = configparser.ConfigParser()
        config.optionxform = str

        write_track_section(session, config)
        write_section(session, config)
        write_signal(session, config)
        write_junction(session, config)
        write_disconnector(session, config)

        with open(output_file, 'w') as configfile:
            config.write(configfile, space_around_delimiters=False)


if __name__ == '__main__':
    main()
