"""My2h JOP Transform Utility
Usage:
  my2h_transform.py load_blocks <myjop_blk_file> <myjop_ztb_file> <output_db_file>
  my2h_transform.py reid <source_db_file> <output_reid_csv>
  my2h_transform.py remap_by_reid <source_db_file> <reid_csv> <output_db_file>
  my2h_transform.py create_ini <source_db_file> <output_ini_file>
  my2h_transform.py create_ir <db_file>
  my2h_transform.py (-h | --help)
  my2h_transform.py --version

Options:
  -h --help          Show this screen.
  --version          Show version.
"""

import os
import logging
import csv
import json
import configparser
from docopt import docopt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils import DATASET_TYPES, remove_file, load_datasets, all_blocks
from dataset import save_datasets
from storage import BASE, IR
from writer import write_railway, write_track_section, write_section, write_signal, write_junction, write_disconnector, write_ir
from reid import ids_old_to_new
from remap import remap_control_area, remap_railway, remap_track_section, remap_blm, remap_blk, remap_signal, remap_junction, remap_disconnector, remap_drive_path
from drive_path import load_drive_paths, save_drive_paths
from create_ir import create_ir


def main():
    '''Entry point'''

    args = docopt(__doc__, version='0.0.1')

    if args['load_blocks']:

        source_blk_file = os.path.abspath(args['<myjop_blk_file>'])
        source_ztb_file = os.path.abspath(args['<myjop_ztb_file>'])
        output_file = os.path.abspath(args['<output_db_file>'])

        remove_file(output_file)

        SQLEngine = create_engine('sqlite:///{}'.format(output_file), echo=False)
        BASE.metadata.create_all(SQLEngine)
        SQLSession = sessionmaker(bind=SQLEngine)
        session = SQLSession()

        datasets = load_datasets(source_blk_file)
        save_datasets(session, datasets)

        logging.info('Blocks succesfully saved in file [{}].'.format(output_file))

        drive_paths = load_drive_paths(source_ztb_file)
        save_drive_paths(session, drive_paths)

        logging.info('Drive paths succesfully saved in file [{}].'.format(output_file))

    if args['reid']:

        source_file = os.path.abspath(args['<source_db_file>'])
        output_file = os.path.abspath(args['<output_reid_csv>'])

        remove_file(output_file)

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

        logging.info('reid_map succesfully saved in file [{}].'.format(output_file))

    if args['remap_by_reid']:

        source_file = os.path.abspath(args['<source_db_file>'])
        reid_file = os.path.abspath(args['<reid_csv>'])
        output_file = os.path.abspath(args['<output_db_file>'])

        remove_file(output_file)

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
        remap_railway(reid, source_session, output_session)
        remap_track_section(reid, source_session, output_session)
        remap_blm(reid, source_session, output_session)
        remap_blk(reid, source_session, output_session)
        remap_signal(reid, source_session, output_session)
        remap_junction(reid, source_session, output_session)
        remap_disconnector(reid, source_session, output_session)

        remap_drive_path(reid, source_session, output_session)

#        blps
#        pnls
#        blezs
#        blqs
#        bluvs

        logging.info('Remapped data succesfully saved in file [{}].'.format(output_file))

    if args['create_ini']:

        source_file = os.path.abspath(args['<source_db_file>'])
        output_file = os.path.abspath(args['<output_ini_file>'])

        remove_file(output_file)

        SQLEngine = create_engine('sqlite:///{}'.format(source_file), echo=False)
        # BASE.metadata.create_all(SQLEngine)
        SQLSession = sessionmaker(bind=SQLEngine)
        session = SQLSession()

        blocks = []
        blocks.extend(write_railway(session))
        blocks.extend(write_track_section(session))
        blocks.extend(write_section(session))
        blocks.extend(write_signal(session))
        blocks.extend(write_junction(session))
        blocks.extend(write_disconnector(session))
        blocks.extend(write_ir(session))

        config = configparser.ConfigParser()
        config.optionxform = str

        for block in sorted(blocks, key=lambda k: k['id']):
            config[block['id']] = block['data']

        with open(output_file, 'w') as configfile:
            config.write(configfile, space_around_delimiters=False)

        logging.info('hJOP configuration data succesfully saved in file [{}].'.format(output_file))

    if args['create_ir']:
        db_file = os.path.abspath(args['<db_file>'])
        SQLEngine = create_engine('sqlite:///{}'.format(db_file), echo=False)
        SQLSession = sessionmaker(bind=SQLEngine)
        session = SQLSession()

        session.query(IR).delete()
        create_ir(session)


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    main()
