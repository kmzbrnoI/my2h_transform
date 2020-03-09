import os


DATASET_TYPES = ['PNL', 'OR', 'OPM', 'OPD', 'L', 'W', 'T', 'H', 'B', 'C', 'A', 'D', 'E', 'V', 'M', 'S', 'K', 'UV', 'Q',
                 'PST', 'EZ', 'N', 'R', 'P']


def remove_file(fname):
    '''Remove file if exists.'''

    if os.path.exists(fname):
        os.remove(fname)
        print('# File [{}] was removed.'.format(fname))


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

    return datasets