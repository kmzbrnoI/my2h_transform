import os
import logging
from functools import lru_cache
from typing import Dict, Any

from storage import Junction, BLK, BLM, Signal, Disconnector, Railway, Track_Section, Control_Area

DATASET_TYPES = ['PNL', 'OR', 'OPM', 'OPD', 'L', 'W', 'T', 'H', 'B', 'C', 'A', 'D', 'E', 'V', 'M', 'S', 'K', 'UV', 'Q',
                 'PST', 'EZ', 'N', 'R', 'P']


def remove_file(fname):
    '''Remove file if exists.'''

    if os.path.exists(fname):
        os.remove(fname)
        logging.info('Old output file [{}] was removed.'.format(fname))


def load_datasets(fname):
    '''
    Load all datasets from given file.
    '''

    datasets = []
    with open(fname, encoding='cp1250') as blk_file:
        lines = blk_file.readlines()
        dataset = []
        type_number = 0
        for line in lines:
            if line == '\n':
                datasets.append({'type': DATASET_TYPES[type_number], 'data': dataset})
                dataset = []
                type_number = type_number + 1
            else:
                dataset.append(line.strip('\n'))

    logging.info('Datasets loaded from file [{}].'.format(fname))

    return datasets


def all_blocks(session) -> Dict[str, Any]:
    result = {}
    for type_ in [Junction, BLK, BLM, Signal, Disconnector, Railway, Track_Section, Control_Area]:
        result.update({block.id: block for block in session.query(type_).all()})
    return result


@lru_cache(maxsize=1000)
def get_table_by_id(session, id_):

    entities = [Railway, Control_Area, Track_Section, Signal, BLK, BLM, Junction, Disconnector, BLUV]

    if id_ == 0:
        return None

    for entity in entities:
        is_valid_entity = session.query(entity).filter(entity.id == str(id_)).count()
        if is_valid_entity:
            return str(entity)

    return None
